from sqlalchemy import Column, Integer, String

from .base import Base, TimestampColumns


class Stream(Base, TimestampColumns):
    __tablename__ = 'streams'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    streamer_id = Column(Integer, nullable=False)
