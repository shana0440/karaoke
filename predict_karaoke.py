# This script used to prepare the music part of karaoke stream
# by download a list of MV from youtube
# and chunk these MV to 5 seconds segments

KARAOKE_DATASET = [
    # 瀬戸乃とと
    "https://www.youtube.com/watch?v=8kFW1rqohiI",

    # Ratio Yuires
    "https://www.youtube.com/watch?v=j-STpN-jOgI",

    # 茶柱ノキ
    "https://www.youtube.com/watch?v=VKo1SJqf6OE",

    # 橘ひなの
    "https://www.youtube.com/watch?v=e4gzua_l-mU",

    # 柚羽まくら
    "https://www.youtube.com/watch?v=hlxZg4vfhbI",
]

# yt-dlp "url" -o "filename"
# ffmpeg -i song1.webm -acodec pcm_s16le -ar 44100 song1.wav >/dev/null 2>&1  
# ffmpeg -i song1.wav -f segment -segment_time 3 -c copy out%03d.wav >/dev/null 2>&1 

import subprocess
import json
import os
import librosa
import math
import tensorflow.keras as keras
import datetime
import numpy as np

KARAOKE_DATASET_PATH = "dataset/karaoke"

SAMPLE_RATE = 22050
DURATION = 3
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION


if __name__ == "__main__":

    model = keras.models.load_model('models/karaoke_model')

    model.summary()

    hop_length = 512
    n_mfcc = 13
    n_fft = 2048
    num_segments = 5

    num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)

    duration = "{}".format(num_segments * DURATION)

    result = []

    for i, stream in enumerate(KARAOKE_DATASET):
        name, out_name = ("{}/karaoke{}".format(KARAOKE_DATASET_PATH, i), "{}/karaoke{}_out".format(KARAOKE_DATASET_PATH, i))
        subprocess.run(["yt-dlp", stream, "-o", name])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.webm".format(name), "-acodec", "pcm_s16le", "-ar", "44100", "{}.wav".format(name)])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.mkv".format(name), "-acodec", "pcm_s16le", "-ar", "44100", "{}.wav".format(name)])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.wav".format(name), "-f", "segment", "-segment_time", duration, "-c", "copy", "{}%04d.wav".format(out_name)])

        out_files = [f for f in os.listdir(KARAOKE_DATASET_PATH) if os.path.basename(out_name) in f]
        out_files.sort()

        predictions = []
        for j, filename in enumerate(out_files):
            filepath = os.path.join(KARAOKE_DATASET_PATH, filename)
            signal, sr = librosa.load(filepath, sr=SAMPLE_RATE)

            mfcc_set = []
            for s in range(num_segments):
                start_sample = num_samples_per_segment * s
                finish_sample = start_sample + num_samples_per_segment

                mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_fft=n_fft, n_mfcc=n_mfcc, hop_length=hop_length)
                mfcc = mfcc.T

                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    mfcc_set.append(mfcc.tolist())


            inputs = np.array(mfcc_set)
            inputs = inputs[..., np.newaxis]

            for k, x_test in enumerate(inputs):
                x_test = x_test[np.newaxis, ...]
                prediction = model.predict(x_test)
                predicted_index = np.argmax(prediction, axis=1)
                predictions.append(predicted_index[0])

        # Determine when the streamer starts and stops singing
        singing_periods = []
        start_singing = None
        for idx, pred in enumerate(predictions):
            if pred == 0 and start_singing is None:  # Streamer starts singing
                start_singing = idx * 5  # Each prediction corresponds to a 5 second interval
            elif pred == 1 and start_singing is not None:  # Streamer stops singing
                end_singing = idx * 5
                singing_periods.append((start_singing, end_singing))
                start_singing = None
        # If the streamer is still singing at the end of the stream
        if start_singing is not None:
            singing_periods.append((start_singing, len(predictions) * 5))

        periods = []
        for start, end in singing_periods:
            periods.append([start, end])

        result.append({ "stream": stream, "periods": periods })
    
    with open("predict_{}s.txt".format(DURATION), "w") as fp:
        
        json.dump(result, fp, indent=4)