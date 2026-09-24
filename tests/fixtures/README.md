# Corpus fixtures

Manifest + SQL layout matches the **read-only** export shape from `etl_to_dbt` in ETL Migration Studio:

- `manifest.json` — pipeline metadata, legacy graph, `legacy_targets`, parity seed maps
- `models/*.sql` — raw 1:1 dbt models (`{{ source() }}` / `{{ ref() }}`)
- `seeds.sql` — DuckDB seed tables for model-level parity

| Directory | Origin |
| --- | --- |
| `wwi_corpus/` | Wide World Importers star-schema Informatica-style pipeline |
| `daily_etl_main_corpus/` | DailyETLMain active diagnosis pipeline |

Refresh from a local ETL-Migration-Studio checkout:

```bash
# sibling repo (default) or explicit path
export ETL_MIGRATION_STUDIO_ROOT=../ETL-Migration-Studio
python scripts/ingest_fixtures_from_studio.py --compile-missing
pytest
python scripts/generate_verification_report.py
```

`--compile-missing` runs `python -m etl_to_dbt.api` against:

- `tests/fixtures/ssis/official/DailyETLMain.dtsx` → `daily_etl_main_corpus/`
- Informatica WWI / complex pipeline XML → `wwi_corpus/`

Provenance is recorded in `.fixture_provenance.json` after ingest.
