"""Entity consolidation wiring: raw rows → survivorship → extra remodeled models."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

import duckdb

from remodel_engine.entity_consolidation_templates import (
    crosswalk_model_name,
    render_compat_view_sql,
    render_crosswalk_sql,
    render_entity_sql,
    render_survivorship_audit_sql,
    validate_entity_consolidation_spec,
)
from remodel_engine.grain_resolution import (
    GrainResolution,
    GrainVerdict,
    SourceRecordRef,
    classify_and_resolve,
)
from remodel_engine.parity_gate import (
    ParityCheckResult,
    verify_entity_consolidation_no_data_loss,
    verify_no_physical_data_loss,
)
from remodel_engine.schema import EntityConsolidationSpec, ParityCheck, RemodeledModel
from remodel_engine.sql_analysis import compile_dbt_sql


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
    matched = [
        c
        for c in all_clusters
        if isinstance(c, dict) and c.get("spec_new_entity") == spec.new_entity
    ]
    if matched:
        return matched
    return [
        c
        for c in all_clusters
        if isinstance(c, dict)
        and any(
            r.get("old_table") in spec.old_tables for r in (c.get("rows") or [])
        )
    ]


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


def rows_by_old_table(
    spec: EntityConsolidationSpec,
    clusters: list[dict[str, Any]],
    extra_rows: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Collect raw rows per old_table from clusters (and optional extras)."""
    by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for cluster in clusters:
        for row in cluster.get("rows") or []:
            key = (str(row["old_table"]), str(row["old_key"]))
            if key in seen:
                continue
            seen.add(key)
            by_table[str(row["old_table"])].append(row)
    for row in extra_rows or []:
        key = (str(row["old_table"]), str(row["old_key"]))
        if key in seen:
            continue
        seen.add(key)
        by_table[str(row["old_table"])].append(row)
    for table in spec.old_tables:
        by_table.setdefault(table, [])
    return dict(by_table)


