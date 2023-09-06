from fastapi import APIRouter
from sqlalchemy import or_
from database.session import open_session
from models import Channel, Video, Clip
from schemas import ChannelSchema, ChannelWithBannerSchema
from query.pagination import paginate
from services.youtube import get_channel_banner_url

router = APIRouter()


@router.get("/channels")
def get_channels(limit: int = 20, offset: int = 0):
    with open_session() as session:
        query = session.query(Channel).order_by(Channel.created_at.desc())
        return paginate(query, limit, offset, ChannelSchema)


@router.get("/channels/search")
def search_channels(q: str, limit: int = 20, offset: int = 0):
    with open_session() as session:
        search = f"%{q}%"
        query = (
            session.query(Channel)
            .join(Channel.videos)
            .join(Video.clips)
            .filter(
                or_(
                    Channel.title.like(search),
                    Channel.custom_url.like(search),
                    Channel.videos.any(Video.clips.any(Clip.name.like(search))),
                )
            )
            .group_by(Channel.id)
        )
        return paginate(query, limit, offset, ChannelSchema)


@router.get("/channels/{channel_id}")
def get_channel(channel_id: int):
    with open_session() as session:
        channel = session.query(Channel).filter_by(id=channel_id).first()
        banner_url = get_channel_banner_url(channel_id=channel.resource_id)
        channel.banner_url = banner_url
        return ChannelWithBannerSchema.model_validate(channel)
