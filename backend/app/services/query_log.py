import logging

from app.db.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def log_query(query: str, in_scope: bool, max_similarity: float | None, used_web_fallback: bool) -> None:
    """Best-effort logging for the dashboard. Never raises: a logging failure must not
    break answering the user's question."""
    client = get_supabase_client()
    if client is None:
        return

    try:
        client.table("query_logs").insert(
            {
                "query": query[:500],
                "in_scope": in_scope,
                "max_similarity": max_similarity,
                "used_web_fallback": used_web_fallback,
            }
        ).execute()
    except Exception:
        logger.warning("Failed to log query for dashboard stats", exc_info=True)
