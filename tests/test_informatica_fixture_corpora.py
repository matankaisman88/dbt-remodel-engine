"""Remodel tests against committed corpora under tests/fixtures/informatica/."""

from __future__ import annotations

from pathlib import Path

import pytest

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine

INFORMATICA_FIXTURES = Path(__file__).parent / "fixtures" / "informatica"

_MANIFESTS = sorted(
    p for p in INFORMATICA_FIXTURES.glob("*/manifest.json") if p.is_file()
)

pytestmark = pytest.mark.skipif(
    not _MANIFESTS,
    reason="Run ingest: python scripts/ingest_fixtures_from_studio.py --compile-missing --all-informatica",
)


@pytest.mark.parametrize(
    "manifest_path",
    _MANIFESTS,
    ids=lambda p: p.parent.name,
)
def test_informatica_fixture_corpus_remodels(manifest_path: Path) -> None:
    req = load_corpus_manifest(manifest_path)
    assert req.source_platform == "informatica"
    assert req.raw_dbt_models

    resp = RemodelEngine().remodel(req)
    assert resp.pipeline_id == req.pipeline_id
    assert resp.remodeled_models
    assert len(resp.remodeled_models) == len(req.raw_dbt_models)
    assert resp.status in {"success", "needs_manual_review", "failed_parity"}


def test_informatica_fixture_tree_has_expected_count() -> None:
    assert len(_MANIFESTS) >= 65
