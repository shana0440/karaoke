from .base import BaseSchema
from .video import VideoSchema


class ClipSchema(BaseSchema):
    id: int
    name: str
    video_id: int
    start_at: float
    end_at: float
    video: VideoSchema

    class Config:
        orm_mode = True
