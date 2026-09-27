from datetime import datetime

from remodel_engine.grain_resolution import (
    GrainVerdict,
    SourceRecordRef,
    classify_and_resolve,
)

TS_OLD = datetime(2020, 1, 1)
TS_MID = datetime(2021, 6, 1)
TS_NEW = datetime(2023, 1, 1)


def _row(
    old_key: str,
    old_table: str,
    ts: datetime,
    **fields: str,
) -> SourceRecordRef:
    return SourceRecordRef(
        old_key=old_key,
        old_table=old_table,
        field_values=dict(fields),
        timestamp=ts,
    )


def test_single_source_lossless_1_1():
    rows = [_row("k1", "t_a", TS_OLD, name="Alice", city="NY")]
    out = classify_and_resolve(rows, ["name", "city"])
    assert out["name"].verdict == GrainVerdict.LOSSLESS_1_1
    assert out["name"].resolved_values == {"name": "Alice"}
    assert out["city"].verdict == GrainVerdict.LOSSLESS_1_1


def test_pure_duplicate_no_conflict_lossless_bridge():
    rows = [
        _row("k1", "t_a", TS_OLD, name="Alice", city="NY"),
        _row("k2", "t_b", TS_NEW, name="Alice", city="NY"),
    ]
    out = classify_and_resolve(rows, ["name", "city"])
    assert out["name"].verdict == GrainVerdict.LOSSLESS_BRIDGE
    assert out["name"].resolved_values == {"name": "Alice"}
    assert out["city"].verdict == GrainVerdict.LOSSLESS_BRIDGE


def test_clear_recency_winner_lossy_resolved():
    rows = [
        _row("k1", "t_a", TS_OLD, name="Alice"),
        _row("k2", "t_b", TS_NEW, name="Alicia"),
    ]
    out = classify_and_resolve(rows, ["name"])
    assert out["name"].verdict == GrainVerdict.LOSSY_RESOLVED
    assert out["name"].resolved_values == {"name": "Alicia"}
    assert "most recent timestamp" in out["name"].reason


def test_tied_timestamp_ambiguous():
    rows = [
        _row("k1", "t_a", TS_MID, name="Alice"),
        _row("k2", "t_b", TS_MID, name="Alicia"),
    ]
    out = classify_and_resolve(rows, ["name"])
    assert out["name"].verdict == GrainVerdict.LOSSY_AMBIGUOUS
    assert out["name"].resolved_values is None
    assert "tied" in out["name"].reason.lower()


def test_three_source_mixed_verdicts():
    rows = [
        _row("k1", "t_a", TS_OLD, name="Alice", city="NY", tier="gold"),
        _row("k2", "t_b", TS_MID, name="Alice", city="NY", tier="gold"),
        _row("k3", "t_c", TS_NEW, name="Alicia", city="NY", tier="silver"),
    ]
    out = classify_and_resolve(rows, ["name", "city", "tier"])
    assert out["name"].verdict == GrainVerdict.LOSSY_RESOLVED
    assert out["name"].resolved_values == {"name": "Alicia"}
    assert out["city"].verdict == GrainVerdict.LOSSLESS_BRIDGE
    assert out["city"].resolved_values == {"city": "NY"}
    assert out["tier"].verdict == GrainVerdict.LOSSY_RESOLVED
    assert out["tier"].resolved_values == {"tier": "silver"}
