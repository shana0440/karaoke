from .base import BaseSchema


class ChannelSchema(BaseSchema):
    id: int
    title: str
    thumbnail_url: str
    custom_url: str
    resource_id: str

    class Config:
        orm_mode = True


class ChannelWithBannerSchema(ChannelSchema):
    banner_url: str
