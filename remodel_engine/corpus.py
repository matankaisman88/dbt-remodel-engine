"""Load corpus manifests from tests/fixtures (etl_to_dbt-style export layout)."""

from __future__ import annotations

import json
from pathlib import Path

from remodel_engine.schema import RawDbtModel, RemodelRequest


def load_corpus_manifest(path: Path) -> RemodelRequest:
    data = json.loads(path.read_text())
    models_dir = path.parent / "models"
    raw_models: list[RawDbtModel] = []
    for entry in data["raw_dbt_models"]:
        sql = entry.get("sql")
        if not sql and entry.get("file"):
            sql = (models_dir / entry["file"]).read_text()
        raw_models.append(
            RawDbtModel(
                model_name=entry["model_name"],
                sql=sql or "",
                materialization=entry.get("materialization", "view"),
            )
        )
    return RemodelRequest(
        pipeline_id=data["pipeline_id"],
        source_platform=data["source_platform"],
        raw_dbt_models=raw_models,
        preferences=data.get("preferences", {}),
        legacy_targets=data.get("legacy_targets", {}),
        lookup_rewrites=data.get("lookup_rewrites", []),
        parity_context=data.get("parity_context"),
        legacy_transformations_count=data.get("legacy_transformations_count"),
        legacy_graph_nodes=data.get("legacy_graph", {}).get("nodes", []),
        legacy_graph_edges=data.get("legacy_graph", {}).get("edges", []),
    )
