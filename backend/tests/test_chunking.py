from app.services.chunking import chunk_markdown


def test_chunk_respects_max_size():
    text = "## Intro\n" + ("palabra " * 400)
    chunks = chunk_markdown(text, chunk_size=200, chunk_overlap=20)

    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.content) <= 200 + 20  # tolerancia por el overlap agregado


def test_chunk_tags_section_title_from_headings():
    text = (
        "## Primera sección\n"
        "Contenido de la primera sección.\n\n"
        "### Subsección\n"
        "Contenido de la subsección.\n"
    )
    chunks = chunk_markdown(text, chunk_size=1000, chunk_overlap=0)

    titles = {c.section_title for c in chunks}
    assert "Primera sección" in titles
    assert "Subsección" in titles


def test_chunk_index_is_sequential():
    text = "## A\n" + ("x " * 300) + "\n## B\n" + ("y " * 300)
    chunks = chunk_markdown(text, chunk_size=100, chunk_overlap=10)

    indices = [c.chunk_index for c in chunks]
    assert indices == list(range(len(chunks)))


def test_chunk_overlap_preserves_boundary_context():
    text = "## Sección\n" + ("palabra " * 300)
    chunks = chunk_markdown(text, chunk_size=100, chunk_overlap=30)

    # el final del primer chunk debe reaparecer al inicio del segundo (overlap real)
    tail_of_first = chunks[0].content[-20:]
    assert tail_of_first in chunks[1].content


def test_empty_document_produces_no_chunks():
    assert chunk_markdown("   \n\n  ") == []
