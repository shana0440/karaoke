from .base import BaseSchema
from .video import VideoSchema


class ClipSchema(BaseSchema):
    id: int
    name: str
    video_id: int
    start_at: int
    end_at: int
    video: VideoSchema
