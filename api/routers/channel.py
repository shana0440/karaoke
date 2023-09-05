from fastapi import APIRouter
from database.session import open_session
from models import Channel
from schemas import ChannelSchema, ChannelWithBannerSchema
from query.pagination import paginate
from services.youtube import get_channel_banner_url

router = APIRouter()


@router.get("/channels")
def get_channels(limit: int = 20, offset: int = 0):
    with open_session() as session:
        query = session.query(Channel).order_by(Channel.created_at.desc())
        return paginate(query, limit, offset, ChannelSchema)


@router.get("/channels/{channel_id}")
def get_channel(channel_id: int):
    with open_session() as session:
        channel = session.query(Channel).filter_by(id=channel_id).first()
        banner_url = get_channel_banner_url(channel_id=channel.resource_id)
        channel.banner_url = banner_url
        return ChannelWithBannerSchema.model_validate(channel)
