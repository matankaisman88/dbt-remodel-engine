# dbt-remodel-engine

Headless **Phase A** remodeling library for 1:1 dbt SQL exported from legacy ETL migrations (Informatica / SSIS via `etl_to_dbt`). It classifies models into staging / intermediate / marts layers, applies guarded refactor rules, and verifies **result equivalence** per model on DuckDB.

There is **no UI** in this repository.

## Modules

| Module | Spec section |
| --- | --- |
| `remodel_engine/layer_synthesizer.py` | Layer rules (staging → intermediate → marts → fail-closed) |
| `remodel_engine/refactor_rules.py` | CTE merge safety gates, lookup/window rewrite |
| `remodel_engine/parity_gate.py` | Model-level parity (row count, null pattern, EXCEPT diff) |
| `remodel_engine/api.py` | `POST /api/v1/remodel` |
| `remodel_engine/engine.py` | End-to-end orchestration |

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
