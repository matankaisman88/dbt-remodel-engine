# Informatica corpora (compiled from ETL-Migration-Studio)

Each subdirectory is one Informatica XML fixture compiled to the remodel export shape:

- `manifest.json`
- `models/*.sql`
- `seeds.sql`

Refresh everything (~70 corpora):

```bash
python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica
```

Run remodel tests against this tree only (no Studio checkout required):

```bash
pytest tests/test_informatica_fixture_corpora.py
```

Provenance for the last ingest: `tests/fixtures/.fixture_provenance.json`.
