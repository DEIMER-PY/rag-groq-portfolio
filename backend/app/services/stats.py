from app.db.supabase_client import get_supabase_client


def get_stats() -> dict:
    client = get_supabase_client()
    if client is None:
        return {
            "total_documents": 0,
            "documents_by_module": [],
            "total_queries": 0,
            "in_scope_queries": 0,
            "web_fallback_queries": 0,
            "recent_queries": [],
        }

    by_module = client.rpc("documents_by_module", {}).execute().data or []
    total_documents = sum(row["chunk_count"] for row in by_module)

    summary_rows = client.rpc("query_log_summary", {}).execute().data or []
    summary = summary_rows[0] if summary_rows else {}

    recent = (
        client.table("query_logs")
        .select("query,in_scope,used_web_fallback,created_at")
        .order("created_at", desc=True)
        .limit(10)
        .execute()
        .data
        or []
    )

    return {
        "total_documents": total_documents,
        "documents_by_module": by_module,
        "total_queries": summary.get("total_queries", 0),
        "in_scope_queries": summary.get("in_scope_queries", 0),
        "web_fallback_queries": summary.get("web_fallback_queries", 0),
        "recent_queries": recent,
    }
