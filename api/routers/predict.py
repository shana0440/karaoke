from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import os
import librosa
import tensorflow.keras as keras
import numpy as np
import config
import utils

router = APIRouter()

model = keras.models.load_model(config.MODEL_PATH)
model.summary()


def remove_noise(periods):
    cleaned_periods = []
    for start, end in periods:
        if end - start > 50:
            cleaned_periods.append([start, end])
    return cleaned_periods 


class YoutubeURL(BaseModel):
    url: str


@router.post("/predict/")
async def predict(youtube_url: YoutubeURL):
    id = utils.extract_youtube_id(youtube_url.url)
    name, out_name = ("{}/karaoke_{}".format(config.KARAOKE_DATASET_PATH, id), "{}/karaoke_{}_out".format(config.KARAOKE_DATASET_PATH, id))
    subprocess.run(["yt-dlp", "-f", "wv", "-f", "ba", youtube_url.url, "-o", "{}.webm".format(name)])
    subprocess.run(["ffmpeg", "-n", "-i", "{}.webm".format(name), "-acodec", "pcm_s16le", "-ar", "44100", "{}.wav".format(name)])
    subprocess.run(["ffmpeg", "-n", "-i", "{}.wav".format(name), "-f", "segment", "-segment_time", config.SEGMENT_DURATION, "-c", "copy", "{}%04d.wav".format(out_name)])
    
    out_files = [f for f in os.listdir(config.KARAOKE_DATASET_PATH) if os.path.basename(out_name) in f]
    out_files.sort()

    predictions = []
    for j, filename in enumerate(out_files):
        filepath = os.path.join(config.KARAOKE_DATASET_PATH, filename)
        signal, sr = librosa.load(filepath, sr=config.SAMPLE_RATE)

        mfcc_set = []
        for s in range(config.NUM_SEGMENTS):
            start_sample = config.NUM_SAMPLES_PER_SEGMENT * s
            finish_sample = start_sample + config.NUM_SAMPLES_PER_SEGMENT

            mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_fft=config.N_FFT, n_mfcc=config.N_MFCC, hop_length=config.HOP_LENGTH)
            mfcc = mfcc.T

            if len(mfcc) == config.EXPECTED_NUM_MFCC_VECTORS_PER_SEGMENT:
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
            singing_periods.append([start_singing, end_singing])
            start_singing = None
    # If the streamer is still singing at the end of the stream
    if start_singing is not None:
        singing_periods.append([start_singing, len(predictions) * 5])

    timeslots = remove_noise(singing_periods)
    
    return {"timeslots": timeslots}


