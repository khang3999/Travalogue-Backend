from fastapi import APIRouter

from app.database import firebase_config

router = APIRouter(prefix="/test", tags=["tests"])

@router.get("/")
async def test_connection():
    return firebase_config.check_connection()
