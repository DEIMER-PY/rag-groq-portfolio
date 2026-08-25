from app.config import settings
from app.db.supabase_client import get_supabase_client


def search(query_embedding: list[float], match_count: int | None = None, filter_module: str | None = None) -> list[dict]:
    client = get_supabase_client()
    if client is None:
        return []

    response = client.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": match_count or settings.match_count,
            "filter_module": filter_module,
            "min_similarity": settings.min_similarity,
        },
    ).execute()

    return response.data or []
