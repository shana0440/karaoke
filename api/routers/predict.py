from fastapi import APIRouter
from pydantic import BaseModel
from functools import reduce
import tensorflow as tf
import numpy as np
import config
from services.youtube import extract_video_id_from_url, download_audio
from services.ffmpeg import convert_to_wav
from train_model import preprocess
from utils.threading import ThreadWithReturnValue
from datetime import timedelta
import json

router = APIRouter()

model = tf.keras.models.load_model(config.MODEL_PATH)
model.summary()


# Define a function to predict a single spectrogram
def predict_feature(feature):
    feature = feature[np.newaxis, ...]
    prediction = model.predict(feature, verbose=0)
    return prediction[0][0]


# Define a function to predict a list of spectrograms using multiple threads
def predict_features(features, chunk_size=500):
    # Chunk the spectrograms into smaller lists
    chunks = [features[i : i + chunk_size] for i in range(0, len(features), chunk_size)]

    # Define a function to predict a single chunk of spectrograms
    def predict_chunk(chunk):
        return list(map(predict_feature, chunk))

    # Create a thread for each chunk and start them all
    threads = []
    for chunk in chunks:
        thread = ThreadWithReturnValue(target=predict_chunk, args=(chunk,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish and collect the results
    results = reduce(lambda x, y: x + y, [thread.join() for thread in threads])

    return results


def remove_noise(periods, threshold=1):
    cleaned_periods = []
    for period in periods:
        start, end = period
        if end - start > threshold:
            cleaned_periods.append(period)
    return cleaned_periods


def merge_close_periods(periods, threshold=2):
    merged_periods = []
    current_period = periods[0]
    for next_period in periods[1:]:
        if next_period[0] - current_period[1] <= threshold:
            current_period[1] = next_period[1]
        else:
            merged_periods.append(current_period)
            current_period = next_period
    merged_periods.append(current_period)
    return merged_periods


class YoutubeURL(BaseModel):
    url: str


@router.post("/predict/")
async def predict(youtube_url: YoutubeURL):
    id = extract_video_id_from_url(youtube_url.url)
    path = "{}/karaoke_{}.webm".format(config.KARAOKE_DATASET_PATH, id)
    print("download audio")
    download_audio(youtube_url.url, path)
    print("convert to wav")
    wav_file = convert_to_wav(path, config.SAMPLE_RATE)
    print("preprocess")
    features = np.array(preprocess(wav_file))
    print("predict")
    predictions = predict_features(features)

    predictions_with_time = [
        {"time": str(timedelta(seconds=i)), "prediction": str(p)}
        for i, p in enumerate(predictions)
    ]
    with open(f"predictions/{id}.json", "w") as fp:
        json.dump({"predictions": predictions_with_time}, fp, indent=2)

    # Determine when the streamer starts and stops singing
    singing_periods = []
    start_singing = None
    for idx, pred in enumerate(predictions):
        if pred != 0 and start_singing is None:  # Streamer starts singing
            start_singing = idx * config.SEGMENT_SECONDS
        elif pred == 0 and start_singing is not None:  # Streamer stops singing
            end_singing = idx * config.SEGMENT_SECONDS
            singing_periods.append([start_singing, end_singing])
            start_singing = None
    # If the streamer is still singing at the end of the stream
    if start_singing is not None:
        singing_periods.append(
            [start_singing, len(predictions) * config.SEGMENT_SECONDS]
        )

    timeslots = singing_periods
    timeslots = merge_close_periods(timeslots, 10)
    # timeslots = remove_noise(timeslots, 5)

    return {"timeslots": timeslots}
