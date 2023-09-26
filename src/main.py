from src.auth import router as auth_router
from src.social import router as social_router

from fastapi import FastAPI


app = FastAPI(
    title="FastAPI Blog",
    description="Simple FastAPI Blog example",
)


app.include_router(auth_router)
app.include_router(social_router)
