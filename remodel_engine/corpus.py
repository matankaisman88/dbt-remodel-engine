"""Load corpus manifests from tests/fixtures (etl_to_dbt-style export layout)."""

from __future__ import annotations

import json
from pathlib import Path

from remodel_engine.schema import RawDbtModel, RemodelRequest


def _resolve_parity_context(
    parity_context: dict | None,
    manifest_path: Path,
) -> dict | None:
    if not parity_context:
        return None
    ctx = dict(parity_context)
    seeds_ref = ctx.get("seeds_sql")
    if not isinstance(seeds_ref, str) or not seeds_ref.strip().endswith(".sql"):
        return ctx
    corpus_dir = manifest_path.parent
    candidates = [
        Path(seeds_ref),
        corpus_dir / Path(seeds_ref).name,
        corpus_dir / "seeds.sql",
    ]
    if seeds_ref.replace("\\", "/").startswith("tests/fixtures/"):
        repo_root = manifest_path
        for _ in range(6):
            if (repo_root / "tests" / "fixtures").is_dir():
                candidates.append(repo_root / seeds_ref.replace("\\", "/"))
                break
            if repo_root.parent == repo_root:
                break
            repo_root = repo_root.parent
    for candidate in candidates:
        if candidate.is_file():
            ctx["seeds_sql"] = str(candidate.resolve())
            break
    return ctx


def _read_raw_model_sql(corpus_dir: Path, entry: dict) -> str:
    """Load monolithic SQL from ``raw_models/`` (layered export) or legacy ``models/*.sql``."""
    inline = entry.get("sql")
    if isinstance(inline, str) and inline.strip():
        return inline
    file_name = str(entry.get("file") or "").strip()
    if not file_name:
        return ""
    stem = Path(file_name).name
    for candidate in (
        corpus_dir / "raw_models" / stem,
        corpus_dir / "models" / file_name,
        corpus_dir / "models" / stem,
    ):
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    return ""


def load_corpus_manifest(path: Path) -> RemodelRequest:
    data = json.loads(path.read_text())
    corpus_dir = path.parent
    raw_models: list[RawDbtModel] = []
    for entry in data["raw_dbt_models"]:
        sql = _read_raw_model_sql(corpus_dir, entry)
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
        shadowed_lookup_renames=data.get("shadowed_lookup_renames", []),
        entity_consolidations=data.get("entity_consolidations", []),
        parity_context=_resolve_parity_context(data.get("parity_context"), path),
        legacy_transformations_count=data.get("legacy_transformations_count"),
        legacy_graph_nodes=data.get("legacy_graph", {}).get("nodes", []),
        legacy_graph_edges=data.get("legacy_graph", {}).get("edges", []),
    )
