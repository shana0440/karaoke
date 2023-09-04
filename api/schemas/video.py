from .base import BaseSchema
from .channel import ChannelSchema


class VideoSchema(BaseSchema):
    id: int
    resource_id: str
    title: str
    channel_id: int
    video_thumbnail: str
    channel: ChannelSchema
