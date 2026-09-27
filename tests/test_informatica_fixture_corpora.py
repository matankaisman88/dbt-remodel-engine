"""Remodel tests against committed corpora under tests/fixtures/informatica/."""

from __future__ import annotations

from pathlib import Path

import pytest

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine

INFORMATICA_FIXTURES = Path(__file__).parent / "fixtures" / "informatica"

_MANIFESTS = sorted(
    p for p in INFORMATICA_FIXTURES.glob("*/manifest.json") if p.is_file()
)

# Pipelines that still fail after source_table_map auto-derivation (real SQL/export gaps).
_CORPUS_XFAIL: dict[str, str] = {
    "informatica_stress_corpus_aggregator_multi_groupby": (
        "classifier: NEEDS_MANUAL_REVIEW for complex aggregator pipeline"
    ),
    "informatica_stress_corpus_deep_lookup_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for deep lookup chain"
    ),
    "informatica_stress_corpus_filter_router_union_faninout": (
        "parity: explain_gate — materialized table int_rtr_high_low missing after CTE inlining"
    ),
    "informatica_stress_corpus_informatica_scd_type2": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "informatica_stress_corpus_long_linear_10stage": (
        "parity: explain_gate — materialized table int_rtr_sev missing after CTE inlining"
    ),
    "informatica_stress_corpus_lookup_composite_condition": (
        "classifier: NEEDS_MANUAL_REVIEW for composite lookup condition"
    ),
    "informatica_stress_corpus_nested_conditional_expression": (
        "classifier: NEEDS_MANUAL_REVIEW for nested IIF expressions"
    ),
    "informatica_stress_corpus_rank_sorter_aggregator_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for rank/sorter/aggregator chain"
    ),
    "informatica_stress_corpus_sequence_update_strategy": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "informatica_stress_corpus_star_join_4satellite": (
        "classifier: NEEDS_MANUAL_REVIEW for star join with four satellites"
    ),
    "informatica_stress_corpus_three_sq_two_joiner_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for three source qualifiers and two joiners"
    ),
    "informatica_xml_aggregator_pipeline": (
        "classifier: NEEDS_MANUAL_REVIEW for aggregator pipeline"
    ),
    "informatica_xml_minimal_with_missing_transformation": (
        "parity: explain_gate — export placeholder FROM /* missing_upstream */"
    ),
    "informatica_xml_minimal_with_unsupported": (
        "parity: explain_gate — export placeholder FROM /* missing_upstream */"
    ),
    "informatica_xml_multi_input_union": (
        "classifier: NEEDS_MANUAL_REVIEW for multi-input union"
    ),
    "informatica_xml_multi_target_pipeline": (
        "parity: seed SQL lacks IS_DELETED on dw_core.dim_customers referenced in exported model"
    ),
    "informatica_xml_real_world_complex_pipeline": (
        "parity: missing seeds for dwh.ref_rate_plan_aliases; invalid incremental timestamp SQL"
    ),
    "informatica_xml_sq_user_defined_join_two_tables": (
        "classifier: NEEDS_MANUAL_REVIEW for user-defined join SQ"
    ),
    "informatica_xml_transform_pipeline": (
        "parity: exported SQL references RAW_DATE not present in dbo.src_customers seed columns"
    ),
    "informatica_xml_update_strategy_pipeline": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "orchestration_infa_wf_enterprise_daily_run": (
        "parity: composite enterprise workflow — missing ref seeds, router CTEs, incremental Jinja"
    ),
    "orchestration_infa_wf_enterprise_master_repository": (
        "parity: mega orchestration bundle — many missing upstream placeholders and seed/column gaps"
    ),
    "orchestration_infa_wf_with_nested_worklet": (
        "parity: nested worklet workflow — router CTE int_rtr_high_low and incremental Jinja failures"
    ),
    "orchestration_infa_wrapped_wf_m_aggregator": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped aggregator mapping"
    ),
    "orchestration_infa_wrapped_wf_m_aggregator_multi_groupby": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped multi-groupby aggregator"
    ),
    "orchestration_infa_wrapped_wf_m_deep_lookup_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped deep lookup chain"
    ),
    "orchestration_infa_wrapped_wf_m_filter_router_union_faninout": (
        "parity: explain_gate — materialized table int_rtr_high_low missing after CTE inlining"
    ),
    "orchestration_infa_wrapped_wf_m_informatica_scd_type2": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "orchestration_infa_wrapped_wf_m_long_linear_10stage": (
        "parity: explain_gate — materialized table int_rtr_sev missing after CTE inlining"
    ),
    "orchestration_infa_wrapped_wf_m_lookup_composite_condition": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped composite lookup"
    ),
    "orchestration_infa_wrapped_wf_m_missing_transformation": (
        "parity: explain_gate — export placeholder FROM /* missing_upstream */"
    ),
    "orchestration_infa_wrapped_wf_m_multi_target": (
        "parity: seed SQL lacks IS_DELETED on dw_core.dim_customers referenced in exported model"
    ),
    "orchestration_infa_wrapped_wf_m_multi_union": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped multi-union pipeline"
    ),
    "orchestration_infa_wrapped_wf_m_nested_conditional_expression": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped nested IIF pipeline"
    ),
    "orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped rank/sorter/aggregator chain"
    ),
    "orchestration_infa_wrapped_wf_m_sequence_update_strategy": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped user-defined join SQ"
    ),
    "orchestration_infa_wrapped_wf_m_star_join_4satellite": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped star join with four satellites"
    ),
    "orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain": (
        "classifier: NEEDS_MANUAL_REVIEW for wrapped three-SQ two-joiner chain"
    ),
    "orchestration_infa_wrapped_wf_m_transforms": (
        "parity: exported SQL references RAW_DATE not present in dbo.src_customers seed columns"
    ),
    "orchestration_infa_wrapped_wf_m_update_strategy": (
        "parity: explain_gate — dbt {% if is_incremental() %} Jinja not stripped for DuckDB EXPLAIN"
    ),
    "orchestration_infa_wrapped_wf_m_with_unsupported": (
        "parity: explain_gate — export placeholder FROM /* missing_upstream */"
    ),
}


