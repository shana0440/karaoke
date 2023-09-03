from sqlalchemy import Column, Integer, String

from .base import Base, TimestampColumns


class Video(Base, TimestampColumns):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    resource_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    channel_id = Column(Integer, nullable=False)
    video_thumbnail = Column(String, nullable=False)
