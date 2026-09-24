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

- `wwi_corpus/` — Wide World Importers–style star schema export
- `daily_etl_main_corpus/` — DailyETLMain / active diagnosis Informatica-style export

These follow the **read-only** `etl_to_dbt` raw model export shape (`manifest.json` + `models/*.sql` + DuckDB `seeds.sql`). Refresh from ETL-Migration-Studio:

```bash
python scripts/ingest_fixtures_from_studio.py --compile-missing
```

## API

```bash
uvicorn remodel_engine.api:app --reload
```

`POST /api/v1/remodel` — request/response schema in `remodel_engine/schema.py` (matches the architecture spec).

## Verification report

`remodeling_verification_report.md` lists **every** model’s layer, parity status, CTE merges, and unfiltered failure / `NEEDS_MANUAL_REVIEW` lists. A model is never marked pass without a successful parity gate when `parity_context` is supplied.
