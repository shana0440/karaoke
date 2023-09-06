from fastapi import APIRouter
from schemas import MvSchema
from services.youtube import (
    get_custom_url_from_channel_url,
    get_channel_id_from_custom_url,
    get_music_less_than_20mins_from_channel_id,
    get_highest_thumbnail_url,
    extract_video_id_from_url,
    get_video_info,
    get_videos_info,
    get_channels_info,
)
from typing import List
from pydantic import BaseModel
from isodate import parse_duration
from database.session import open_session
from models import Channel, Video, Clip


router = APIRouter()


class RetrieveMvsFromChannelUrlRequest(BaseModel):
    channel_url: str


@router.post("/mvs/channel")
def get_mvs_from_channel_url(request: RetrieveMvsFromChannelUrlRequest):
    custom_url = get_custom_url_from_channel_url(request.channel_url)
    channel_id = get_channel_id_from_custom_url(custom_url)
    video_ids = [
        video.id.videoId
        for video in get_music_less_than_20mins_from_channel_id(channel_id)
    ]
    videos = get_videos_info(video_ids)

    return [
        MvSchema(
            id=video.id,
            title=video.snippet.title,
            channel_id=video.snippet.channelId,
            channel_title=video.snippet.channelTitle,
            thumbnail_url=get_highest_thumbnail_url(video.snippet),
            duration=parse_duration(video.contentDetails.duration).total_seconds(),
        )
        for video in videos
    ]


class RetrieveMvFromVideoUrlRequest(BaseModel):
    video_url: str


@router.post("/mvs/video")
def get_mv_from_video_url(request: RetrieveMvFromVideoUrlRequest):
    video_id = extract_video_id_from_url(request.video_url)
    video_info = get_video_info(video_id)
    return MvSchema(
        id=video_id,
        title=video_info.snippet.title,
        channel_id=video_info.snippet.channelId,
        channel_title=video_info.snippet.channelTitle,
        thumbnail_url=get_highest_thumbnail_url(video_info.snippet),
        duration=parse_duration(video_info.contentDetails.duration).total_seconds(),
    )


class CreateMvsRequest(BaseModel):
    video_ids: List[str]


@router.post("/mvs", status_code=201)
def create_mvs(request: CreateMvsRequest):
    videos = get_videos_info(request.video_ids)
    channel_ids = list(set([video.snippet.channelId for video in videos]))
    channels = get_channels_info(channel_ids)
    with open_session() as session:
        id_to_channel = {}
        for channel_info in channels:
            channel = (
                session.query(Channel).filter_by(resource_id=channel_info.id).first()
            )
            if not channel:
                channel = Channel(
                    resource_id=channel_info.id,
                    title=channel_info.snippet.title,
                    thumbnail_url=get_highest_thumbnail_url(channel_info.snippet),
                    custom_url=channel_info.snippet.customUrl,
                )
                session.add(channel)
                session.flush()
            id_to_channel[channel_info.id] = channel

        for video_info in videos:
            video = session.query(Video).filter_by(resource_id=video_info.id).first()
            if not video:
                video = Video(
                    resource_id=video_info.id,
                    title=video_info.snippet.title,
                    channel_id=id_to_channel[video_info.snippet.channelId].id,
                    video_thumbnail=get_highest_thumbnail_url(video_info.snippet),
                )
                session.add(video)
                session.flush()
                clip = Clip(
                    name=video.title,
                    start_at=0,
                    end_at=parse_duration(
                        video_info.contentDetails.duration
                    ).total_seconds(),
                    video_id=video.id,
                )
                session.add(clip)
    return
