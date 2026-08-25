from fastapi import APIRouter

from app.config import settings
from app.db.supabase_client import get_supabase_client

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "groq_configured": bool(settings.groq_api_key),
        "supabase_configured": get_supabase_client() is not None,
    }
