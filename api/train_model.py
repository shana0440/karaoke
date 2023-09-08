import os
import json
from config import (
    SAMPLE_RATE,
    KARAOKE_DATASET_PATH,
    HOP_LENGTH,
    N_FFT,
    MODEL_PATH,
    SEGMENT_SECONDS,
    DATASET_SOURCE,
    ZATSUDAN_DATASET_PATH,
    SONG_DATASET_PATH,
)
from matplotlib import pyplot as plt
import tensorflow as tf
import librosa
from services.youtube import extract_video_id_from_url, download_audio
from services.ffmpeg import (
    split_audio_segments,
    extract_audio_segment,
    get_audio_duration,
    convert_to_wav,
)
import numpy as np
import argparse


def load_data_source():
    with open(DATASET_SOURCE, "r") as fp:
        data = json.load(fp)
    return data


def splite_song_and_zatudan(audio_path, id, songs_range):
    songs = []
    zatudans = []
    start = "00:00:00"
    for range in songs_range:
        start_time, end_time = range
        zatudan = os.path.join(
            ZATSUDAN_DATASET_PATH,
            "zatudan_{}_{}_{}.wav".format(id, start, start_time),
        )
        extract_audio_segment(audio_path, start, start_time, zatudan)
        song = os.path.join(
            SONG_DATASET_PATH,
            "song_{}_{}_{}.wav".format(id, start_time, end_time),
        )
        extract_audio_segment(audio_path, start_time, end_time, song)
        start = end_time
        songs.append(song)
        zatudans.append(zatudan)

    total_duration = get_audio_duration(audio_path)
    zatudan = os.path.join(
        ZATSUDAN_DATASET_PATH,
        "zatudan_{}_{}_{}.wav".format(id, start, total_duration),
    )
    extract_audio_segment(audio_path, start, total_duration, zatudan)
    zatudans.append(zatudan)

    return zatudans, songs


def load_wav_22050_mono(filepath):
    signal, sr = librosa.load(filepath, sr=SAMPLE_RATE)
    target_sr = 22050
    wav_16k = librosa.resample(signal, orig_sr=sr, target_sr=target_sr)
    return wav_16k, target_sr


def padding_zero(sample, sequence_length):
    sample = sample[:sequence_length]
    zero_padding = tf.zeros([sequence_length] - tf.shape(sample), dtype=tf.float32)
    sample = tf.concat([zero_padding, sample], 0)
    return sample


def preprocess(filepath):
    wav, sr = librosa.load(filepath, sr=SAMPLE_RATE)
    sequence_length = int(sr * SEGMENT_SECONDS)
    if len(wav) <= sequence_length:
        return []

    split_files = split_audio_segments(filepath, SEGMENT_SECONDS)
    features = []
    for file in split_files:
        wav, sr = librosa.load(file, sr=SAMPLE_RATE)

        sample = wav
        sample = padding_zero(sample, sequence_length)
        # stft = librosa.stft(np.array(sample), n_fft=N_FFT, hop_length=HOP_LENGTH)
        # spectrogram = np.abs(stft)
        # features.append(spectrogram[..., np.newaxis])
        mfcc = librosa.feature.mfcc(
            y=np.array(sample), sr=sr, n_mfcc=128, hop_length=HOP_LENGTH, n_fft=N_FFT
        )
        mfcc = mfcc.T
        # show_mfcc(mfcc)
        features.append(mfcc[..., np.newaxis])

    return features


