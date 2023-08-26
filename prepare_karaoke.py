# This script used to prepare the music part of karaoke stream
# by download a list of MV from youtube
# and chunk these MV to 5 seconds segments

SONG_DATASET = [
    # 瀬戸乃とと
    "https://www.youtube.com/watch?v=QQxkfmQJEso",
    "https://www.youtube.com/watch?v=QT8OWSCJciQ",
    "https://www.youtube.com/watch?v=o4oTnZoBo_M",
    "https://www.youtube.com/watch?v=0b4OR-QYaHA",
    "https://www.youtube.com/watch?v=Y6bYEfnTdog",
    "https://www.youtube.com/watch?v=YHUZNTwGd1g",
    "https://www.youtube.com/watch?v=IHfp0qQBlt4",
    "https://www.youtube.com/watch?v=rOvDocTct80",
    "https://www.youtube.com/watch?v=tCwkx2vdtpw",
    "https://www.youtube.com/watch?v=Tef7qs1_dJU",
    "https://www.youtube.com/watch?v=Idl8qd0ixQo",
    "https://www.youtube.com/watch?v=9FwuR-MUQ8c",

    # Ratio Yuires
    "https://www.youtube.com/watch?v=ExFDrvU6q68",
    "https://www.youtube.com/watch?v=WYl7kRBM0wk",
    "https://www.youtube.com/watch?v=e0wPI5CwUpQ",
    "https://www.youtube.com/watch?v=BoscIJzjEhA",
    "https://www.youtube.com/watch?v=xYkUw3g4lhw",
    "https://www.youtube.com/watch?v=4AcbqN7JCQs",

    # 茶柱ノキ
    "https://www.youtube.com/watch?v=JQyRUVvusuY",
    "https://www.youtube.com/watch?v=zxgKLnNTJvs",
    "https://www.youtube.com/watch?v=y3vERVIlugI",
    "https://www.youtube.com/watch?v=ALvVE8YVaW4",
    "https://www.youtube.com/watch?v=SAmGpUCsfVM",
    "https://www.youtube.com/watch?v=RrJEeakytDI",
    "https://www.youtube.com/watch?v=V2qRISofCCs",
    "https://www.youtube.com/watch?v=faAWulI2CEU",
    "https://www.youtube.com/watch?v=KtSr7axJB48",
    "https://www.youtube.com/watch?v=IGSz_PRBj6Q",
    "https://www.youtube.com/watch?v=7LUE3s9Sai0",

    # 橘ひなの
    "https://www.youtube.com/watch?v=ZGIu8i8-YUU",
    "https://www.youtube.com/watch?v=cPtRNQz5nac",
    "https://www.youtube.com/watch?v=yTv14R0kCl4",
    "https://www.youtube.com/watch?v=YuTSkW3RqH8",
    "https://www.youtube.com/watch?v=XI6_Dt0N_1M",

    # 柚羽まくら
    "https://www.youtube.com/watch?v=zfo3Gmj2mbo",
    "https://www.youtube.com/watch?v=dVfGv1hPmjo",
    "https://www.youtube.com/watch?v=TC-wp-OTPXg",
    "https://www.youtube.com/watch?v=VZ-d4QjgOXo",
    "https://www.youtube.com/watch?v=SHqU3ENJTTQ",

    # YUKIHIME
    "https://www.youtube.com/watch?v=Tm--UAHlFY0",
    "https://www.youtube.com/watch?v=dk10g8OaE6E",
    "https://www.youtube.com/watch?v=TT4b45gH1Xw",
    "https://www.youtube.com/watch?v=2DHApttG-UU",
    "https://www.youtube.com/watch?v=xyehAKHmcXw",
    "https://www.youtube.com/watch?v=_OoQcJrJhYE",
    "https://www.youtube.com/watch?v=GreCy0ZOXZ4",

    # ニュイ・ソシエール
    "https://www.youtube.com/watch?v=fRfEPAvsBqU",
    "https://www.youtube.com/watch?v=d4v3cQ0o8SM",

    # ヰ世界情緒
    "https://www.youtube.com/watch?v=fxqy6jnJaD0",
    "https://www.youtube.com/watch?v=Xj3Frg6BpEA",
    "https://www.youtube.com/watch?v=oMwWBcGd_V8",
    "https://www.youtube.com/watch?v=LmaDRgdcwcY",
    "https://www.youtube.com/watch?v=kmkMfFljd-0",

    # ソフィア・ヴァレンタイン
    "https://www.youtube.com/watch?v=Nt9WVwU88uU",
]

