from sqlalchemy import Column, Integer, String

from .base import Base, TimestampColumns


class Streamer(Base, TimestampColumns):
    __tablename__ = 'streamers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False)
    resource_id = Column(Integer, nullable=False, unique=True)
