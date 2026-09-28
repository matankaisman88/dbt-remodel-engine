"""Orchestrates remodel: decompose → refactor → classify → EXPLAIN → parity."""

from __future__ import annotations

import duckdb

from remodel_engine.graph_builder import build_after_graph, build_before_graph
from remodel_engine.layer_synthesizer import LegacyTargetMeta, Layer, classify_model
from remodel_engine.parity_gate import ParityContext, run_parity_gate
from remodel_engine.physical_decomposer import (
    DecomposeResult,
    PhysicalModel,
    physical_decompose_batch,
    topological_model_order,
)
from remodel_engine.refactor_rules import (
    LookupRewriteSpec,
    apply_lookup_window_rewrite,
    collapse_eligible_ctes,
    explain_gate,
)
from remodel_engine.entity_consolidation import run_entity_consolidation_pass
from remodel_engine.schema import (
    EntityConsolidationSpec,
    ParityCheck,
    RefactoringSummary,
    RemodelRequest,
    RemodelResponse,
    RemodeledModel,
    ShadowedLookupRenameSpec,
)
from remodel_engine.star_shadowing import fix_star_shadowing_for_ctas
from remodel_engine.sql_analysis import compile_dbt_sql, extract_refs, parse_ctes


class RemodelEngine:
    def remodel(self, request: RemodelRequest) -> RemodelResponse:
        legacy_targets = {
            k: LegacyTargetMeta(**v) for k, v in request.legacy_targets.items()
        }
        lookup_specs = {
            s["model_name"]: LookupRewriteSpec(**s) for s in request.lookup_rewrites
        }
        shadow_lookup_specs = [
            ShadowedLookupRenameSpec(**s) for s in request.shadowed_lookup_renames
        ]
        entity_consolidation_specs = [
            EntityConsolidationSpec(**s) for s in request.entity_consolidations
        ]
        parity_ctx = _parity_context_from_request(request)

        decompose_stats = DecomposeResult()
        working: list[_WorkModel] = []
        raw_sql_by_name = {m.model_name: m.sql for m in request.raw_dbt_models}

        if request.preferences.physical_decompose:
            decomposed = physical_decompose_batch(
                [
                    {
                        "model_name": m.model_name,
                        "sql": m.sql,
                        "materialization": m.materialization,
                    }
                    for m in request.raw_dbt_models
                ],
                legacy_targets=legacy_targets,
            )
            decompose_stats = decomposed
            for physical in decomposed.models:
                working.append(
                    _WorkModel(
                        name=physical.model_name,
                        sql=physical.sql,
                        materialization=physical.materialization,
                        layer_hint=physical.layer,
                        relative_path=physical.relative_path,
                        classification_reason=physical.classification_reason,
                        source_raw_model=physical.source_raw_model,
                        is_mart=physical.is_mart,
                    )
                )
        else:
            for raw in request.raw_dbt_models:
                working.append(
                    _WorkModel(
                        name=raw.model_name,
                        sql=raw.sql,
                        materialization=raw.materialization,
                    )
                )

        remodeled: list[RemodeledModel] = []
        total_ctes = 0
        total_windows = 0
        manual_review = 0
        any_parity_fail = False

        model_sql_out: dict[str, str] = {}
        model_layers: dict[str, str] = {}

        conn = duckdb.connect(":memory:") if parity_ctx else None
        runtime_table_map: dict[str, str] = {}
        if parity_ctx:
            runtime_table_map = dict(parity_ctx.model_table_map)

        try:
            if conn is not None and parity_ctx:
                conn.execute(parity_ctx.seeds_sql)
                if request.preferences.physical_decompose and working:
                    runtime_table_map = _materialize_physical_models(
                        conn,
                        working,
                        parity_ctx,
                        runtime_table_map,
                        shadow_lookup_specs,
                    )
            elif request.preferences.physical_decompose:
                for item in working:
                    item.sql = fix_star_shadowing_for_ctas(
                        item.sql,
                        model_name=item.name,
                        source_raw_model=item.source_raw_model,
                        shadowed_lookup_renames=shadow_lookup_specs,
                    )

            for item in working:
                pre_refactor_sql = item.sql
                refactored = collapse_eligible_ctes(
                    item.sql, enabled=request.preferences.collapse_ctes
                )
                lookup = apply_lookup_window_rewrite(
                    refactored.sql,
                    lookup_specs.get(item.name),
                    enabled=request.preferences.modernize_window_functions,
                )
                final_sql = lookup.sql
                total_ctes += refactored.ctes_collapsed
                total_windows += lookup.window_functions_applied

                if item.layer_hint and item.classification_reason:
                    classification_layer = item.layer_hint
                    classification_reason = item.classification_reason
                    flagged = classification_layer == Layer.NEEDS_MANUAL_REVIEW.value
                else:
                    classification = classify_model(
                        item.name, final_sql, legacy_targets=legacy_targets
                    )
                    classification_layer = classification.layer.value
                    classification_reason = classification.classification_reason
                    flagged = classification.flagged or classification.layer == Layer.NEEDS_MANUAL_REVIEW
                out_name = item.name
                model_sql_out[out_name] = final_sql
                model_layers[out_name] = classification_layer
                if flagged:
                    manual_review += 1

                explain_ok, explain_msg = (True, "skipped")
                if conn is not None and parity_ctx:
                    try:
                        compiled = compile_dbt_sql(
                            final_sql,
                            runtime_table_map,
                            parity_ctx.source_table_map,
                        )
                        explain_ok, explain_msg = explain_gate(compiled, conn)
                    except Exception as exc:  # noqa: BLE001
                        explain_ok, explain_msg = False, str(exc)

                parity = ParityCheck(status="skipped", row_count_match=None)
                if parity_ctx and conn is not None and item.is_mart and item.source_raw_model:
                    raw_sql = raw_sql_by_name.get(item.source_raw_model, "")
                    result = run_parity_gate(
                        model_name=item.source_raw_model.replace(".", "_"),
                        raw_sql=raw_sql,
                        remodeled_sql=final_sql,
                        context=ParityContext(
                            model_table_map=runtime_table_map,
                            source_table_map=parity_ctx.source_table_map,
                            seeds_sql=parity_ctx.seeds_sql,
                        ),
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
                    elif result.status == "needs_manual_review":
                        manual_review += 1
                    for audit in refactored.merge_audits:
                        audit.verified_by_parity = result.status == "pass"
                elif parity_ctx and conn is not None and not request.preferences.physical_decompose:
                    raw_sql = raw_sql_by_name.get(item.name, item.sql)
                    result = run_parity_gate(
                        model_name=item.name.replace(".", "_"),
                        raw_sql=raw_sql,
                        remodeled_sql=final_sql,
                        context=parity_ctx,
                        conn=conn,
                        gate_grain_risk=classification_layer == Layer.INTERMEDIATE.value,
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
                    elif result.status == "needs_manual_review":
                        manual_review += 1
                elif (
                    parity_ctx
                    and conn is not None
                    and request.preferences.physical_decompose
                    and not item.is_mart
                    and not flagged
                    and classification_layer == Layer.INTERMEDIATE.value
                ):
                    result = run_parity_gate(
                        model_name=item.name.replace(".", "_"),
                        raw_sql=pre_refactor_sql,
                        remodeled_sql=final_sql,
                        context=ParityContext(
                            model_table_map=runtime_table_map,
                            source_table_map=parity_ctx.source_table_map,
                            seeds_sql=parity_ctx.seeds_sql,
                        ),
                        conn=conn,
                        gate_grain_risk=True,
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
                    elif result.status == "needs_manual_review":
                        manual_review += 1
                    for audit in refactored.merge_audits:
                        audit.verified_by_parity = result.status == "pass"
                elif not parity_ctx:
                    parity = ParityCheck(status="skipped", error="no parity_context provided")

                remodeled.append(
                    RemodeledModel(
                        model_name=out_name,
                        layer=classification_layer,
                        sql=final_sql,
                        relative_path=item.relative_path,
                        inner_ctes=[c.name for c in parse_ctes(final_sql)],
                        classification_reason=classification_reason,
                        parity_check=parity,
                        flagged=flagged,
                        merge_audits=[a.model_dump() for a in refactored.merge_audits],
                        source_raw_model=item.source_raw_model,
                    )
                )
        finally:
            if conn is not None:
                conn.close()

        needs_survivorship_review = False
        if entity_consolidation_specs:
            (
                consolidation_models,
                needs_survivorship_review,
                consolidation_rejected,
            ) = run_entity_consolidation_pass(
                entity_consolidation_specs,
                request.parity_context,
            )
            remodeled.extend(consolidation_models)
            if consolidation_rejected:
                any_parity_fail = True

        status = "success"
        if any_parity_fail:
            status = "failed_parity"
        elif manual_review > 0:
            status = "needs_manual_review"
        elif needs_survivorship_review:
            status = "needs_survivorship_review"

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
                shared_models_extracted=decompose_stats.shared_models_extracted,
                ctes_materialized=decompose_stats.ctes_materialized,
            ),
            before_graph=build_before_graph(
                request.legacy_graph_nodes, request.legacy_graph_edges
            ),
            after_graph=build_after_graph(model_sql_out, model_layers),
            remodeled_models=remodeled,
        )


class _WorkModel:
    __slots__ = (
        "name",
        "sql",
        "materialization",
        "layer_hint",
        "relative_path",
        "classification_reason",
        "source_raw_model",
        "is_mart",
    )

    def __init__(
        self,
        *,
        name: str,
        sql: str,
        materialization: str,
        layer_hint: str | None = None,
        relative_path: str | None = None,
        classification_reason: str = "",
        source_raw_model: str | None = None,
        is_mart: bool = False,
    ) -> None:
        self.name = name
        self.sql = sql
        self.materialization = materialization
        self.layer_hint = layer_hint
        self.relative_path = relative_path
        self.classification_reason = classification_reason
        self.source_raw_model = source_raw_model
        self.is_mart = is_mart


def _table_column_names(conn: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    try:
        rows = conn.execute(f"DESCRIBE {table}").fetchall()
    except duckdb.Error:
        return set()
    return {str(row[0]).upper() for row in rows}


def _ref_source_column_names(
    conn: duckdb.DuckDBPyConnection,
    sql: str,
    table_map: dict[str, str],
) -> set[str]:
    columns: set[str] = set()
    for ref in extract_refs(sql):
        mapped = table_map.get(ref)
        if mapped:
            columns |= _table_column_names(conn, mapped)
    return columns


def _materialize_physical_models(
    conn: duckdb.DuckDBPyConnection,
    models: list[_WorkModel],
    context: ParityContext,
    table_map: dict[str, str],
    shadow_lookup_specs: list[ShadowedLookupRenameSpec],
) -> dict[str, str]:
    physical = [
        PhysicalModel(
            model_name=m.name,
            relative_path=m.relative_path or f"models/{m.name}.sql",
            sql=m.sql,
            layer=m.layer_hint or "intermediate",
        )
        for m in models
    ]
    order = topological_model_order(physical)
    by_name = {m.name: m for m in models}
    updated = dict(table_map)
    for name in order:
        item = by_name[name]
        ref_columns = _ref_source_column_names(conn, item.sql, updated)
        renamed_present = any(
            spec.renamed_column.upper() in ref_columns
            for spec in shadow_lookup_specs
            if item.name == spec.model_name
            or (item.source_raw_model == spec.model_name)
            or item.name.startswith(f"int_{spec.model_name}__")
        )
        item.sql = fix_star_shadowing_for_ctas(
            item.sql,
            model_name=item.name,
            source_raw_model=item.source_raw_model,
            shadowed_lookup_renames=shadow_lookup_specs,
            renamed_column_present=renamed_present,
        )
        try:
            compiled = compile_dbt_sql(item.sql, updated, context.source_table_map)
            table = f"remodel_{name}"
            conn.execute(f"CREATE OR REPLACE TABLE {table} AS {compiled}")
            updated[name] = table
        except (KeyError, duckdb.Error):
            # Keep remodeling; parity/explain on downstream models will fail closed.
            continue
    return updated


def _parity_context_from_request(request: RemodelRequest) -> ParityContext | None:
    if not request.parity_context:
        return None
    from pathlib import Path

    ctx = request.parity_context
    explicit_source = {
        (k.split(".", 1)[0], k.split(".", 1)[1]): v
        for k, v in ctx.get("source_table_map", {}).items()
    }
    seeds_sql = ctx.get("seeds_sql", "")
    if isinstance(seeds_sql, str) and seeds_sql.strip().endswith(".sql"):
        seeds_path = Path(seeds_sql)
        if not seeds_path.is_file():
            seeds_path = Path.cwd() / seeds_sql
        seeds_sql = seeds_path.read_text()
    derived_source: dict[tuple[str, str], str] = {}
    if isinstance(seeds_sql, str) and seeds_sql.strip():
        from remodel_engine.seed_introspection import extract_source_table_map

        derived_source = extract_source_table_map(seeds_sql)
    source_map = {**derived_source, **explicit_source}
    return ParityContext(
        model_table_map=ctx.get("model_table_map", {}),
        source_table_map=source_map,
        seeds_sql=seeds_sql,
    )
