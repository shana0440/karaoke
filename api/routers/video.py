from fastapi import APIRouter
from sqlalchemy import or_
from database.session import open_session
from models import Video, Clip
from schemas import VideoSchema
from query.pagination import paginate

router = APIRouter()


@router.get("/videos/search")
def search_videos(q: str, limit: int = 20, offset: int = 0):
    with open_session() as session:
        search = f"%{q}%"
        query = (
            session.query(Video)
            .join(Video.clips)
            .filter(
                or_(
                    Video.title.like(search),
                    Video.clips.any(Clip.name.like(search)),
                )
            )
            .group_by(Video.id)
        )
        return paginate(query, limit, offset, VideoSchema)


@router.get("/videos/{video_id}")
def get_video(video_id: int):
    with open_session() as session:
        video = session.query(Video).filter_by(id=video_id).first()
        return VideoSchema.model_validate(video)
