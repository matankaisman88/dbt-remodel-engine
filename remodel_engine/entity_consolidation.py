"""Entity consolidation wiring: raw rows → survivorship → extra remodeled models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from remodel_engine.entity_consolidation_templates import (
    render_compat_view_sql,
    render_crosswalk_sql,
    render_survivorship_audit_sql,
)
from remodel_engine.grain_resolution import (
    GrainResolution,
    GrainVerdict,
    SourceRecordRef,
    classify_and_resolve,
)
from remodel_engine.schema import EntityConsolidationSpec, ParityCheck, RemodeledModel


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            pass
        for fmt in ("%Y%m%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    raise ValueError(f"unsupported timestamp value: {value!r}")


def _source_record_from_dict(data: dict[str, Any]) -> SourceRecordRef:
    return SourceRecordRef(
        old_key=str(data["old_key"]),
        old_table=str(data["old_table"]),
        field_values=dict(data.get("field_values") or {}),
        timestamp=_parse_timestamp(data["timestamp"]),
    )


def load_entity_consolidation_clusters(
    parity_context: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not parity_context:
        return []
    clusters = parity_context.get("entity_consolidation_clusters")
    if isinstance(clusters, list):
        return clusters
    return []


def clusters_for_spec(
    spec: EntityConsolidationSpec,
    all_clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not all_clusters:
        return []
    keyed = {
        c.get("spec_new_entity"): c
        for c in all_clusters
        if isinstance(c, dict) and c.get("spec_new_entity")
    }
    if spec.new_entity in keyed:
        return [keyed[spec.new_entity]]
    matched: list[dict[str, Any]] = []
    for cluster in all_clusters:
        if not isinstance(cluster, dict):
            continue
        rows = cluster.get("rows") or []
        if any(r.get("old_table") in spec.old_tables for r in rows):
            matched.append(cluster)
    return matched


def build_audit_rows_for_cluster(
    cluster: dict[str, Any],
    spec: EntityConsolidationSpec,
    resolutions: dict[str, dict[str, GrainResolution]],
) -> list[dict[str, Any]]:
    rows = cluster.get("rows") or []
    new_key = str(cluster.get("new_key", ""))
    field_resolutions = resolutions.get(new_key) or {}
    audit: list[dict[str, Any]] = []
    for raw in rows:
        for field in spec.conflict_fields:
            resolution = field_resolutions.get(field)
            audit.append(
                {
                    "old_key": str(raw.get("old_key")),
                    "old_table": str(raw.get("old_table")),
                    "new_key": new_key,
                    "conflict_field": field,
                    "resolution_verdict": (
                        resolution.verdict.value if resolution else None
                    ),
                    "resolution_reason": resolution.reason if resolution else None,
                }
            )
    return audit


def run_entity_consolidation_pass(
    specs: list[EntityConsolidationSpec],
    parity_context: dict[str, Any] | None,
) -> tuple[list[RemodeledModel], bool]:
    """Returns extra remodeled models and whether survivorship review is needed."""
    clusters = load_entity_consolidation_clusters(parity_context)
    extra: list[RemodeledModel] = []
    needs_survivorship_review = False

    for spec in specs:
        spec_clusters = clusters_for_spec(spec, clusters)
        resolutions_by_new_key: dict[str, dict[str, GrainResolution]] = {}
        audit_rows: list[dict[str, Any]] = []

        for cluster in spec_clusters:
            new_key = str(cluster.get("new_key", ""))
            refs = [_source_record_from_dict(r) for r in cluster.get("rows") or []]
            field_res = classify_and_resolve(refs, spec.conflict_fields)
            resolutions_by_new_key[new_key] = field_res
            for _field, resolution in field_res.items():
                if resolution.verdict == GrainVerdict.LOSSY_AMBIGUOUS:
                    needs_survivorship_review = True
            audit_rows.extend(
                build_audit_rows_for_cluster(cluster, spec, resolutions_by_new_key)
            )

        crosswalk_name = f"int_{spec.new_entity}__crosswalk"
        audit_name = f"int_{spec.new_entity}__survivorship_audit"
        skipped = ParityCheck(status="skipped", row_count_match=None)

        extra.append(
            RemodeledModel(
                model_name=crosswalk_name,
                layer="intermediate",
                sql=render_crosswalk_sql(spec),
                relative_path=f"models/intermediate/{crosswalk_name}.sql",
                classification_reason="entity_consolidation: crosswalk",
                parity_check=skipped,
            )
        )
        for old_table in spec.old_tables:
            compat_name = f"stg_{old_table}__compat"
            extra.append(
                RemodeledModel(
                    model_name=compat_name,
                    layer="staging",
                    sql=render_compat_view_sql(old_table, spec),
                    relative_path=f"models/staging/{compat_name}.sql",
                    classification_reason=f"entity_consolidation: compat view for {old_table}",
                    parity_check=skipped,
                )
            )
        extra.append(
            RemodeledModel(
                model_name=audit_name,
                layer="intermediate",
                sql=render_survivorship_audit_sql(spec),
                relative_path=f"models/intermediate/{audit_name}.sql",
                classification_reason="entity_consolidation: survivorship audit",
                parity_check=skipped,
                merge_audits=audit_rows,
            )
        )

        if parity_context is not None and spec_clusters:
            from remodel_engine.parity_gate import verify_no_physical_data_loss

            raw_rows = [
                r
                for cluster in spec_clusters
                for r in (cluster.get("rows") or [])
            ]
            loss_check = verify_no_physical_data_loss(raw_rows, audit_rows)
            extra[-1].parity_check = ParityCheck(
                status=loss_check.status,
                row_count_match=loss_check.row_count_match,
                error=loss_check.error,
            )
    return extra, needs_survivorship_review
