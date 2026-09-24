# Corpus fixtures

Manifest + SQL layout matches the **read-only** export shape from `etl_to_dbt` in ETL Migration Studio:

- `manifest.json` — pipeline metadata, legacy graph, `legacy_targets`, parity seed maps
- `models/*.sql` — raw 1:1 dbt models (`{{ source() }}` / `{{ ref() }}`)
- `seeds.sql` — DuckDB seed tables for model-level parity

| Directory | Origin |
| --- | --- |
| `wwi_corpus/` | Wide World Importers star-schema Informatica-style pipeline |
| `daily_etl_main_corpus/` | DailyETLMain active diagnosis pipeline |

Replace these trees with a fresh copy from `ETL-Migration-Studio-main` to re-run verification against your local exports.
