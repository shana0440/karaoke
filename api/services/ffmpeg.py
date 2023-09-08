import os
import subprocess


def split_audio_segments(filepath, segment_seconds):
    path_without_ext = os.path.splitext(filepath)[0]
    outpath = f"{path_without_ext}_out"
    subprocess.run(
        [
            "ffmpeg",
            "-n",
            "-i",
            filepath,
            "-f",
            "segment",
            "-segment_time",
            f"{segment_seconds}",
            "-c",
            "copy",
            f"{outpath}_%04d.wav",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    dirname = os.path.dirname(filepath)
    out_files = [
        os.path.join(dirname, f)
        for f in os.listdir(dirname)
        if os.path.basename(outpath) in f
    ]
    out_files.sort()
    return out_files


def convert_to_wav(filepath, sr):
    path_without_ext = os.path.splitext(filepath)[0]
    outpath = f"{path_without_ext}.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-n",
            "-i",
            filepath,
            "-acodec",
            "pcm_s16le",
            "-ar",
            f"{sr}",
            outpath,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return outpath


def extract_audio_segment(filepath, start, to, output):
    subprocess.run(
        [
            "ffmpeg",
            "-n",
            "-i",
            filepath,
            "-ss",
            start,
            "-to",
            to,
            "-c",
            "copy",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def get_audio_duration(filepath):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filepath,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    total_duration = str(float(result.stdout))
    return total_duration
