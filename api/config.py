import math

DATASET_SOURCE = "dataset/source.json"
TESTSET_SOURCE = "dataset/test.json"
KARAOKE_DATASET_PATH = "dataset/karaoke"
SONG_DATASET_PATH = "dataset/songs"
ZATSUDAN_DATASET_PATH = "dataset/zatsudan"
JSON_PATH = "dataset/karaoke.json"
MODEL_PATH = "dataset/models/karaoke_model"

SAMPLE_RATE = 22050
SEGMENT_SECONDS = 1

HOP_LENGTH = 512
N_FFT = 2048

DB_URL = "sqlite:///karaoke.db"