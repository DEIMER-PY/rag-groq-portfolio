from app.schemas.notebook import NotebookQueryResponse, NotebookUploadResponse
from app.services import notebook


def test_upload_document_chunks_embeds_and_inserts(mocker):
    fake_client = mocker.MagicMock()
    mocker.patch("app.services.notebook.get_supabase_client", return_value=fake_client)
    mocker.patch("app.services.notebook.embed_texts", return_value=[[0.1, 0.2], [0.3, 0.4]])
    mocker.patch(
        "app.services.notebook.chunk_markdown",
        return_value=[
            mocker.Mock(content="parte 1", chunk_index=0),
            mocker.Mock(content="parte 2", chunk_index=1),
        ],
    )

    result = notebook.upload_document("nb-1", "Mi documento", "contenido largo...")

    assert isinstance(result, NotebookUploadResponse)
    assert result.chunks_added == 2
    fake_client.table.assert_called_with("notebook_documents")
    inserted_rows = fake_client.table.return_value.insert.call_args[0][0]
    assert all(row["notebook_id"] == "nb-1" for row in inserted_rows)
    assert all(row["source_title"] == "Mi documento" for row in inserted_rows)


def test_upload_document_with_no_chunks_returns_zero(mocker):
    mocker.patch("app.services.notebook.get_supabase_client", return_value=mocker.MagicMock())
    mocker.patch("app.services.notebook.chunk_markdown", return_value=[])

    result = notebook.upload_document("nb-1", "Vacío", "   ")

    assert result.chunks_added == 0


def test_query_notebook_scopes_retrieval_to_notebook_id(mocker):
    fake_client = mocker.MagicMock()
    fake_client.rpc.return_value.execute.return_value.data = [
        {"content": "dato relevante", "source_title": "doc.txt", "chunk_index": 0, "similarity": 0.9}
    ]
    mocker.patch("app.services.notebook.get_supabase_client", return_value=fake_client)
    mocker.patch("app.services.notebook.embed_query", return_value=[0.1, 0.2])
    mocker.patch("app.services.notebook.generate_answer", return_value="Respuesta basada en el documento")

    result = notebook.query_notebook("nb-1", "¿qué dice el documento?")

    fake_client.rpc.assert_called_once()
    call_args = fake_client.rpc.call_args[0]
    assert call_args[0] == "match_notebook_documents"
    assert call_args[1]["p_notebook_id"] == "nb-1"
    assert isinstance(result, NotebookQueryResponse)
    assert result.sources == ["doc.txt"]


def test_query_notebook_with_no_documents_still_answers_gracefully(mocker):
    fake_client = mocker.MagicMock()
    fake_client.rpc.return_value.execute.return_value.data = []
    mocker.patch("app.services.notebook.get_supabase_client", return_value=fake_client)
    mocker.patch("app.services.notebook.embed_query", return_value=[0.1, 0.2])
    mock_generate = mocker.patch(
        "app.services.notebook.generate_answer", return_value="El documento no menciona eso"
    )

    result = notebook.query_notebook("nb-empty", "¿qué dice el documento?")

    assert result.sources == []
    prompt_arg = mock_generate.call_args[0][0]
    assert "todavía no tiene documentos" in prompt_arg
