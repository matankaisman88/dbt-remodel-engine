"""Compile Informatica fixtures from ETL-Migration-Studio and run the remodel engine."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import informatica_fixtures as infa  # noqa: E402
import ingest_fixtures_from_studio as ingest  # noqa: E402
from studio_compile_export import compile_bundle  # noqa: E402

from remodel_engine.corpus import load_corpus_manifest  # noqa: E402
from remodel_engine.engine import RemodelEngine  # noqa: E402


def _resolve_studio() -> Path | None:
    return ingest.resolve_studio_root(None)


_STUDIO = _resolve_studio()
_INFORMATICA_XML = (
    list(infa.iter_informatica_fixture_paths(_STUDIO)) if _STUDIO is not None else []
)

pytestmark = pytest.mark.skipif(
    _STUDIO is None or not _INFORMATICA_XML,
    reason="ETL-Migration-Studio with Informatica fixtures required (sibling repo or env)",
)


def _ids(path: Path) -> str:
    assert _STUDIO is not None
    return infa.pipeline_id_for_fixture(_STUDIO, path)


@pytest.mark.parametrize("xml_path", _INFORMATICA_XML, ids=_ids)
def test_informatica_fixture_compiles_and_remodels(xml_path: Path, tmp_path: Path) -> None:
    assert _STUDIO is not None
    pipeline_id = infa.pipeline_id_for_fixture(_STUDIO, xml_path)
    bundle_dir = tmp_path / pipeline_id
    compile_bundle(_STUDIO, xml_path, pipeline_id, bundle_dir)

    manifest = bundle_dir / "manifest.json"
    assert manifest.is_file()
    assert (bundle_dir / "models").is_dir()
    assert list((bundle_dir / "models").glob("*.sql"))
    assert (bundle_dir / "seeds.sql").is_file()

    req = load_corpus_manifest(manifest)
    assert req.pipeline_id == pipeline_id
    assert req.source_platform == "informatica"
    assert req.raw_dbt_models

    resp = RemodelEngine().remodel(req)
    assert resp.pipeline_id == pipeline_id
    assert resp.remodeled_models
    assert len(resp.remodeled_models) == len(req.raw_dbt_models)
    assert resp.status in {"success", "needs_manual_review", "failed_parity"}


def test_informatica_discovery_count_matches_studio() -> None:
    assert _STUDIO is not None
    paths = infa.iter_informatica_fixture_paths(_STUDIO)
    plans = ingest.discover_informatica_ingest_plans(_STUDIO, None, set())
    assert len(plans) == len(paths)
    assert len(paths) >= 65
