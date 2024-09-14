from fastapi import APIRouter, Depends

from app.config import Settings, get_settings


router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "environment": settings.environment,
        "testing": settings.testing,
    }

@router.get("/lol/")
async def kek(settings: Settings = Depends(get_settings)):
    return {
        "ping": "kek",
        "environment": settings.environment,
        "testing": settings.testing,
    }
