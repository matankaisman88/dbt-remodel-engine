from pathlib import Path

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine

FIXTURES = Path(__file__).parent / "fixtures"


def test_wwi_corpus_runs_end_to_end():
    req = load_corpus_manifest(FIXTURES / "wwi_corpus" / "manifest.json")
    resp = RemodelEngine().remodel(req)
    assert resp.pipeline_id == "wwi_sales_star"
    assert resp.remodeled_models
    assert resp.after_graph.nodes


def test_daily_etl_main_corpus_runs_end_to_end():
    req = load_corpus_manifest(FIXTURES / "daily_etl_main_corpus" / "manifest.json")
    resp = RemodelEngine().remodel(req)
    assert resp.pipeline_id == "daily_etl_main_active_diagnosis"
