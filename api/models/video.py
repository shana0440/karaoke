from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampColumns


class Video(Base, TimestampColumns):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    resource_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    video_thumbnail = Column(String, nullable=False)

    clips = relationship("Clip", back_populates="video", lazy="joined")
    channel = relationship("Channel", back_populates="videos", lazy="joined")
