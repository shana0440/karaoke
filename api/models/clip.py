from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampColumns


class Clip(Base, TimestampColumns):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    start_at = Column(Float, nullable=False)
    end_at = Column(Float, nullable=False)

    video = relationship("Video", back_populates="clips", lazy="joined")
