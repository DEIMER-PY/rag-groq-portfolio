from scripts.ingest import iter_corpus_files


def test_iter_corpus_files_filters_by_module(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    (corpus / "frontend").mkdir(parents=True)
    (corpus / "backend").mkdir(parents=True)
    (corpus / "frontend" / "a.md").write_text("# A", encoding="utf-8")
    (corpus / "backend" / "b.md").write_text("# B", encoding="utf-8")

    import scripts.ingest as ingest_module

    monkeypatch.setattr(ingest_module, "CORPUS_DIR", corpus)

    all_files = iter_corpus_files(None)
    assert len(all_files) == 2

    frontend_only = iter_corpus_files("frontend")
    assert len(frontend_only) == 1
    assert frontend_only[0].name == "a.md"
