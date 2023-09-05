from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from database.session import open_session
from models import Video, Clip, Channel
from services.youtube import (
    get_channel_info,
    get_video_info,
    extract_video_id_from_url,
    get_highest_thumbnail_url,
)
from schemas.clip import ClipSchema
from query.pagination import paginate

router = APIRouter()


class ClipEntity(BaseModel):
    name: str
    start_at: float
    end_at: float


class CreateClipsRequest(BaseModel):
    stream_url: str
    clips: List[ClipEntity]


@router.post("/clips", status_code=201)
def create_clips(body: CreateClipsRequest):
    id = extract_video_id_from_url(body.stream_url)
    video_info = get_video_info(id)
    channel_info = get_channel_info(video_info.channelId)
    with open_session() as session:
        channel = (
            session.query(Channel).filter_by(resource_id=video_info.channelId).first()
        )
        if channel is None:
            channel = Channel(
                resource_id=video_info.channelId,
                title=channel_info.title,
                thumbnail_url=get_highest_thumbnail_url(channel_info),
                custom_url=channel_info.customUrl,
            )
            session.add(channel)
            session.flush()

        video = Video(
            resource_id=id,
            title=video_info.title,
            channel_id=channel.id,
            video_thumbnail=get_highest_thumbnail_url(video_info),
        )
        session.add(video)
        session.flush()

        for s in body.clips:
            clip = Clip(
                name=s.name, start_at=s.start_at, end_at=s.end_at, video_id=video.id
            )
            session.add(clip)

    return


@router.get("/clips")
def get_clips(limit: int = 20, offset: int = 0):
    with open_session() as session:
        query = session.query(Clip).order_by(Clip.created_at.desc())
        return paginate(query, limit, offset, ClipSchema)


@router.get("/channels/{channel_id}/clips")
def get_channel_clips(channel_id: int, limit: int = 20, offset: int = 0):
    with open_session() as session:
        query = session.query(Clip).join(Clip.video).filter_by(channel_id=channel_id)
        return paginate(query, limit, offset, ClipSchema)
