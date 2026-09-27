import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ingest_fixtures_from_studio as ingest  # noqa: E402


def _write_export_bundle(
    base: Path,
    pipeline_id: str,
    model_name: str,
    *,
    seeds: bool = True,
) -> Path:
    export = base
    models = export / "models"
    models.mkdir(parents=True, exist_ok=True)
    manifest = {
        "pipeline_id": pipeline_id,
        "source_platform": "test",
        "raw_dbt_models": [{"model_name": model_name, "file": f"{model_name}.sql"}],
        "parity_context": {"seeds_sql": str(export / "seeds.sql")},
    }
    (export / "manifest.json").write_text(json.dumps(manifest))
    (models / f"{model_name}.sql").write_text("SELECT 1 AS id")
    if seeds:
        (export / "seeds.sql").write_text("CREATE TABLE seed AS SELECT 1;")
    return export


def test_ingest_copies_export_bundle(tmp_path: Path):
    studio = tmp_path / "studio"
    export = studio / "exports" / "daily"
    _write_export_bundle(export, "daily_etl_main_active_diagnosis", "raw_stg_diagnosis")

    dest_root = tmp_path / "remodel"
    ingest.FIXTURES = dest_root / "tests" / "fixtures"
    plan = ingest.discover_export_corpora(studio, None)[0]
    assert plan.corpus_name == "daily_etl_main_active_diagnosis"
    ingest.ingest_corpus(studio, plan, compile_missing=False)

    dest = ingest.FIXTURES / "daily_etl_main_active_diagnosis"
    assert (dest / "manifest.json").is_file()
    assert (dest / "models" / "raw_stg_diagnosis.sql").is_file()
    assert (dest / "seeds.sql").is_file()
    copied = json.loads((dest / "manifest.json").read_text())
    assert (
        copied["parity_context"]["seeds_sql"]
        == "tests/fixtures/daily_etl_main_active_diagnosis/seeds.sql"
    )

    ingest.FIXTURES = ROOT / "tests" / "fixtures"
    shutil.rmtree(dest_root, ignore_errors=True)


def test_discover_export_corpora_finds_all_valid_manifests(tmp_path: Path):
    studio = tmp_path / "studio"
    _write_export_bundle(
        studio / "a" / "wwi_sales_star",
        "wwi_sales_star",
        "stg_sales",
    )
    _write_export_bundle(
        studio / "b" / "daily_etl_main_active_diagnosis",
        "daily_etl_main_active_diagnosis",
        "raw_stg_diagnosis",
    )
    _write_export_bundle(
        studio / "c" / "third_pipeline",
        "third/custom pipeline",
        "stg_third",
    )
    noise = studio / "noise"
    noise.mkdir(parents=True)
    (noise / "manifest.json").write_text(json.dumps({"pipeline_id": "no_models"}))

    plans = ingest.discover_export_corpora(studio, None)
    assert len(plans) == 3
    assert [p.corpus_name for p in plans] == [
        "daily_etl_main_active_diagnosis",
        "third_custom_pipeline",
        "wwi_sales_star",
    ]
    assert {p.pipeline_id for p in plans} == {
        "wwi_sales_star",
        "daily_etl_main_active_diagnosis",
        "third/custom pipeline",
    }


def test_discover_export_corpora_pipeline_id_filter(tmp_path: Path):
    studio = tmp_path / "studio"
    _write_export_bundle(studio / "one", "pipeline_one", "m1")
    _write_export_bundle(studio / "two", "pipeline_two", "m2")

    plans = ingest.discover_export_corpora(studio, {"pipeline_one"})
    assert len(plans) == 1
    assert plans[0].pipeline_id == "pipeline_one"


def test_discover_skips_node_modules_and_git(tmp_path: Path):
    studio = tmp_path / "studio"
    _write_export_bundle(studio / "ok", "visible", "m_ok")
    _write_export_bundle(studio / "node_modules" / "pkg", "hidden_nm", "m_nm")
    _write_export_bundle(studio / ".git" / "artifacts", "hidden_git", "m_git")

    plans = ingest.discover_export_corpora(studio, None)
    assert len(plans) == 1
    assert plans[0].pipeline_id == "visible"


def test_ingest_multiple_discovered_corpora(tmp_path: Path):
    studio = tmp_path / "studio"
    for i, pid in enumerate(("alpha_pipe", "beta_pipe", "gamma_pipe"), start=1):
        _write_export_bundle(studio / f"export_{i}", pid, f"model_{i}")

    dest_root = tmp_path / "remodel"
    ingest.FIXTURES = dest_root / "tests" / "fixtures"
    plans = ingest.discover_export_corpora(studio, None)
    assert len(plans) == 3

    provenance = []
    for plan in plans:
        provenance.append(ingest.ingest_corpus(studio, plan, compile_missing=False))

    assert len(provenance) == 3
    for entry in provenance:
        dest = ingest.FIXTURES / entry["corpus"]
        assert (dest / "manifest.json").is_file()
        assert entry["model_sql_files"] == 1

    ingest.FIXTURES = ROOT / "tests" / "fixtures"
    shutil.rmtree(dest_root, ignore_errors=True)


def test_sanitize_corpus_name():
    assert ingest.sanitize_corpus_name("third/custom pipeline") == "third_custom_pipeline"
    assert ingest.sanitize_corpus_name("  WWI.Sales  ") == "wwi.sales"


def test_discover_informatica_plans_from_temp_xml(tmp_path: Path):
    studio = tmp_path / "studio"
    for name in ("alpha.xml", "beta.xml", "gamma.xml"):
        folder = studio / "fixtures" / "informatica_xml"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text("<POWERMART></POWERMART>")

    plans = ingest.discover_informatica_ingest_plans(studio, None, set())
    assert len(plans) == 3
    assert all(p.fixture_namespace == "informatica" for p in plans)
    assert {p.pipeline_id for p in plans} == {
        "informatica_xml_alpha",
        "informatica_xml_beta",
        "informatica_xml_gamma",
    }


def test_compile_defaults_apply_when_studio_has_no_exports(tmp_path: Path):
    studio = tmp_path / "studio"
    studio.mkdir()
    (studio / "tests" / "fixtures" / "ssis" / "official").mkdir(parents=True)
    dtsx = studio / "tests" / "fixtures" / "ssis" / "official" / "DailyETLMain.dtsx"
    dtsx.write_text("<DTS:Executable />")

    defaults = tmp_path / "defaults.json"
    defaults.write_text(
        json.dumps(
            {
                "corpora": [
                    {
                        "pipeline_id": "daily_etl_main_active_diagnosis",
                        "compile_inputs": ["tests/fixtures/ssis/official/DailyETLMain.dtsx"],
                    }
                ]
            }
        )
    )
    ingest.STUDIO_COMPILE_DEFAULTS = defaults
    plans = ingest.discover_compile_only_plans(
        studio,
        compile_inputs_glob=None,
        pipeline_ids=None,
        existing_pipeline_ids=set(),
    )
    assert len(plans) == 1
    assert plans[0].pipeline_id == "daily_etl_main_active_diagnosis"
    ingest.STUDIO_COMPILE_DEFAULTS = ROOT / "scripts" / "studio_compile_defaults.json"
