from pyyoutube import Client, Channel, Video
from typing import List
import config
import re

yt = Client(api_key=config.YOUTUBE_API_KEY)


def get_video_info(video_id: str):
    result = yt.videos.list(video_id=video_id)
    return result.items[0] if len(result.items) > 0 else None


def get_videos_info(video_ids: List[str]) -> List[Video]:
    # youtube api will throw error if too many video id
    chunked_video_ids = [video_ids[i : i + 50] for i in range(0, len(video_ids), 50)]
    videos = []
    for chunk in chunked_video_ids:
        chunk_videos = yt.videos.list(video_id=",".join(chunk), max_results=len(chunk))
        videos.extend(chunk_videos.items)
    return videos


def get_channel_info(channel_id: str):
    result = yt.channels.list(channel_id=channel_id)
    return result.items[0].snippet if len(result.items) > 0 else None


def get_channels_info(channel_ids: List[str]) -> List[Channel]:
    # youtube api will throw error if too many video id
    chunked_channel_ids = [
        channel_ids[i : i + 50] for i in range(0, len(channel_ids), 50)
    ]
    channels = []
    for chunk in chunked_channel_ids:
        chunk_channels = yt.channels.list(
            channel_id=",".join(chunk), max_results=len(chunk)
        )
        channels.extend(chunk_channels.items)
    return channels


# TODO: make cache stateless
banner_url_cache = {}


def get_channel_banner_url(channel_id: str):
    if banner_url_cache.get(channel_id):
        return banner_url_cache.get(channel_id)

    result = yt.channels.list(channel_id=channel_id)
    banner_url = (
        result.items[0].brandingSettings.image.bannerExternalUrl
        if len(result.items) > 0
        else None
    )
    banner_url_cache[channel_id] = banner_url
    return banner_url


def get_video_most_like_comment(video_id: str):
    result = yt.commentThreads.list(video_id=video_id, order="relevance")
    if len(result.items) == 0:
        return None
    most_like_comment = result.items[0]
    for comment in result.items:
        if (
            most_like_comment.snippet.topLevelComment.snippet.likeCount
            < comment.snippet.topLevelComment.snippet.likeCount
        ):
            most_like_comment = comment
    return most_like_comment


def extract_video_id_from_url(url):
    start = url.find("v=") + 2
    end = url.find("&", start)
    if end == -1:
        end = len(url)
    return url[start:end]


def get_highest_thumbnail_url(resource):
    return (
        (resource.thumbnails.standard and resource.thumbnails.standard.url)
        or (resource.thumbnails.high and resource.thumbnails.high.url)
        or (resource.thumbnails.medium and resource.thumbnails.medium.url)
        or resource.thumbnails.default.url
    )


def get_custom_url_from_channel_url(channel_url: str):
    match = re.search(r"@(\w+)", channel_url)
    if match:
        return match.group(1)
    return None


def get_channel_id_from_custom_url(custom_url: str):
    result = yt.search.list(type="channel", q=custom_url)
    return result.items[0].snippet.channelId if len(result.items) > 0 else None


def get_music_less_than_20mins_from_channel_id(channel_id: str):
    def make_fetch_videos(video_duration):
        def fetch_videos(page_token):
            result = yt.search.list(
                channel_id=channel_id,
                max_results=50,  # 50 is the maximum value
                order="date",
                type="video",
                video_duration=video_duration,
                page_token=page_token,
                topic_id="/m/04rlf",
            )
            return result.nextPageToken, result.items

        return fetch_videos

    medium_result = continue_fetch(make_fetch_videos("medium"))
    short_result = continue_fetch(make_fetch_videos("short"))
    return medium_result + short_result


def continue_fetch(fetch):
    results = []
    page_token = ""
    while True:
        page_token, items = fetch(page_token)
        results += items
        if not page_token:
            break
    return results
