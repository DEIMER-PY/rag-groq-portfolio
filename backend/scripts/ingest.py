"""CLI de ingesta: lee corpus/**/*.md, los chunkea, genera embeddings y los
sube a la tabla `documents` de Supabase. Ver AGENTS.md para el flujo completo.

Uso (desde la carpeta backend/, con el venv activado):
    python -m scripts.ingest
    python -m scripts.ingest --only ia-rag
"""

import argparse
from pathlib import Path

from app.db.supabase_client import get_supabase_client
from app.services.chunking import chunk_markdown
from app.services.embeddings import embed_texts

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "corpus"
BATCH_SIZE = 50


def iter_corpus_files(only_module: str | None) -> list[Path]:
    files = sorted(CORPUS_DIR.rglob("*.md"))
    if only_module:
        files = [f for f in files if f.relative_to(CORPUS_DIR).parts[0] == only_module]
    return files


def ingest_file(path: Path) -> int:
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase no está configurado (revisa SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY)")

    relative_path = path.relative_to(CORPUS_DIR)
    source_file = relative_path.as_posix()
    module = relative_path.parts[0]

    text = path.read_text(encoding="utf-8")
    chunks = chunk_markdown(text)
    if not chunks:
        print(f"  (sin contenido chunkeable, se omite) {source_file}")
        return 0

    embeddings = embed_texts([c.content for c in chunks])

    rows = [
        {
            "content": chunk.content,
            "embedding": embedding,
            "source_file": source_file,
            "module": module,
            "section_title": chunk.section_title,
            "chunk_index": chunk.chunk_index,
            "token_count": len(chunk.content) // 4,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.table("documents").delete().eq("source_file", source_file).execute()
    for i in range(0, len(rows), BATCH_SIZE):
        client.table("documents").insert(rows[i : i + BATCH_SIZE]).execute()

    print(f"  {source_file}: {len(rows)} chunks")
    return len(rows)


def main() -> None:
    global CORPUS_DIR

    parser = argparse.ArgumentParser(description="Ingesta el corpus Markdown en Supabase pgvector")
    parser.add_argument("--path", default=str(CORPUS_DIR), help="Ruta al corpus (default: corpus/)")
    parser.add_argument("--only", default=None, help="Ingerir solo un módulo (ej. ia-rag)")
    args = parser.parse_args()

    CORPUS_DIR = Path(args.path).resolve()

    files = iter_corpus_files(args.only)
    if not files:
        print("No se encontraron documentos .md para ingerir.")
        return

    print(f"Ingiriendo {len(files)} documento(s)...")
    total = sum(ingest_file(path) for path in files)
    print(f"Listo. {total} chunks insertados en total.")


if __name__ == "__main__":
    main()
