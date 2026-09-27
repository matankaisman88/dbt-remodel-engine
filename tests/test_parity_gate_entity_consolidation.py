from remodel_engine.parity_gate import verify_no_physical_data_loss


def test_verify_no_physical_data_loss_passes_when_all_keys_present():
    raw_rows = [
        {"old_key": "1", "old_table": "a"},
        {"old_key": "2", "old_table": "b"},
    ]
    audit_rows = [
        {"old_key": "1", "old_table": "a", "conflict_field": "name"},
        {"old_key": "2", "old_table": "b", "conflict_field": "name"},
    ]
    result = verify_no_physical_data_loss(raw_rows, audit_rows)
    assert result.status == "pass"


def test_verify_no_physical_data_loss_fails_when_key_missing():
    raw_rows = [{"old_key": "1", "old_table": "a"}]
    audit_rows = []
    result = verify_no_physical_data_loss(raw_rows, audit_rows)
    assert result.status == "fail"
    assert "missing" in (result.error or "")
