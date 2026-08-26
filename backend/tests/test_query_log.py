from app.services import query_log


def test_log_query_inserts_expected_row(mocker):
    fake_client = mocker.MagicMock()
    mocker.patch("app.services.query_log.get_supabase_client", return_value=fake_client)

    query_log.log_query("que es SOLID", in_scope=True, max_similarity=0.72, used_web_fallback=False)

    fake_client.table.assert_called_once_with("query_logs")
    inserted = fake_client.table.return_value.insert.call_args[0][0]
    assert inserted["query"] == "que es SOLID"
    assert inserted["in_scope"] is True
    assert inserted["max_similarity"] == 0.72
    assert inserted["used_web_fallback"] is False


def test_log_query_never_raises_when_supabase_fails(mocker):
    fake_client = mocker.MagicMock()
    fake_client.table.side_effect = RuntimeError("boom")
    mocker.patch("app.services.query_log.get_supabase_client", return_value=fake_client)

    query_log.log_query("que es SOLID", in_scope=True, max_similarity=0.72, used_web_fallback=False)  # no raise


def test_log_query_noop_when_supabase_not_configured(mocker):
    mocker.patch("app.services.query_log.get_supabase_client", return_value=None)

    query_log.log_query("que es SOLID", in_scope=True, max_similarity=0.72, used_web_fallback=False)  # no raise
