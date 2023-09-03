from sqlalchemy import Column, Integer, String

from .base import Base, TimestampColumns


class Channel(Base, TimestampColumns):
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    custom_url = Column(String, nullable=False, unique=True)
    resource_id = Column(String, nullable=False, unique=True)
