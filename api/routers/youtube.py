from fastapi import APIRouter

from services.youtube import get_video_most_like_comment

router = APIRouter()

@router.get("/videos/{video_id}/most-like-comment")
async def get_most_like_comment(video_id: str):
    comment = get_video_most_like_comment(video_id)
    return comment.snippet.topLevelComment.snippet