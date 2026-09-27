"""Corpus loader prefers raw_models/ for monolithic SQL after layered export."""

from __future__ import annotations

import json
from pathlib import Path

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.physical_decomposer import physical_decompose_batch, write_physical_models


def test_load_corpus_manifest_reads_raw_models_when_models_are_layered(tmp_path: Path) -> None:
    raw_sql = "SELECT 1 AS id FROM {{ source('dbo', 'orders') }}\n"
    (tmp_path / "raw_models").mkdir()
    (tmp_path / "raw_models" / "tgt_orders.sql").write_text(raw_sql, encoding="utf-8")
    write_physical_models(
        physical_decompose_batch(
            [{"model_name": "tgt_orders", "sql": raw_sql, "materialization": "view"}]
        ).models,
        tmp_path,
    )
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "pipeline_id": "p1",
                "source_platform": "informatica",
                "raw_dbt_models": [
                    {"model_name": "tgt_orders", "file": "tgt_orders.sql", "materialization": "view"}
                ],
                "preferences": {"physical_decompose": True},
            }
        ),
        encoding="utf-8",
    )
    request = load_corpus_manifest(tmp_path / "manifest.json")
    assert request.raw_dbt_models[0].sql.strip() == raw_sql.strip()
    assert list((tmp_path / "models").rglob("*.sql"))
    assert not list((tmp_path / "models").glob("*.sql"))
