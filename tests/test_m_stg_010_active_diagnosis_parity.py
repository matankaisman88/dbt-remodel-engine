"""Regression: m_STG_010 physical decompose parity on _tmp_compile bundle."""

from pathlib import Path

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "_tmp_compile"
MANIFEST = BUNDLE / "manifest.json"

pytestmark = __import__("pytest").mark.skipif(
    not MANIFEST.is_file(),
    reason="_tmp_compile/m_STG_010 bundle required",
)


def test_m_stg_010_active_diagnosis_marts_parity() -> None:
    req = load_corpus_manifest(MANIFEST)
    assert req.preferences.physical_decompose is True
    resp = RemodelEngine().remodel(req)
    marts = [
        m
        for m in resp.remodeled_models
        if m.source_raw_model is not None
    ]
    assert len(marts) == 3
    assert all(m.parity_check.status == "pass" for m in marts)
    assert resp.status in {"success", "needs_manual_review"}


def test_m_stg_010_benign_intermediate_expression_models_parity_pass() -> None:
    req = load_corpus_manifest(MANIFEST)
    resp = RemodelEngine().remodel(req)
    benign = [
        m
        for m in resp.remodeled_models
        if m.layer == "intermediate"
        and not m.flagged
        and "projection/filter/expression" in m.classification_reason
    ]
    assert benign, "expected decomposed expression intermediate models"
    assert all(m.parity_check.status == "pass" for m in benign)