def _manifest_params():
    for manifest_path in _MANIFESTS:
        corpus_id = manifest_path.parent.name
        reason = _CORPUS_XFAIL.get(corpus_id)
        if reason:
            yield pytest.param(
                manifest_path,
                marks=pytest.mark.xfail(reason=reason, strict=True),
            )
        else:
            yield manifest_path


pytestmark = pytest.mark.skipif(
    not _MANIFESTS,
    reason="Run ingest: python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica",
)


@pytest.mark.parametrize(
    "manifest_path",
    list(_manifest_params()),
    ids=lambda p: p.parent.name,
)
def test_informatica_fixture_corpus_remodels(manifest_path: Path) -> None:
    req = load_corpus_manifest(manifest_path)
    assert req.source_platform == "informatica"
    assert req.raw_dbt_models

    resp = RemodelEngine().remodel(req)
    assert resp.pipeline_id == req.pipeline_id
    assert resp.remodeled_models
    assert len(resp.remodeled_models) == len(req.raw_dbt_models)
    assert resp.status == "success", (
        f"{manifest_path.parent.name}: expected success, got {resp.status} — "
        f"model statuses: {[(m.model_name, m.parity_check.status, m.parity_check.error) for m in resp.remodeled_models]}"
    )


def test_informatica_fixture_tree_has_expected_count() -> None:
    assert len(_MANIFESTS) >= 65


def test_informatica_xfail_allowlist_covers_all_non_success_corpora() -> None:
    """Every corpus that is not expected to succeed must be listed in _CORPUS_XFAIL."""
    from collections import Counter

    status_by_corpus: dict[str, str] = {}
    for manifest_path in _MANIFESTS:
        resp = RemodelEngine().remodel(load_corpus_manifest(manifest_path))
        status_by_corpus[manifest_path.parent.name] = resp.status

    non_success = {k for k, v in status_by_corpus.items() if v != "success"}
    assert non_success == set(_CORPUS_XFAIL.keys()), (
        f"Update _CORPUS_XFAIL: missing={non_success - set(_CORPUS_XFAIL)} "
        f"stale={set(_CORPUS_XFAIL) - non_success}"
    )
    assert Counter(status_by_corpus.values())["success"] == len(_MANIFESTS) - len(_CORPUS_XFAIL)
