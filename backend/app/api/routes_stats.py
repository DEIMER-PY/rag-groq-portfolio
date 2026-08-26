from fastapi import APIRouter

from app.services.stats import get_stats

router = APIRouter()


@router.get("/stats")
async def stats() -> dict:
    return get_stats()
