from app.schemas.query import QueryResponse
from app.services import rag_pipeline


def _mock_common(mocker, kb_results, is_in_scope=True):
    mocker.patch("app.services.rag_pipeline.guardrails.is_in_scope", return_value=is_in_scope)
    mocker.patch("app.services.rag_pipeline.embed_query", return_value=[0.1, 0.2, 0.3])
    mocker.patch("app.services.rag_pipeline.retrieval.search", return_value=kb_results)
    mocker.patch("app.services.rag_pipeline.query_log.log_query")
    mocker.patch("app.services.rag_pipeline.generate_answer", return_value="Respuesta generada")


def test_out_of_scope_query_short_circuits_without_calling_llm(mocker):
    _mock_common(mocker, kb_results=[], is_in_scope=False)
    mock_generate = mocker.patch("app.services.rag_pipeline.generate_answer")

    result = rag_pipeline.answer_query("¿cuál es la mejor receta de pizza?")

    assert isinstance(result, QueryResponse)
    assert "Solo puedo ayudarte" in result.answer
    assert result.sources == []
    assert result.used_web_fallback is False
    mock_generate.assert_not_called()


def test_high_similarity_kb_result_does_not_trigger_web_fallback(mocker):
    kb_results = [
        {"source_file": "ia-rag/rag-arquitectura.md", "section_title": "Intro", "similarity": 0.8, "content": "..."}
    ]
    _mock_common(mocker, kb_results=kb_results)
    mock_web = mocker.patch("app.services.rag_pipeline.web_search.search_web")
    mocker.patch("app.services.rag_pipeline.web_search.has_recency_signal", return_value=False)

    result = rag_pipeline.answer_query("¿qué es RAG?")

    mock_web.assert_not_called()
    assert result.used_web_fallback is False
    assert result.sources[0].source_type == "kb"


def test_low_similarity_triggers_web_fallback(mocker):
    kb_results = [{"source_file": "x.md", "section_title": None, "similarity": 0.1, "content": "..."}]
    _mock_common(mocker, kb_results=kb_results)
    mocker.patch("app.services.rag_pipeline.web_search.has_recency_signal", return_value=False)
    mocker.patch(
        "app.services.rag_pipeline.web_search.search_web",
        return_value=[{"url": "https://example.com", "title": "Ejemplo", "snippet": "..."}],
    )

    result = rag_pipeline.answer_query("¿qué framework es tendencia ahora mismo?")

    assert result.used_web_fallback is True
    source_types = {s.source_type for s in result.sources}
    assert source_types == {"kb", "web"}


def test_recency_signal_triggers_web_fallback_even_with_high_similarity(mocker):
    kb_results = [{"source_file": "x.md", "section_title": None, "similarity": 0.9, "content": "..."}]
    _mock_common(mocker, kb_results=kb_results)
    mocker.patch("app.services.rag_pipeline.web_search.has_recency_signal", return_value=True)
    mock_web = mocker.patch(
        "app.services.rag_pipeline.web_search.search_web",
        return_value=[{"url": "https://example.com", "title": "Ejemplo", "snippet": "..."}],
    )

    result = rag_pipeline.answer_query("¿cuál es la última versión de React en 2026?")

    mock_web.assert_called_once()
    assert result.used_web_fallback is True


def test_all_sources_have_source_type():
    from app.schemas.query import SourceRef

    ref = SourceRef(source_type="kb", title="x", source_file="x.md")
    assert ref.source_type in {"kb", "web"}
