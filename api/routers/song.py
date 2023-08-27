from fastapi import APIRouter
from pydantic import BaseModel
import utils
from db import session, Stream, Song
from typing import List

router = APIRouter()

class SongEntity(BaseModel):
    name: str
    start_at: int
    end_at: int


class CreateSongsRequest(BaseModel):
    stream_url: str
    songs: List[SongEntity]

@router.post("/songs", status_code=201)
def create_songs(body: CreateSongsRequest):
    id = utils.extract_youtube_id(body.stream_url)
    with session.begin():
        new_stream = Stream(id=id, url=body.stream_url)
        session.add(new_stream)
        session.flush()
        
        for s in body.songs:
            new_song = Song(name=s.name, start_at=s.start_at, end_at=s.end_at, stream_id=new_stream.id)
            session.add(new_song)
        session.commit()

    return {}
    

@router.get("/{id}/songs")
def get_songs_by_id(id: str):
    songs = session.query(Song).filter(Song.stream_id == id).all()
    return songs
