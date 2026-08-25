from app.services import retrieval


def test_search_calls_match_documents_rpc_with_expected_params(mocker):
    fake_client = mocker.MagicMock()
    fake_client.rpc.return_value.execute.return_value.data = [
        {"source_file": "ia-rag/rag-arquitectura.md", "similarity": 0.8, "content": "..."}
    ]
    mocker.patch("app.services.retrieval.get_supabase_client", return_value=fake_client)

    results = retrieval.search([0.1, 0.2, 0.3], match_count=3, filter_module="ia-rag")

    fake_client.rpc.assert_called_once_with(
        "match_documents",
        {
            "query_embedding": [0.1, 0.2, 0.3],
            "match_count": 3,
            "filter_module": "ia-rag",
            "min_similarity": mocker.ANY,
        },
    )
    assert results[0]["source_file"] == "ia-rag/rag-arquitectura.md"


def test_search_returns_empty_list_when_supabase_not_configured(mocker):
    mocker.patch("app.services.retrieval.get_supabase_client", return_value=None)

    assert retrieval.search([0.1, 0.2, 0.3]) == []