def _sql_literal(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def materialize_entity_consolidation_sources(
    conn: duckdb.DuckDBPyConnection,
    spec: EntityConsolidationSpec,
    clusters: list[dict[str, Any]],
    extra_rows: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Create DuckDB tables for each old_table; return ref name → table name."""
    validate_entity_consolidation_spec(spec)
    table_map: dict[str, str] = {}
    grouped = rows_by_old_table(spec, clusters, extra_rows=extra_rows)
    for old_table in spec.old_tables:
        key_col = spec.old_key_columns[old_table]
        columns = [key_col, spec.timestamp_column, *spec.conflict_fields]
        duck_table = f"ec_src_{old_table}"
        col_defs = ", ".join(f"{col} VARCHAR" for col in columns)
        conn.execute(f"CREATE OR REPLACE TABLE {duck_table} ({col_defs})")
        for row in grouped.get(old_table, []):
            fv = row.get("field_values") or {}
            values = [
                _sql_literal(row.get("old_key")),
                _sql_literal(fv.get(spec.timestamp_column, row.get("timestamp"))),
                *[_sql_literal(fv.get(col)) for col in spec.conflict_fields],
            ]
            conn.execute(
                f"INSERT INTO {duck_table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
            )
        table_map[old_table] = duck_table
    return table_map


def execute_entity_consolidation_sql(
    conn: duckdb.DuckDBPyConnection,
    spec: EntityConsolidationSpec,
    clusters: list[dict[str, Any]],
    *,
    extra_rows: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    """Compile and execute generated consolidation SQL; return model → DuckDB table."""
    source_map = materialize_entity_consolidation_sources(
        conn, spec, clusters, extra_rows=extra_rows
    )
    crosswalk_name = crosswalk_model_name(spec)
    audit_name = f"int_{spec.new_entity}__survivorship_audit"
    compat_names = {t: f"stg_{t}__compat" for t in spec.old_tables}

    sql_by_model = {
        crosswalk_name: render_crosswalk_sql(spec, clusters),
        spec.new_entity: render_entity_sql(spec),
        audit_name: render_survivorship_audit_sql(spec),
        **{
            compat_names[t]: render_compat_view_sql(t, spec) for t in spec.old_tables
        },
    }

    runtime_map = dict(source_map)
    executed: dict[str, str] = {}
    order = [
        crosswalk_name,
        spec.new_entity,
        audit_name,
        *compat_names.values(),
    ]
    for model_name in order:
        compiled = compile_dbt_sql(
            sql_by_model[model_name],
            runtime_map,
            {},
        )
        out_table = f"ec_model_{model_name.replace('.', '_')}"
        conn.execute(f"CREATE OR REPLACE TABLE {out_table} AS {compiled}")
        runtime_map[model_name] = out_table
        executed[model_name] = out_table
    return executed


def run_entity_consolidation_pass(
    specs: list[EntityConsolidationSpec],
    parity_context: dict[str, Any] | None,
) -> tuple[list[RemodeledModel], bool]:
    """Returns extra remodeled models and whether survivorship review is needed."""
    clusters = load_entity_consolidation_clusters(parity_context)
    extra: list[RemodeledModel] = []
    needs_survivorship_review = False

    for spec in specs:
        validate_entity_consolidation_spec(spec)
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

        crosswalk_name = crosswalk_model_name(spec)
        audit_name = f"int_{spec.new_entity}__survivorship_audit"
        skipped = ParityCheck(status="skipped", row_count_match=None)

        crosswalk_sql = render_crosswalk_sql(spec, spec_clusters)
        entity_sql = render_entity_sql(spec)
        audit_sql = render_survivorship_audit_sql(spec)

        extra.append(
            RemodeledModel(
                model_name=crosswalk_name,
                layer="intermediate",
                sql=crosswalk_sql,
                relative_path=f"models/intermediate/{crosswalk_name}.sql",
                classification_reason="entity_consolidation: crosswalk",
                parity_check=skipped,
            )
        )
        extra.append(
            RemodeledModel(
                model_name=spec.new_entity,
                layer="marts",
                sql=entity_sql,
                relative_path=f"models/marts/{spec.new_entity}.sql",
                classification_reason="entity_consolidation: consolidated entity",
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
        audit_model = RemodeledModel(
            model_name=audit_name,
            layer="intermediate",
            sql=audit_sql,
            relative_path=f"models/intermediate/{audit_name}.sql",
            classification_reason="entity_consolidation: survivorship audit",
            parity_check=skipped,
            merge_audits=audit_rows,
        )
        extra.append(audit_model)

        if parity_context is not None and spec_clusters:
            conn = duckdb.connect(":memory:")
            try:
                executed = execute_entity_consolidation_sql(
                    conn, spec, spec_clusters
                )
                loss_check = verify_entity_consolidation_no_data_loss(
                    conn,
                    spec=spec,
                    source_table_map={
                        t: f"ec_src_{t}" for t in spec.old_tables
                    },
                    audit_table=executed[audit_name],
                    compat_tables={
                        t: executed[f"stg_{t}__compat"] for t in spec.old_tables
                    },
                )
            except Exception as exc:  # noqa: BLE001
                loss_check = ParityCheckResult(status="fail", error=str(exc))
            finally:
                conn.close()
            audit_model.parity_check = ParityCheck(
                status=loss_check.status,
                row_count_match=loss_check.row_count_match,
                error=loss_check.error,
            )
    return extra, needs_survivorship_review


__all__ = [
    "build_audit_rows_for_cluster",
    "clusters_for_spec",
    "execute_entity_consolidation_sql",
    "load_entity_consolidation_clusters",
    "materialize_entity_consolidation_sources",
    "rows_by_old_table",
    "run_entity_consolidation_pass",
    "verify_no_physical_data_loss",
]
