import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ingest_fixtures_from_studio as ingest  # noqa: E402


def test_ingest_copies_export_bundle(tmp_path: Path):
    studio = tmp_path / "studio"
    export = studio / "exports" / "daily"
    models = export / "models"
    models.mkdir(parents=True)
    manifest = {
        "pipeline_id": "daily_etl_main_active_diagnosis",
        "source_platform": "ssis",
        "raw_dbt_models": [{"model_name": "raw_stg_diagnosis", "file": "raw_stg_diagnosis.sql"}],
        "parity_context": {"seeds_sql": "exports/daily/seeds.sql"},
    }
    (export / "manifest.json").write_text(json.dumps(manifest))
    (models / "raw_stg_diagnosis.sql").write_text("SELECT 1 AS diagnosis_id")
    (export / "seeds.sql").write_text("CREATE TABLE seed_diagnosis AS SELECT 1;")

    dest_root = tmp_path / "remodel"
    ingest.FIXTURES = dest_root / "tests" / "fixtures"
    ingest.ingest_corpus(
        studio,
        "daily_etl_main_corpus",
        ingest.CORPUS_SPECS["daily_etl_main_corpus"],
        compile_missing=False,
    )

    dest = ingest.FIXTURES / "daily_etl_main_corpus"
    assert (dest / "manifest.json").is_file()
    assert (dest / "models" / "raw_stg_diagnosis.sql").is_file()
    assert (dest / "seeds.sql").is_file()
    copied = json.loads((dest / "manifest.json").read_text())
    assert copied["parity_context"]["seeds_sql"] == "tests/fixtures/daily_etl_main_corpus/seeds.sql"

    ingest.FIXTURES = ROOT / "tests" / "fixtures"
    shutil.rmtree(dest_root, ignore_errors=True)
