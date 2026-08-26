from app.core.prompts import NOTEBOOK_SYSTEM_PROMPT, build_notebook_prompt
from app.db.supabase_client import get_supabase_client
from app.schemas.notebook import NotebookQueryResponse, NotebookSource, NotebookUploadResponse
from app.services.chunking import chunk_markdown
from app.services.embeddings import embed_query, embed_texts
from app.services.groq_client import generate_answer

NOTEBOOK_CHUNK_SIZE = 800
NOTEBOOK_CHUNK_OVERLAP = 100
NOTEBOOK_MATCH_COUNT = 6


def upload_document(notebook_id: str, title: str, content: str) -> NotebookUploadResponse:
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase no está configurado")

    chunks = chunk_markdown(content, chunk_size=NOTEBOOK_CHUNK_SIZE, chunk_overlap=NOTEBOOK_CHUNK_OVERLAP)
    if not chunks:
        return NotebookUploadResponse(title=title, chunks_added=0)

    embeddings = embed_texts([c.content for c in chunks])
    rows = [
        {
            "notebook_id": notebook_id,
            "content": chunk.content,
            "embedding": embedding,
            "source_title": title,
            "chunk_index": chunk.chunk_index,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.table("notebook_documents").insert(rows).execute()

    return NotebookUploadResponse(title=title, chunks_added=len(rows))


def list_sources(notebook_id: str) -> list[NotebookSource]:
    client = get_supabase_client()
    if client is None:
        return []

    rows = client.rpc("notebook_sources", {"p_notebook_id": notebook_id}).execute().data or []
    return [NotebookSource(**row) for row in rows]


def query_notebook(notebook_id: str, query: str) -> NotebookQueryResponse:
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase no está configurado")

    query_embedding = embed_query(query)
    result = client.rpc(
        "match_notebook_documents",
        {"query_embedding": query_embedding, "p_notebook_id": notebook_id, "match_count": NOTEBOOK_MATCH_COUNT},
    ).execute()
    chunks = result.data or []

    prompt = build_notebook_prompt(query, chunks)
    answer = generate_answer(prompt, system_prompt=NOTEBOOK_SYSTEM_PROMPT)

    sources = sorted({c["source_title"] for c in chunks})
    return NotebookQueryResponse(answer=answer, sources=sources)
