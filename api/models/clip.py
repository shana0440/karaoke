from sqlalchemy import Column, Integer, String, DateTime

from .base import Base, TimestampColumns


class Clip(Base, TimestampColumns):
    __tablename__ = 'clips'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    video_id = Column(Integer, nullable=False)
    start_at = Column(Integer, nullable=False)
    end_at = Column(Integer, nullable=False)
