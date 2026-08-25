from duckduckgo_search import DDGS

WEB_SIGNAL_PATTERN_WORDS = (
    "actual",
    "reciente",
    "última versión",
    "ultima version",
    "novedades",
    "hoy",
    "2025",
    "2026",
)


def has_recency_signal(query: str) -> bool:
    lowered = query.lower()
    return any(word in lowered for word in WEB_SIGNAL_PATTERN_WORDS)


def search_web(query: str, max_results: int = 3) -> list[dict]:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception:
        return []

    return [
        {"url": r.get("href", ""), "title": r.get("title", ""), "snippet": r.get("body", "")}
        for r in results
    ]
