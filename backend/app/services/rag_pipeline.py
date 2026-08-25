from app.core.prompts import build_user_prompt
from app.schemas.query import QueryResponse, SourceRef
from app.services import guardrails, retrieval, web_search
from app.services.embeddings import embed_query
from app.services.groq_client import generate_answer


def answer_query(query: str) -> QueryResponse:
    guardrails.validate_input_length(query)

    if not guardrails.is_in_scope(query):
        return QueryResponse(answer=guardrails.out_of_scope_response(), sources=[], used_web_fallback=False)

    query_embedding = embed_query(query)
    kb_results = retrieval.search(query_embedding)

    max_similarity = max((r.get("similarity", 0) for r in kb_results), default=0)
    needs_web_fallback = max_similarity < 0.35 or web_search.has_recency_signal(query)

    web_results = web_search.search_web(query) if needs_web_fallback else []
    used_web_fallback = bool(web_results)

    user_prompt = build_user_prompt(query, kb_results, web_results)
    answer = generate_answer(user_prompt)

    sources = [
        SourceRef(
            source_type="kb",
            title=r.get("section_title") or r["source_file"],
            similarity=r.get("similarity"),
            source_file=r["source_file"],
        )
        for r in kb_results
    ] + [
        SourceRef(source_type="web", title=r["title"], url=r["url"])
        for r in web_results
    ]

    return QueryResponse(answer=answer, sources=sources, used_web_fallback=used_web_fallback)
