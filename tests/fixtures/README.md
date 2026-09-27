# Corpus fixtures

Manifest + SQL layout matches the **read-only** export shape from `etl_to_dbt` in ETL Migration Studio:

- `manifest.json` — pipeline metadata, legacy graph, `legacy_targets`, parity seed maps
- `models/*.sql` — raw 1:1 dbt models (`{{ source() }}` / `{{ ref() }}`)
- `seeds.sql` — DuckDB seed tables for model-level parity

| Directory | Origin |
| --- | --- |
| `wwi_corpus/` | Curated WWI star-schema remodel corpus (hand-maintained) |
| `daily_etl_main_corpus/` | Curated active-diagnosis remodel corpus (hand-maintained) |
| `informatica/<pipeline_id>/` | Informatica XML compiled from Studio (~70 corpora) |

See `informatica/README.md` for the Informatica tree layout.

## Refresh from ETL-Migration-Studio

```bash
export ETL_MIGRATION_STUDIO_ROOT=../ETL-Migration-Studio

# Curated defaults (SSIS DailyETLMain + real_world Informatica XML)
python scripts/ingest_fixtures_from_studio.py --compile-missing

# All Informatica XML corpora into tests/fixtures/informatica/
python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica

# Preview without deleting/writing
python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica --dry-run

pytest
python scripts/generate_verification_report.py
```

`--compile-missing` invokes `scripts/studio_compile_export.py` (Studio `parse_pipeline` + `convert_pipeline`).

## Tests

| Command | What it exercises |
| --- | --- |
| `pytest tests/test_informatica_fixture_corpora.py` | Remodel every committed corpus under `informatica/` |
| `pytest tests/test_informatica_studio_remodel.py` | Compile from a local Studio checkout, then remodel |
| `pytest tests/test_corpus_integration.py` | Curated `wwi_corpus` and `daily_etl_main_corpus` |

Provenance for the last full ingest: `.fixture_provenance.json`.
