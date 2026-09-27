# dbt-remodel-engine

Headless **Phase A** remodeling library for 1:1 dbt SQL exported from legacy ETL migrations (Informatica / SSIS via `etl_to_dbt`). It classifies models into staging / intermediate / marts layers, applies guarded refactor rules, and verifies **result equivalence** per model on DuckDB.

There is **no UI** in this repository.

## Architecture (v2.x)

### CTAS star-shadowing harmonization

Physical decomposition materializes models with `CREATE TABLE AS`. Analytical engines (DuckDB, Snowflake, BigQuery) then disambiguate duplicate column names (e.g. `COL` and `COL_1`) when a bind `SELECT` lists `join.COL AS COL` before `base.*`, while monolithic inline CTEs resolve `COALESCE(<COL>_DIM, <COL>)` using Informatica-style projection order.

`remodel_engine/star_shadowing.py` harmonizes bindings when `physical_decompose` is enabled. Rewrites use **sqlglot** AST transforms (`harmonize_bind_select_ast`, `rewrite_coalesce_bindings_ast`) instead of regex: SQL is parsed with `sqlglot.parse_one(..., read="duckdb")` after swapping `{{ ... }}` Jinja for parse placeholders (restored on output). On parse failure, the original SQL is returned unchanged.

- **Shadowed join columns:** Drops redundant `join.COL AS COL` projections when trailing `base.*` shadows the same name and `base.COL` already appears elsewhere in the bind list, so downstream references bind to the base attribute without CTAS suffix drift.
- **Rate-plan lookups:** For `lkp_lkp_ref_dim_rate_plan` binds, renames the join PK to `RATE_PLAN_PK_LKP`. Downstream models expand `COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK)` to `COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK_LKP, RATE_PLAN_PK)` **only when** the immediate upstream ref already exposes `RATE_PLAN_PK_LKP` (parity materialization introspects ref column names per model in topological order).
- **Renamed lookups:** Intentionally distinct aliases (e.g. `DIAGNOSIS_PK_LOOKUP`) are left unchanged.

When `parity_context` is absent, star-shadowing runs once per model without upstream column gating (COALESCE expansion requires `renamed_column_present=True` and a matching `shadowed_lookup_renames` manifest entry).

Together this preserves data and null-pattern parity across decomposed models without hand-editing exported SQL.

### Rule #2 risk assessment and layer synthesis

Layer classification (`layer_synthesizer.py`) and parity grain gating (`sql_analysis.py`, `parity_gate.py`) are decoupled to eliminate false `needs_manual_review` flags:

- **Layer routing:** Scalar expressions, projections, and standard filters on `ref()` upstreams classify as `intermediate` when rule #2 matches (`refactor_rules.assess_rule2`).
- **Benign transforms:** Single-ref work, equijoins, and standard deduplication (`ROW_NUMBER() = 1` / `QUALIFY`) pass grain evaluation without manual review.
- **Active intermediate parity:** Unflagged decomposed intermediate models run pre- vs post-refactor parity checks (`parity_check.status == "pass"`), eliminating ambiguous `skipped` states in downstream UIs.
- **Targeted grain gating:** Manual review is strictly reserved for grain-altering constructs: top-level `GROUP BY`, asymmetric joins (`FULL` / `RIGHT` / `CROSS`), non-equi or fuzzy join predicates, unpinned window functions, and complex `CASE` (deep nesting or subqueries in `WHEN` / `THEN` via `has_complex_case`).

For SQL with `ref()` upstreams, the parity gate delegates grain checks to the unified `assess_rule2` assessment; other models use `assess_grain_risk` directly.

### Integration boundaries (headless engine)

This repository is a **headless compiler and transformation library** only:

- **In scope:** Decomposed, parity-validated dbt SQL layers (`staging`, `intermediate`, `marts`), refactor rules, and the remodel HTTP API.
- **Out of scope:** Orchestration DAG generation (e.g. Airflow `--select +<model>` upstream materialization) and execution-scope guards (blocking non-transformation workflows, sessions, or SSIS control flow). Those belong in consuming clients and API orchestration layers (e.g. ETL-Migration-Studio).

## Modules

| Module | Role |
| --- | --- |
| `remodel_engine/engine.py` | End-to-end orchestration (decompose → refactor → classify → parity) |
| `remodel_engine/physical_decomposer.py` | Split monolithic SQL into layered physical models with `{{ ref() }}` linkage |
| `remodel_engine/star_shadowing.py` | CTAS star-shadow harmonization via sqlglot AST (bind `SELECT` prune/rename + gated COALESCE rewrite) |
| `remodel_engine/sql_analysis.py` | Static SQL analysis (refs/sources, CTE parse, grain-risk heuristics) |
| `remodel_engine/layer_synthesizer.py` | Layer rules (staging → intermediate → marts → fail-closed) |
| `remodel_engine/refactor_rules.py` | CTE merge safety gates, lookup/window rewrite, rule #2 assessment |
| `remodel_engine/parity_gate.py` | Model-level parity (row count, null pattern, EXCEPT diff) |
| `remodel_engine/api.py` | `POST /api/v1/remodel` |

## Install

```bash
pip install -e ".[dev]"
```

## Tests & corpora

```bash
pytest
python scripts/generate_verification_report.py
```

Corpus manifests live under `tests/fixtures/`:

| Path | Description |
| --- | --- |
| `wwi_corpus/` | Curated WWI star-schema remodel corpus (hand-maintained) |
| `daily_etl_main_corpus/` | Curated active-diagnosis remodel corpus (hand-maintained) |
| `informatica/<pipeline_id>/` | ~70 Informatica XML corpora compiled from ETL-Migration-Studio |

Each corpus uses the **read-only** `etl_to_dbt` export shape: `manifest.json`, `models/*.sql`, and DuckDB `seeds.sql`.

Informatica-only remodel regression (no Studio checkout required):

```bash
pytest tests/test_informatica_fixture_corpora.py
```

### Refresh fixtures from ETL-Migration-Studio

Set `ETL_MIGRATION_STUDIO_ROOT` or clone the sibling repo at `../ETL-Migration-Studio`.

```bash
# Curated SSIS + Informatica defaults (see scripts/studio_compile_defaults.json)
python scripts/ingest_fixtures_from_studio.py --compile-missing

# All Informatica XML under Studio fixtures/ → tests/fixtures/informatica/
python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica

# List plans without writing
python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica --dry-run
```

Discovery scans Studio for pre-built export bundles (`manifest.json` with `models/` or `raw_dbt_models`). When none exist, `--compile-missing` runs `scripts/studio_compile_export.py` (Studio `parse_pipeline` + `convert_pipeline`).

Optional filters: `--pipeline-id`, `--compile-inputs-glob`, `--studio-root`.

Provenance: `tests/fixtures/.fixture_provenance.json` after ingest.

## API

```bash
uvicorn remodel_engine.api:app --reload
```

`POST /api/v1/remodel` — request/response schema in `remodel_engine/schema.py` (matches the architecture spec).

### Running via Docker

For consumer repos that run dependencies via docker-compose (without local engine development):

```bash
docker build -t dbt-remodel-engine .
docker run -p 8001:8001 dbt-remodel-engine
```

The service listens on port **8001**. Liveness: `GET /health` → `{"status":"ok"}`.

## Verification report

`remodeling_verification_report.md` lists **every** corpus and model’s layer, parity status, CTE merges, and unfiltered failure / `NEEDS_MANUAL_REVIEW` lists. Corpora are discovered from all `tests/fixtures/**/manifest.json` paths. A model is never marked pass without a successful parity gate when `parity_context` is supplied.
