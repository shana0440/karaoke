from pyyoutube import Client
import config

yt = Client(api_key=config.YOUTUBE_API_KEY)


def get_video_info(video_id: str):
    result = yt.videos.list(video_id=video_id)
    return result.items[0].snippet if len(result.items) > 0 else None


def get_channel_info(channel_id: str):
    result = yt.channels.list(channel_id=channel_id)
    return result.items[0].snippet if len(result.items) > 0 else None


def extract_video_id_from_url(url):
    start = url.find("v=") + 2
    end = url.find("&", start)
    if end == -1:
        end = len(url)
    return url[start:end]