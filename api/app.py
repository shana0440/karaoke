from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers import predict, clip, youtube, channel, video, mv

app = FastAPI()

api = APIRouter(prefix="/api")

api.include_router(predict.router)
api.include_router(clip.router)
api.include_router(youtube.router)
api.include_router(channel.router)
api.include_router(video.router)
api.include_router(mv.router)

app.include_router(api)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
