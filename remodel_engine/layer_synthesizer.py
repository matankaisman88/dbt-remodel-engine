"""Layer Synthesizer — Section 3 classification rules (strict priority order)."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from remodel_engine.sql_analysis import analyze_sql

class Layer(str, Enum):
    STAGING = "staging"
    INTERMEDIATE = "intermediate"
    MARTS = "marts"
    NEEDS_MANUAL_REVIEW = "needs_manual_review"


class MartKind(str, Enum):
    DIM = "dim"
    FCT = "fct"


class LegacyTargetMeta(BaseModel):
    target_name: str
    last_transformation_type: str = Field(
        description="e.g. update_strategy_scd, aggregator, expression"
    )


class ClassificationResult(BaseModel):
    layer: Layer
    model_name: str
    suggested_name: str | None = None
    mart_kind: MartKind | None = None
    classification_reason: str
    flagged: bool = False


def _staging_transforms_only(sql: str) -> tuple[bool, str]:
    analysis = analyze_sql(sql)
    if analysis.has_join:
        return False, "staging rule: multi-source join detected"
    if analysis.has_aggregation and not _is_basic_dedup_only(sql):
        return False, "staging rule: aggregation beyond basic deduplication"
    if analysis.has_case:
        return False, "staging rule: CASE/router-style branching not allowed in staging"
    return True, "staging rule: source-only upstream with allowed transforms"


def _is_basic_dedup_only(sql: str) -> bool:
    upper = sql.upper()
    if "DISTINCT" in upper:
        return True
    if "QUALIFY" in upper and "ROW_NUMBER" in upper:
        return True
    return False


def classify_model(
    model_name: str,
    sql: str,
    *,
    legacy_targets: dict[str, LegacyTargetMeta] | None = None,
) -> ClassificationResult:
    """
    Apply rules in order: Staging → Intermediate → Marts → NEEDS_MANUAL_REVIEW.
    First matching rule wins.
    """
    legacy_targets = legacy_targets or {}
    analysis = analyze_sql(sql)

    # Rule 1 — Staging (must fully match; otherwise fall through)
    if not analysis.refs and analysis.sources:
        ok, detail = _staging_transforms_only(sql)
        if ok:
            return ClassificationResult(
                layer=Layer.STAGING,
                model_name=model_name,
                suggested_name=_with_prefix(model_name, "stg_"),
                classification_reason=f"matched rule #1: {detail}",
            )

    # Rule 2 — Intermediate
    if analysis.refs and (
        analysis.has_join
        or analysis.has_window
        or analysis.has_aggregation
        or analysis.has_case
    ):
        return ClassificationResult(
            layer=Layer.INTERMEDIATE,
            model_name=model_name,
            suggested_name=_with_prefix(model_name, "int_"),
            classification_reason=(
                "matched rule #2: ref() upstream with join/window/aggregation/CASE"
            ),
        )

    # Rule 3 — Marts (1:1 legacy physical target mapping)
    if model_name in legacy_targets:
        meta = legacy_targets[model_name]
        kind = _mart_kind_from_transformation(meta.last_transformation_type)
        if kind is None:
            return ClassificationResult(
                layer=Layer.NEEDS_MANUAL_REVIEW,
                model_name=model_name,
                classification_reason=(
                    "rule #3 ambiguous: legacy target mapping present but "
                    f"unknown last_transformation_type={meta.last_transformation_type!r}"
                ),
                flagged=True,
            )
        prefix = "dim_" if kind == MartKind.DIM else "fct_"
        return ClassificationResult(
            layer=Layer.MARTS,
            model_name=model_name,
            suggested_name=_with_prefix(model_name, prefix),
            mart_kind=kind,
            classification_reason=(
                f"matched rule #3: direct 1:1 target mapping to {meta.target_name}, "
                f"{meta.last_transformation_type}"
            ),
        )

    if analysis.refs:
        return ClassificationResult(
            layer=Layer.NEEDS_MANUAL_REVIEW,
            model_name=model_name,
            classification_reason=(
                "rule #2 incomplete: has ref() but no join/window/aggregation/CASE — "
                "cannot classify as intermediate; not a legacy target"
            ),
            flagged=True,
        )

    if analysis.sources and not analysis.refs:
        return ClassificationResult(
            layer=Layer.NEEDS_MANUAL_REVIEW,
            model_name=model_name,
            classification_reason=(
                "failed rule #1 (sources only but disallowed transforms) and no other rule matched"
            ),
            flagged=True,
        )

    return ClassificationResult(
        layer=Layer.NEEDS_MANUAL_REVIEW,
        model_name=model_name,
        classification_reason="no rule matched unambiguously — fail-closed to NEEDS_MANUAL_REVIEW",
        flagged=True,
    )


def _mart_kind_from_transformation(last_type: str) -> MartKind | None:
    normalized = last_type.lower().replace(" ", "_").replace("-", "_")
    if "update_strategy" in normalized or "scd" in normalized:
        return MartKind.DIM
    if "aggregator" in normalized or "fact" in normalized:
        return MartKind.FCT
    return None


def _with_prefix(model_name: str, prefix: str) -> str:
    base = model_name
    changed = True
    while changed:
        changed = False
        for p in ("raw_", "stg_", "int_", "dim_", "fct_"):
            if base.startswith(p):
                base = base[len(p) :]
                changed = True
                break
    if base.startswith(prefix):
        return base
    return f"{prefix}{base}"
