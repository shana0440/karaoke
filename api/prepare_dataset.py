import config
import subprocess
import json
import os
import librosa
import utils


def load_data_source():
    with open(config.DATASET_SOURCE, "r") as fp:
        data = json.load(fp)
    return data


def splite_song_and_zatudan(stream_path, id, songs_range):
    songs = []
    zatudans = []
    start = "00:00:00"
    for range in songs_range:
        start_time, end_time = range
        zatudan = os.path.join(
            config.ZATSUDAN_DATASET_PATH,
            "zatudan_{}_{}_{}.wav".format(id, start, start_time),
        )
        subprocess.run(
            [
                "ffmpeg",
                "-n",
                "-i",
                stream_path,
                "-ss",
                start,
                "-to",
                start_time,
                "-c",
                "copy",
                zatudan,
            ]
        )
        song = os.path.join(
            config.SONG_DATASET_PATH,
            "song_{}_{}_{}.wav".format(id, start_time, end_time),
        )
        subprocess.run(
            [
                "ffmpeg",
                "-n",
                "-i",
                stream_path,
                "-ss",
                start_time,
                "-to",
                end_time,
                "-c",
                "copy",
                song,
            ]
        )
        start = end_time
        songs.append(song)
        zatudans.append(zatudan)

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            stream_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    total_duration = str(float(result.stdout))
    zatudan = os.path.join(
        config.ZATSUDAN_DATASET_PATH,
        "zatudan_{}_{}_{}.wav".format(id, start, total_duration),
    )
    subprocess.run(
        [
            "ffmpeg",
            "-n",
            "-i",
            stream_path,
            "-ss",
            start,
            "-to",
            total_duration,
            "-c",
            "copy",
            zatudan,
        ]
    )
    zatudans.append(zatudan)

    return zatudans, songs


def prepare_data(data, files, value):
    for filepath in files:
        signal, sr = librosa.load(filepath, sr=config.SAMPLE_RATE)

        for s in range(config.NUM_SEGMENTS):
            start_sample = config.NUM_SAMPLES_PER_SEGMENT * s
            finish_sample = start_sample + config.NUM_SAMPLES_PER_SEGMENT

            mfcc = librosa.feature.mfcc(
                y=signal[start_sample:finish_sample],
                sr=sr,
                n_fft=config.N_FFT,
                n_mfcc=config.N_MFCC,
                hop_length=config.HOP_LENGTH,
            )
            mfcc = mfcc.T

            if len(mfcc) == config.EXPECTED_NUM_MFCC_VECTORS_PER_SEGMENT:
                data["mfcc"].append(mfcc.tolist())
                data["labels"].append(value)


if __name__ == "__main__":
    data = {
        "mapping": ["song", "zatsudan"],
        "mfcc": [],
        "labels": [],
    }

    source = load_data_source()

    for i, stream in enumerate(source["streams"]):
        id = utils.extract_youtube_id(stream["url"])
        name, out_name = (
            "{}/karaoke_{}".format(config.KARAOKE_DATASET_PATH, id),
            "{}/karaoke_{}_out".format(config.KARAOKE_DATASET_PATH, id),
        )
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                "wv",
                "-f",
                "ba",
                stream["url"],
                "-o",
                "{}.webm".format(name),
            ]
        )
        subprocess.run(
            [
                "ffmpeg",
                "-n",
                "-i",
                "{}.webm".format(name),
                "-acodec",
                "pcm_s16le",
                "-ar",
                "44100",
                "{}.wav".format(name),
            ]
        )
        zatudans, songs = splite_song_and_zatudan(
            "{}.wav".format(name), id, stream["songs"]
        )

        prepare_data(data, songs, 0)
        prepare_data(data, zatudans, 1)

    with open(config.JSON_PATH, "w") as fp:
        json.dump(data, fp)
