"""Orchestrates remodel: refactor → classify → EXPLAIN → parity."""

from __future__ import annotations

import duckdb

from remodel_engine.graph_builder import build_after_graph, build_before_graph
from remodel_engine.layer_synthesizer import LegacyTargetMeta, Layer, classify_model
from remodel_engine.parity_gate import ParityContext, run_parity_gate
from remodel_engine.refactor_rules import (
    LookupRewriteSpec,
    apply_lookup_window_rewrite,
    collapse_eligible_ctes,
    explain_gate,
)
from remodel_engine.schema import (
    ParityCheck,
    RefactoringSummary,
    RemodelRequest,
    RemodelResponse,
    RemodeledModel,
)
from remodel_engine.sql_analysis import parse_ctes


class RemodelEngine:
    def remodel(self, request: RemodelRequest) -> RemodelResponse:
        legacy_targets = {
            k: LegacyTargetMeta(**v) for k, v in request.legacy_targets.items()
        }
        lookup_specs = {
            s["model_name"]: LookupRewriteSpec(**s) for s in request.lookup_rewrites
        }
        parity_ctx = _parity_context_from_request(request)

        remodeled: list[RemodeledModel] = []
        total_ctes = 0
        total_windows = 0
        manual_review = 0
        any_parity_fail = False

        model_sql_out: dict[str, str] = {}
        model_layers: dict[str, str] = {}

        conn = duckdb.connect(":memory:") if parity_ctx else None
        try:
            if conn is not None and parity_ctx:
                conn.execute(parity_ctx.seeds_sql)
            for raw in request.raw_dbt_models:
                refactored = collapse_eligible_ctes(
                    raw.sql, enabled=request.preferences.collapse_ctes
                )
                lookup = apply_lookup_window_rewrite(
                    refactored.sql,
                    lookup_specs.get(raw.model_name),
                    enabled=request.preferences.modernize_window_functions,
                )
                final_sql = lookup.sql
                total_ctes += refactored.ctes_collapsed
                total_windows += lookup.window_functions_applied

                classification = classify_model(
                    raw.model_name, final_sql, legacy_targets=legacy_targets
                )
                out_name = classification.suggested_name or raw.model_name
                model_sql_out[out_name] = final_sql
                model_layers[out_name] = classification.layer.value
                if classification.flagged or classification.layer == Layer.NEEDS_MANUAL_REVIEW:
                    manual_review += 1

                explain_ok, explain_msg = (True, "skipped")
                if conn is not None and parity_ctx:
                    try:
                        from remodel_engine.sql_analysis import compile_dbt_sql

                        compiled = compile_dbt_sql(
                            final_sql,
                            parity_ctx.model_table_map,
                            parity_ctx.source_table_map,
                        )
                        explain_ok, explain_msg = explain_gate(compiled, conn)
                    except Exception as exc:  # noqa: BLE001
                        explain_ok, explain_msg = False, str(exc)

                parity = ParityCheck(status="skipped", row_count_match=None)
                trace_rule: str | None = None
                if parity_ctx and conn is not None:
                    result = run_parity_gate(
                        model_name=raw.model_name.replace(".", "_"),
                        raw_sql=raw.sql,
                        remodeled_sql=final_sql,
                        context=parity_ctx,
                        conn=conn,
                    )
                    parity = ParityCheck(
                        status=result.status,
                        row_count_match=result.row_count_match,
                        column_diff=[d.model_dump() for d in result.column_diff],
                        error=result.error,
                    )
                    if not explain_ok:
                        parity = ParityCheck(
                            status="fail",
                            row_count_match=False,
                            error=f"explain_gate: {explain_msg}",
                        )
                    if result.status == "fail":
                        any_parity_fail = True
                        if refactored.merge_audits:
                            trace_rule = "cte_inlining_merge"
                        elif lookup.window_functions_applied:
                            trace_rule = "lookup_window_rewrite"
                    for audit in refactored.merge_audits:
                        audit.verified_by_parity = result.status == "pass"
                elif not parity_ctx:
                    parity = ParityCheck(status="skipped", error="no parity_context provided")

                remodeled.append(
                    RemodeledModel(
                        model_name=out_name,
                        layer=classification.layer.value,
                        sql=final_sql,
                        inner_ctes=[c.name for c in parse_ctes(final_sql)],
                        classification_reason=classification.classification_reason,
                        parity_check=parity,
                        flagged=classification.flagged,
                        merge_audits=[a.model_dump() for a in refactored.merge_audits],
                    )
                )
        finally:
            if conn is not None:
                conn.close()

        status = "success"
        if any_parity_fail:
            status = "failed_parity"
        elif manual_review > 0:
            status = "needs_manual_review"

        return RemodelResponse(
            pipeline_id=request.pipeline_id,
            status=status,  # type: ignore[arg-type]
            refactoring_summary=RefactoringSummary(
                legacy_transformations_count=request.legacy_transformations_count
                or len(request.raw_dbt_models),
                modern_models_count=len(remodeled),
                ctes_collapsed=total_ctes,
                window_functions_applied=total_windows,
                models_needs_manual_review=manual_review,
            ),
            before_graph=build_before_graph(
                request.legacy_graph_nodes, request.legacy_graph_edges
            ),
            after_graph=build_after_graph(model_sql_out, model_layers),
            remodeled_models=remodeled,
        )


def _parity_context_from_request(request: RemodelRequest) -> ParityContext | None:
    if not request.parity_context:
        return None
    from pathlib import Path

    ctx = request.parity_context
    source_map = {
        (k.split(".", 1)[0], k.split(".", 1)[1]): v
        for k, v in ctx.get("source_table_map", {}).items()
    }
    seeds_sql = ctx.get("seeds_sql", "")
    if isinstance(seeds_sql, str) and seeds_sql.strip().endswith(".sql"):
        seeds_path = Path(seeds_sql)
        if not seeds_path.is_file():
            seeds_path = Path.cwd() / seeds_sql
        seeds_sql = seeds_path.read_text()
    return ParityContext(
        model_table_map=ctx.get("model_table_map", {}),
        source_table_map=source_map,
        seeds_sql=seeds_sql,
    )
