from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from database.session import open_session

from models import Video, Clip, Channel
from services.youtube import get_channel_info, get_video_info, extract_video_id_from_url

router = APIRouter()

class ClipEntity(BaseModel):
    name: str
    start_at: int
    end_at: int


class CreateClipsRequest(BaseModel):
    stream_url: str
    clips: List[ClipEntity]

@router.post("/clips", status_code=201)
def create_clips(body: CreateClipsRequest):
    id = extract_video_id_from_url(body.stream_url)
    video_info = get_video_info(id)
    channel_info = get_channel_info(video_info.channelId)
    with open_session() as session:
        channel = session.query(Channel).filter_by(resource_id=video_info.channelId).first()
        if channel is None:
            channel = Channel(
                resource_id=video_info.channelId, 
                title=channel_info.title,
                thumbnail_url=channel_info.thumbnails.default.url,
                custom_url=channel_info.customUrl,
            )
            session.add(channel)
            session.flush()

        video = Video(
            resource_id=id, 
            title=video_info.title, 
            channel_id=channel.id,
            video_thumbnail=video_info.thumbnails.default.url
        )
        session.add(video)
        session.flush()
        
        for s in body.clips:
            clip = Clip(name=s.name, start_at=s.start_at, end_at=s.end_at, video_id=video.id)
            session.add(clip)

    return
    