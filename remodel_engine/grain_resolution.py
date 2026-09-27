"""Hardcoded most-recent-timestamp-wins survivorship for entity consolidation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class GrainVerdict(str, Enum):
    LOSSLESS_1_1 = "LOSSLESS_1_1"
    LOSSLESS_BRIDGE = "LOSSLESS_BRIDGE"
    LOSSY_RESOLVED = "LOSSY_RESOLVED"
    LOSSY_AMBIGUOUS = "LOSSY_AMBIGUOUS"


@dataclass
class SourceRecordRef:
    old_key: str
    old_table: str
    field_values: dict[str, Any]
    timestamp: datetime


@dataclass
class GrainResolution:
    verdict: GrainVerdict
    resolved_values: dict[str, Any] | None
    reason: str


def _field_values(rows: list[SourceRecordRef], field: str) -> list[Any]:
    return [r.field_values[field] for r in rows if field in r.field_values]


def classify_and_resolve(
    rows: list[SourceRecordRef], conflict_fields: list[str]
) -> dict[str, GrainResolution]:
    """One resolution per conflict field. Hardcoded rule: most-recent-timestamp-wins.

    No config, no pluggable rules — extend only when a second real case demands it.
    """
    out: dict[str, GrainResolution] = {}
    for field in conflict_fields:
        if not rows:
            out[field] = GrainResolution(
                verdict=GrainVerdict.LOSSLESS_1_1,
                resolved_values=None,
                reason="no source rows",
            )
            continue

        values = _field_values(rows, field)
        if len(rows) == 1:
            val = values[0] if values else None
            out[field] = GrainResolution(
                verdict=GrainVerdict.LOSSLESS_1_1,
                resolved_values={field: val},
                reason="single source record",
            )
            continue

        if not values:
            out[field] = GrainResolution(
                verdict=GrainVerdict.LOSSLESS_BRIDGE,
                resolved_values={field: None},
                reason="field absent on all sources",
            )
            continue

        distinct = {str(v) for v in values}
        if len(distinct) == 1:
            out[field] = GrainResolution(
                verdict=GrainVerdict.LOSSLESS_BRIDGE,
                resolved_values={field: values[0]},
                reason="all sources agree",
            )
            continue

        max_ts = max(r.timestamp for r in rows)
        at_max = [r for r in rows if r.timestamp == max_ts]
        winner_values = {str(r.field_values.get(field)) for r in at_max if field in r.field_values}
        if len(winner_values) > 1:
            out[field] = GrainResolution(
                verdict=GrainVerdict.LOSSY_AMBIGUOUS,
                resolved_values=None,
                reason="tied most-recent timestamp with conflicting values",
            )
            continue

        resolved = next(r.field_values[field] for r in at_max if field in r.field_values)
        out[field] = GrainResolution(
            verdict=GrainVerdict.LOSSY_RESOLVED,
            resolved_values={field: resolved},
            reason="most recent timestamp wins",
        )
    return out
