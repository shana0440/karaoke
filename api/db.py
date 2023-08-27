from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///karaoke.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stream_id = Column(Integer)
    start_at = Column(Integer)
    end_at = Column(Integer)

class Stream(Base):
    __tablename__ = 'streams'
    id = Column(String, primary_key=True)
    url = Column(String)

