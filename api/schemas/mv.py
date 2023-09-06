from pydantic import BaseModel


class MvSchema(BaseModel):
    id: str
    channel_id: str
    thumbnail_url: str
    title: str
    channel_title: str
    duration: float
