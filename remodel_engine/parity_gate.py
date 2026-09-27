"""Model-Level Parity Gate — Section 5 (DuckDB result equivalence)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import duckdb
from pydantic import BaseModel, Field

from remodel_engine.refactor_rules import assess_rule2
from remodel_engine.sql_analysis import analyze_sql, assess_grain_risk, compile_dbt_sql


def grain_risk_requires_manual_review(sql: str) -> tuple[bool, str | None]:
    """
    Parity grain gate — aligned with rule #2 classification.

    Benign single-ref projections, filters, and expression transforms do not block
    parity; only grain-changing constructs trigger manual review.
    """
    analysis = analyze_sql(sql)
    if analysis.refs:
        rule2 = assess_rule2(sql)
        if rule2.needs_manual_review:
            reason = rule2.classification_reason
            if reason.startswith("rule #2 grain risk: "):
                reason = reason[len("rule #2 grain risk: ") :]
            return True, reason
        return False, None
    risky, reason = assess_grain_risk(sql)
    return risky, reason


class ColumnDiff(BaseModel):
    column: str
    raw_null_count: int
    remodeled_null_count: int
    sample_mismatches: list[dict[str, Any]] = Field(default_factory=list)


class ParityCheckResult(BaseModel):
    status: str  # pass | fail | skipped
    row_count_match: bool | None = None
    raw_row_count: int | None = None
    remodeled_row_count: int | None = None
    column_diff: list[ColumnDiff] = Field(default_factory=list)
    error: str | None = None
    trace_rule: str | None = None


@dataclass
class ParityContext:
    model_table_map: dict[str, str]
    source_table_map: dict[tuple[str, str], str]
    seeds_sql: str


def _table_columns(conn: duckdb.DuckDBPyConnection, table: str) -> list[str]:
    return [row[0] for row in conn.execute(f"DESCRIBE {table}").fetchall()]


def verify_no_physical_data_loss(
    raw_rows: list[dict[str, Any]],
    audit_model_rows: list[dict[str, Any]],
) -> ParityCheckResult:
    """Assert every old_key from every old_table appears in the audit model output."""
    expected = {(str(r["old_key"]), str(r["old_table"])) for r in raw_rows}
    if not expected:
        return ParityCheckResult(status="skipped", row_count_match=True)
    seen = {
        (str(r["old_key"]), str(r["old_table"]))
        for r in audit_model_rows
        if r.get("old_key") is not None and r.get("old_table") is not None
    }
    missing = expected - seen
    if missing:
        sample = sorted(missing)[:5]
        return ParityCheckResult(
            status="fail",
            row_count_match=False,
            error=f"audit missing {len(missing)} raw keys; sample={sample}",
        )
    return ParityCheckResult(status="pass", row_count_match=True)


def run_parity_gate(
    *,
    model_name: str,
    raw_sql: str,
    remodeled_sql: str,
    context: ParityContext,
    conn: duckdb.DuckDBPyConnection | None = None,
    sample_limit: int = 5,
    gate_grain_risk: bool = False,
) -> ParityCheckResult:
    owns_conn = conn is None
    if conn is None:
        conn = duckdb.connect(":memory:")

    try:
        if gate_grain_risk:
            risky, risk_reason = grain_risk_requires_manual_review(remodeled_sql)
            if risky:
                return ParityCheckResult(
                    status="needs_manual_review",
                    trace_rule=risk_reason,
                )

        try:
            conn.execute(context.seeds_sql)
        except duckdb.Error:
            pass
        raw_compiled = compile_dbt_sql(
            raw_sql, context.model_table_map, context.source_table_map
        )
        remodeled_compiled = compile_dbt_sql(
            remodeled_sql, context.model_table_map, context.source_table_map
        )

        raw_table = f"parity_raw_{model_name}"
        rem_table = f"parity_rem_{model_name}"
        conn.execute(f"CREATE OR REPLACE TABLE {raw_table} AS {raw_compiled}")
        conn.execute(f"CREATE OR REPLACE TABLE {rem_table} AS {remodeled_compiled}")

        raw_count = conn.execute(f"SELECT COUNT(*) FROM {raw_table}").fetchone()[0]
        rem_count = conn.execute(f"SELECT COUNT(*) FROM {rem_table}").fetchone()[0]
        row_count_match = raw_count == rem_count

        raw_cols = _table_columns(conn, raw_table)
        rem_cols = _table_columns(conn, rem_table)
        columns = [c for c in raw_cols if c in rem_cols]

        column_diffs: list[ColumnDiff] = []
        for col in columns:
            raw_nulls = conn.execute(
                f'SELECT COUNT(*) FROM {raw_table} WHERE "{col}" IS NULL'
            ).fetchone()[0]
            rem_nulls = conn.execute(
                f'SELECT COUNT(*) FROM {rem_table} WHERE "{col}" IS NULL'
            ).fetchone()[0]
            mismatches: list[dict[str, Any]] = []
            if raw_nulls != rem_nulls:
                mismatches.append(
                    {
                        "kind": "null_pattern",
                        "raw_nulls": raw_nulls,
                        "remodeled_nulls": rem_nulls,
                    }
                )
            if mismatches:
                column_diffs.append(
                    ColumnDiff(
                        column=col,
                        raw_null_count=raw_nulls,
                        remodeled_null_count=rem_nulls,
                        sample_mismatches=mismatches,
                    )
                )

        if set(raw_cols) != set(rem_cols):
            column_diffs.append(
                ColumnDiff(
                    column="__schema__",
                    raw_null_count=0,
                    remodeled_null_count=0,
                    sample_mismatches=[
                        {
                            "kind": "column_set_mismatch",
                            "raw_only": sorted(set(raw_cols) - set(rem_cols)),
                            "remodeled_only": sorted(set(rem_cols) - set(raw_cols)),
                        }
                    ],
                )
            )

        diff_rows = conn.execute(
            f"""
            SELECT COUNT(*) FROM (
              (SELECT * FROM {raw_table} EXCEPT SELECT * FROM {rem_table})
              UNION ALL
              (SELECT * FROM {rem_table} EXCEPT SELECT * FROM {raw_table})
            )
            """
        ).fetchone()[0]

        if diff_rows > 0:
            sample = conn.execute(
                f"""
                SELECT * FROM (
                  (SELECT * FROM {raw_table} EXCEPT SELECT * FROM {rem_table})
                  UNION ALL
                  (SELECT * FROM {rem_table} EXCEPT SELECT * FROM {raw_table})
                ) LIMIT {sample_limit}
                """
            ).fetchall()
            column_diffs.append(
                ColumnDiff(
                    column="__rows__",
                    raw_null_count=raw_count,
                    remodeled_null_count=rem_count,
                    sample_mismatches=[
                        {"kind": "row_diff_count", "diff_rows": diff_rows, "sample": sample}
                    ],
                )
            )

        status = (
            "pass"
            if row_count_match and diff_rows == 0 and not column_diffs
            else "fail"
        )
        return ParityCheckResult(
            status=status,
            row_count_match=row_count_match,
            raw_row_count=raw_count,
            remodeled_row_count=rem_count,
            column_diff=column_diffs,
        )
    except Exception as exc:  # noqa: BLE001
        return ParityCheckResult(status="fail", error=str(exc))
    finally:
        if owns_conn:
            conn.close()
