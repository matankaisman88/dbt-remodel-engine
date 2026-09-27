"""Regression guard for Febrl duplicate-cluster conflict detection rate."""

from __future__ import annotations

import json
from pathlib import Path

FIXTURE = (
    Path(__file__).parent / "fixtures" / "entity_consolidation" / "febrl_conflict_sample.json"
)


def measure_cluster_conflict_rate(
    clusters: list[dict],
    conflict_fields: list[str],
) -> float:
    """Share of multi-row clusters with at least one conflicting conflict_field."""
    multi = [c for c in clusters if len(c.get("rows") or []) > 1]
    if not multi:
        return 0.0
    with_conflict = 0
    for cluster in multi:
        rows = cluster["rows"]
        if any(
            len({str(r["field_values"][field]) for r in rows}) > 1
            for field in conflict_fields
        ):
            with_conflict += 1
    return with_conflict / len(multi)


def test_febrl_conflict_rate_within_expected_band():
    data = json.loads(FIXTURE.read_text())
    measured = measure_cluster_conflict_rate(data["clusters"], data["conflict_fields"])
    reference = float(data.get("reference_conflict_rate", 0.943))
    tolerance = 0.05
    assert reference - tolerance <= measured <= reference + tolerance, (
        f"conflict rate {measured:.4f} outside band around {reference:.4f}"
    )