def show_spectrogram(spectrogram):
    log_spectrogram = librosa.amplitude_to_db(spectrogram)
    librosa.display.specshow(log_spectrogram, sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    plt.colorbar()
    plt.show()


def show_mfcc(mfcc):
    librosa.display.specshow(mfcc, sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    plt.xlabel("Time")
    plt.colorbar()
    plt.show()


def show_wave(wave1, wave2):
    plt.plot(wave1)
    plt.plot(wave2)
    plt.show()


def build_model(input_shape):
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=input_shape)
    )
    model.add(tf.keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(tf.keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    return model


def save_dataset(dataset: tf.data.Dataset):
    chunk_size = 1024
    dir = "dataset/train"
    for i, chunk in enumerate(dataset.batch(chunk_size)):
        chunk.save(dir)
    return dir


def prepare_dataset():
    source = load_data_source()

    print("download and split")
    all_songs = []
    all_zatudans = []
    for i, stream in enumerate(source["streams"]):
        id = extract_video_id_from_url(stream["url"])
        print("process video {}".format(id))
        name = "{}/karaoke_{}.webm".format(KARAOKE_DATASET_PATH, id)
        download_audio(stream["url"], name)
        wav_file = convert_to_wav(name, SAMPLE_RATE)
        zatudans, songs = splite_song_and_zatudan(wav_file, id, stream["songs"])
        all_songs += songs
        all_zatudans += zatudans

    print("preprocess songs")
    dataset = None
    for song in all_songs:
        sliced_song = preprocess(song)
        if len(sliced_song) == 0:
            continue
        song_dataset = tf.data.Dataset.zip(
            (
                tf.data.experimental.from_list(sliced_song),
                tf.data.Dataset.from_tensor_slices(tf.ones(len(sliced_song))),
            )
        )
        dataset = (
            dataset.concatenate(song_dataset) if dataset is not None else song_dataset
        )

    print("preprocess zatudans")
    for zatudan in all_zatudans:
        sliced_zatudan = preprocess(zatudan)
        if len(sliced_zatudan) == 0:
            continue
        zatudan_dataset = tf.data.Dataset.zip(
            (
                tf.data.experimental.from_list(sliced_zatudan),
                tf.data.Dataset.from_tensor_slices(tf.zeros(len(sliced_zatudan))),
            )
        )
        dataset = dataset.concatenate(zatudan_dataset)

    dataset.save("dataset/train")
    return dataset


def train(dataset: tf.data.Dataset = None):
    print("load dataset")
    if dataset is None:
        data = tf.data.Dataset.load("dataset/train")
    else:
        data = dataset

    data = data.shuffle(buffer_size=1000)
    data = data.batch(32)
    data = data.prefetch(tf.data.experimental.AUTOTUNE)

    print("prepare model")
    train_count = int(len(data) * 0.7)
    train = data.take(train_count)
    test = data.skip(train_count).take(len(data) - train_count)
    samples, labels = train.as_numpy_iterator().next()
    input_shape = (samples.shape[1], samples.shape[2], samples.shape[3])
    model = build_model(input_shape)

    model.summary()
    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.0001)
    model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=[
            tf.keras.metrics.Recall(),
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Accuracy(),
        ],
    )

    print("start training")
    hist = model.fit(
        train,
        validation_data=(test),
        epochs=50,
        batch_size=32,
    )

    # save model
    model.save(MODEL_PATH)

    with open(os.path.join(MODEL_PATH, "history.json"), "w") as fp:
        json.dump(hist.history, fp, indent=2)

    # Plot validation loss
    plt.subplot(2, 2, 1)
    plt.title("Validation Loss")
    plt.plot(hist.history["val_loss"])

    # Plot validation precision
    plt.subplot(2, 2, 2)
    plt.title("Validation Precision")
    plt.plot(hist.history["val_precision"])

    # Plot validation recall
    plt.subplot(2, 2, 3)
    plt.title("Validation Recall")
    plt.plot(hist.history["val_recall"])

    # Plot validation accuracy
    plt.subplot(2, 2, 4)
    plt.title("Validation Accuracy")
    plt.plot(hist.history["val_accuracy"])

    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_PATH, "history.png"))
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Prepare the dataset")
    parser.add_argument("--train", action="store_true", help="Train the dataset")
    args = parser.parse_args()

    if args.prepare:
        prepare_dataset()
    elif args.train:
        train()
    else:
        dataset = prepare_dataset()
        train(dataset)


if __name__ == "__main__":
    print(tf.config.list_physical_devices("GPU"))
    main()