ZATSUDAN_DATASET = [
    # 魑魅 ちとせ
    "https://www.youtube.com/watch?v=28bjlA0-y3Q",
    "https://www.youtube.com/watch?v=2qh4gnoqXPQ",
    "https://www.youtube.com/watch?v=mOVnwhRm_ec",

    # Pomu Rainpuff
    "https://www.youtube.com/watch?v=u0OEHULEQOA",
    "https://www.youtube.com/watch?v=JPhlFo6lGzo",

    # 茶柱ノキ
    "https://www.youtube.com/watch?v=teYQEZ2vdVE",
    "https://www.youtube.com/watch?v=StkOsd8nCZE",

    # 橘ひなの
    "https://www.youtube.com/watch?v=-1SKnP26Ytw",

    # ニュイ・ソシエール
    "https://www.youtube.com/watch?v=i6bB-4qsgm8",

    # ソフィア・ヴァレンタイン
    "https://www.youtube.com/watch?v=O25Ol3SE0no",
]

# yt-dlp "url" -o "filename"
# ffmpeg -i song1.webm -acodec pcm_s16le -ar 44100 song1.wav >/dev/null 2>&1  
# ffmpeg -i song1.wav -f segment -segment_time 3 -c copy out%03d.wav >/dev/null 2>&1 

import subprocess
import json
import os
import librosa
import math

SONG_DATASET_PATH = "dataset/songs"
ZATSUDAN_DATASET_PATH = "dataset/zatsudan"
JSON_PATH = "dataset/karaoke.json"

SAMPLE_RATE = 22050
DURATION = 2
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION


def extract_youtube_id(url):
    start = url.find("v=") + 2
    end = url.find("&", start)
    if end == -1:
        end = len(url)
    return url[start:end]


if __name__ == "__main__":

    data = {
        "mapping": ["song", "zatsudan"],
        "mfcc": [],
        "labels": [],
    }

    hop_length = 512
    n_mfcc = 13
    n_fft = 2048
    num_segments = 5

    num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)
    duration = "{}".format(DURATION * num_segments)

    for i, song in enumerate(SONG_DATASET):
        id = extract_youtube_id(song);
        name, out_name = ("{}/song_{}".format(SONG_DATASET_PATH, id), "{}/song_{}_out".format(SONG_DATASET_PATH, id))
        subprocess.run(["yt-dlp", "-f", "wv", "-f", "ba", song, "-o", "{}.webm".format(name)])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.webm".format(name), "-acodec", "pcm_s16le", "-ar", "44100", "{}.wav".format(name)])
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "{}.wav".format(name)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        total_duration = float(result.stdout)
        trim_duration = total_duration - 10
        subprocess.run(["ffmpeg", "-y", "-i", "{}.wav".format(name), "-ss", "5", "-t", str(trim_duration), "{}_trimmed.wav".format(name)]) 
        subprocess.run(["ffmpeg", "-n", "-i", "{}_trimmed.wav".format(name), "-f", "segment", "-segment_time", duration, "-c", "copy", "{}%04d.wav".format(out_name)])

        out_files = [f for f in os.listdir(SONG_DATASET_PATH) if os.path.basename(out_name) in f]
        for filename in out_files:
            filepath = os.path.join(SONG_DATASET_PATH, filename)
            signal, sr = librosa.load(filepath, sr=SAMPLE_RATE)

            for s in range(num_segments):
                start_sample = num_samples_per_segment * s
                finish_sample = start_sample + num_samples_per_segment

                mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_fft=n_fft, n_mfcc=n_mfcc, hop_length=hop_length)
                mfcc = mfcc.T

                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    data["mfcc"].append(mfcc.tolist())
                    data["labels"].append(0)
        
    
    for i, song in enumerate(ZATSUDAN_DATASET):
        id = extract_youtube_id(song);
        name, out_name = ("{}/zatsudan_{}".format(ZATSUDAN_DATASET_PATH, id), "{}/zatsudan_{}_out".format(ZATSUDAN_DATASET_PATH, id))
        subprocess.run(["yt-dlp", "-f", "wv", "-f", "ba", song, "-o", "{}.webm".format(name)])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.webm".format(name), "-acodec", "pcm_s16le", "-ar", "44100", "{}.wav".format(name)])
        subprocess.run(["ffmpeg", "-n", "-i", "{}.wav".format(name), "-f", "segment", "-segment_time", duration, "-c", "copy", "{}%04d.wav".format(out_name)])

        out_files = [f for f in os.listdir(ZATSUDAN_DATASET_PATH) if os.path.basename(out_name) in f]
        for filename in out_files:
            filepath = os.path.join(ZATSUDAN_DATASET_PATH, filename)
            signal, sr = librosa.load(filepath, sr=SAMPLE_RATE)

            for s in range(num_segments):
                start_sample = num_samples_per_segment * s
                finish_sample = start_sample + num_samples_per_segment

                mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_fft=n_fft, n_mfcc=n_mfcc, hop_length=hop_length)
                mfcc = mfcc.T

                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    data["mfcc"].append(mfcc.tolist())
                    data["labels"].append(1)
        
    with open(JSON_PATH, "w") as fp:
        json.dump(data, fp)