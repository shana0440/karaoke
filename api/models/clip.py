from sqlalchemy import Column, Integer, String, DateTime

from .base import Base, TimestampColumns


class Clip(Base, TimestampColumns):
    __tablename__ = 'clips'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stream_id = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
