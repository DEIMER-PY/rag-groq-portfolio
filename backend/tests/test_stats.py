from fastapi.testclient import TestClient

from app.main import app
from app.services import stats

client = TestClient(app)


def test_get_stats_shape(mocker):
    fake_client = mocker.MagicMock()
    fake_client.rpc.return_value.execute.return_value.data = [
        {"module": "backend", "chunk_count": 39},
        {"module": "frontend", "chunk_count": 31},
    ]

    def rpc_side_effect(name, params):
        result = mocker.MagicMock()
        if name == "documents_by_module":
            result.execute.return_value.data = [
                {"module": "backend", "chunk_count": 39},
                {"module": "frontend", "chunk_count": 31},
            ]
        elif name == "query_log_summary":
            result.execute.return_value.data = [
                {"total_queries": 10, "in_scope_queries": 8, "web_fallback_queries": 2}
            ]
        return result

    fake_client.rpc.side_effect = rpc_side_effect
    fake_client.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value.data = [
        {"query": "que es un closure", "in_scope": True, "used_web_fallback": False, "created_at": "2026-01-01T00:00:00Z"}
    ]
    mocker.patch("app.services.stats.get_supabase_client", return_value=fake_client)

    result = stats.get_stats()

    assert result["total_documents"] == 70
    assert result["documents_by_module"] == [
        {"module": "backend", "chunk_count": 39},
        {"module": "frontend", "chunk_count": 31},
    ]
    assert result["total_queries"] == 10
    assert result["in_scope_queries"] == 8
    assert result["web_fallback_queries"] == 2
    assert len(result["recent_queries"]) == 1


def test_get_stats_returns_zeros_when_supabase_not_configured(mocker):
    mocker.patch("app.services.stats.get_supabase_client", return_value=None)

    result = stats.get_stats()

    assert result["total_documents"] == 0
    assert result["recent_queries"] == []


def test_stats_endpoint_returns_200(mocker):
    mocker.patch(
        "app.api.routes_stats.get_stats",
        return_value={
            "total_documents": 0,
            "documents_by_module": [],
            "total_queries": 0,
            "in_scope_queries": 0,
            "web_fallback_queries": 0,
            "recent_queries": [],
        },
    )

    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json()["total_documents"] == 0
