#!/usr/bin/env python3
"""Compile a Studio legacy artifact into a dbt-remodel-engine fixture export bundle."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]


def _graph_to_legacy(nodes, edges, *, prefix: str) -> tuple[list[dict], list[dict]]:
    out_nodes: list[dict] = []
    for node in nodes:
        node_id = f"{prefix}{node.id}" if prefix else node.id
        out_nodes.append(
            {
                "id": node_id,
                "label": node.label,
                "meta": {"type": node.widget_type},
            }
        )
    out_edges: list[dict] = []
    for edge in edges:
        src = f"{prefix}{edge.source}" if prefix else edge.source
        tgt = f"{prefix}{edge.target}" if prefix else edge.target
        out_edges.append({"source": src, "target": tgt})
    return out_nodes, out_edges


def _model_stem(relative_path: str) -> str:
    return Path(relative_path).name.removesuffix(".sql")


def _reset_dir(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def _write_layered_models(out_dir: Path, raw_entries: list[dict], raw_models_dir: Path) -> None:
    """Decompose monoliths and write ``models/staging|intermediate|marts/*.sql``."""
    if str(ENGINE_ROOT) not in sys.path:
        sys.path.insert(0, str(ENGINE_ROOT))

    from remodel_engine.layer_synthesizer import LegacyTargetMeta
    from remodel_engine.physical_decomposer import physical_decompose_batch, write_physical_models

    raw_payload = [
        {
            "model_name": entry["model_name"],
            "sql": (raw_models_dir / entry["file"]).read_text(encoding="utf-8"),
            "materialization": entry.get("materialization", "view"),
        }
        for entry in raw_entries
    ]
    legacy_targets = {
        entry["model_name"]: LegacyTargetMeta(
            target_name=str(entry.get("target_name") or entry["model_name"]),
            last_transformation_type=str(entry.get("last_transformation_type") or "target"),
        )
        for entry in raw_entries
        if entry.get("is_legacy_target")
    }
    decomposed = physical_decompose_batch(raw_payload, legacy_targets=legacy_targets)
    models_dir = _reset_dir(out_dir / "models")
    written = write_physical_models(decomposed.models, out_dir)
    if not written:
        raise RuntimeError(f"physical_decompose produced no model files under {models_dir}")


def compile_bundle(
    studio_root: Path,
    source_file: Path,
    pipeline_id: str,
    out_dir: Path,
    *,
    dialect: str = "duckdb",
) -> None:
    studio_root = studio_root.resolve()
    source_file = source_file.resolve()
    out_dir = out_dir.resolve()

    if str(studio_root) not in sys.path:
        sys.path.insert(0, str(studio_root))

    from etl_to_dbt.ui.server.dbt_output_sync import build_duckdb_init_sql
    from etl_to_dbt.ui.server.remodel_adapter import studio_source_platform
    from etl_to_dbt.ui.server.service import (
        _require_session,
        _source_xml_for_mapping,
        clear_sessions,
        convert_pipeline,
        graph_for_mapping,
        parse_pipeline,
    )

    clear_sessions()
    raw = source_file.read_bytes()
    parsed = parse_pipeline(content=raw, filename=source_file.name)
    session = _require_session(parsed.pipeline_id)
    converted = convert_pipeline(session.pipeline_id, dialect)

    raw_models_dir = _reset_dir(out_dir / "raw_models")

    raw_entries: list[dict] = []
    used_names: set[str] = set()
    legacy_nodes: list[dict] = []
    legacy_edges: list[dict] = []
    legacy_targets: dict[str, dict[str, str]] = {}

    pieces_by_name = {piece.mapping_name: piece for piece in converted.mappings}
    multi_mapping = len([m for m in session.mappings if not m.is_external_reference]) > 1

    for mapping in session.mappings:
        if mapping.is_external_reference:
            continue
        piece = pieces_by_name.get(mapping.name)
        if piece is None or not piece.models:
            continue
        graph = graph_for_mapping(mapping, _source_xml_for_mapping(session, mapping))
        prefix = f"{mapping.name}:" if multi_mapping else ""
        nodes, edges = _graph_to_legacy(graph.nodes, graph.edges, prefix=prefix)
        legacy_nodes.extend(nodes)
        legacy_edges.extend(edges)

        for rel_path, sql in piece.models.items():
            stem = _model_stem(rel_path)
            model_name = stem
            if model_name in used_names:
                n = 2
                while f"{stem}_{n}" in used_names:
                    n += 1
                model_name = f"{stem}_{n}"
            used_names.add(model_name)
            file_name = f"{model_name}.sql"
            (raw_models_dir / file_name).write_text(sql, encoding="utf-8")
            materialization = "table" if "{{ config(materialized='table'" in sql.lower() else "view"
            is_legacy_target = (
                model_name.startswith("raw_tgt_")
                or stem.startswith("tgt_")
                or stem.startswith("shortcut_to")
            )
            raw_entries.append(
                {
                    "model_name": model_name,
                    "file": file_name,
                    "materialization": materialization,
                    "is_legacy_target": is_legacy_target,
                    "target_name": stem.removeprefix("tgt_").upper(),
                    "last_transformation_type": "target",
                }
            )
            if is_legacy_target:
                legacy_targets[model_name] = {
                    "target_name": stem.removeprefix("tgt_").upper(),
                    "last_transformation_type": "target",
                }

    if not raw_entries:
        raise RuntimeError(f"No dbt models produced from {source_file}")

    _write_layered_models(out_dir, raw_entries, raw_models_dir)

    merged_sources_yml = None
    for piece in converted.mappings:
        if piece.sources_yml:
            merged_sources_yml = piece.sources_yml
            break

    seeds_sql = build_duckdb_init_sql(
        session.mappings,
        pieces=converted.mappings,
        merged_sources_yml=merged_sources_yml,
    )
    (out_dir / "seeds.sql").write_text(seeds_sql, encoding="utf-8")

    manifest = {
        "pipeline_id": pipeline_id,
        "source_platform": studio_source_platform(session.source_engine),
        "legacy_transformations_count": len(legacy_nodes),
        "legacy_graph": {"nodes": legacy_nodes, "edges": legacy_edges},
        "legacy_targets": legacy_targets,
        "preferences": {
            "target_pattern": "star_schema",
            "collapse_ctes": True,
            "modernize_window_functions": False,
            "physical_decompose": True,
        },
        "lookup_rewrites": [],
        "shadowed_lookup_renames": [],
        "parity_context": {
            "seeds_sql": "seeds.sql",
            "source_table_map": {},
            "model_table_map": {},
        },
        "raw_dbt_models": [
            {
                "model_name": entry["model_name"],
                "file": entry["file"],
                "materialization": entry["materialization"],
            }
            for entry in raw_entries
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--studio-root", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True, help="Legacy .dtsx / .xml file")
    parser.add_argument("--pipeline-id", required=True, help="pipeline_id for remodel manifest")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dialect", default="duckdb")
    args = parser.parse_args()

    if not args.source.is_file():
        print(f"Source file not found: {args.source}", file=sys.stderr)
        return 2
    if not args.studio_root.is_dir():
        print(f"Studio root not found: {args.studio_root}", file=sys.stderr)
        return 2

    try:
        compile_bundle(
            args.studio_root,
            args.source,
            args.pipeline_id,
            args.out_dir,
            dialect=args.dialect,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    manifest = args.out_dir / "manifest.json"
    if not manifest.is_file():
        print(f"Compile finished but {manifest} is missing", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
