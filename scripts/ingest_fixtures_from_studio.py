#!/usr/bin/env python3
"""Copy real etl_to_dbt export bundles from ETL-Migration-Studio into tests/fixtures/."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"

CORPUS_SPECS: dict[str, dict] = {
    "daily_etl_main_corpus": {
        "pipeline_id": "daily_etl_main_active_diagnosis",
        "compile_inputs": [
            "tests/fixtures/ssis/official/DailyETLMain.dtsx",
        ],
        "seed_globs": [
            "tests/fixtures/**/daily_etl_main*/seeds.sql",
            "tests/fixtures/**/DailyETLMain*/seeds.sql",
            "tests/fixtures/**/active_diagnosis*/seeds.sql",
        ],
    },
    "wwi_corpus": {
        "pipeline_id": "wwi_sales_star",
        "compile_inputs": [
            "fixtures/informatica_xml/real_world_complex_pipeline.xml",
            "tests/fixtures/informatica_xml/real_world_complex_pipeline.xml",
            "fixtures/informatica_xml/wwi_star_schema_pipeline.xml",
            "tests/fixtures/informatica_xml/wwi_star_schema_pipeline.xml",
            "fixtures/informatica_xml/wwi_sales_star.xml",
        ],
        "seed_globs": [
            "tests/fixtures/**/wwi*/seeds.sql",
            "tests/fixtures/**/real_world_complex*/seeds.sql",
        ],
    },
}


def resolve_studio_root(explicit: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    env_root = os.environ.get("ETL_MIGRATION_STUDIO_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())
    candidates.extend(
        [
            ROOT.parent / "ETL-Migration-Studio",
            ROOT.parent / "ETL-Migration-Studio-main",
            Path("/ETL-Migration-Studio"),
            Path("/ETL-Migration-Studio-main"),
        ]
    )
    for path in candidates:
        if path.is_dir() and (path / "pyproject.toml").is_file():
            return path
        if path.is_dir() and any(path.rglob("etl_to_dbt")):
            return path
    return None


def find_export_bundle(studio: Path, pipeline_id: str) -> Path | None:
    for manifest in studio.rglob("manifest.json"):
        if "node_modules" in manifest.parts or ".git" in manifest.parts:
            continue
        try:
            data = json.loads(manifest.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("pipeline_id") == pipeline_id:
            if (manifest.parent / "models").is_dir() or data.get("raw_dbt_models"):
                return manifest.parent
    return None


def first_existing(studio: Path, relative_paths: list[str]) -> Path | None:
    for rel in relative_paths:
        path = studio / rel
        if path.is_file():
            return path
    return None


def compile_export(studio: Path, source_file: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    attempts = [
        [sys.executable, "-m", "etl_to_dbt.api", "export", str(source_file), "-o", str(out_dir)],
        [sys.executable, "-m", "etl_to_dbt.api", str(source_file), "--output", str(out_dir)],
        [sys.executable, "-m", "etl_to_dbt.api", str(source_file), str(out_dir)],
    ]
    errors: list[str] = []
    for cmd in attempts:
        try:
            subprocess.run(cmd, cwd=studio, check=True, capture_output=True, text=True)
            return
        except subprocess.CalledProcessError as exc:
            errors.append(f"{' '.join(cmd)}:\n{exc.stderr or exc.stdout}")
    raise RuntimeError("etl_to_dbt export failed:\n" + "\n---\n".join(errors))


def find_seed_sql(studio: Path, seed_globs: list[str], export_dir: Path) -> Path | None:
    local_seeds = export_dir / "seeds.sql"
    if local_seeds.is_file():
        return local_seeds
    for pattern in seed_globs:
        matches = sorted(studio.glob(pattern))
        if matches:
            return matches[0]
    return None


def rewrite_manifest_seeds_path(manifest_path: Path, corpus_name: str) -> None:
    data = json.loads(manifest_path.read_text())
    parity = data.get("parity_context") or {}
    parity["seeds_sql"] = f"tests/fixtures/{corpus_name}/seeds.sql"
    data["parity_context"] = parity
    manifest_path.write_text(json.dumps(data, indent=2) + "\n")


def copy_corpus_tree(src: Path, dest: Path, corpus_name: str) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy2(src / "manifest.json", dest / "manifest.json")
    models_src = src / "models"
    if models_src.is_dir():
        shutil.copytree(models_src, dest / "models")
    rewrite_manifest_seeds_path(dest / "manifest.json", corpus_name)


def ingest_corpus(studio: Path, corpus_name: str, spec: dict, *, compile_missing: bool) -> dict:
    pipeline_id = spec["pipeline_id"]
    export_dir = find_export_bundle(studio, pipeline_id)
    source_used: str | None = None

    if export_dir is None and compile_missing:
        source_file = first_existing(studio, spec["compile_inputs"])
        if source_file is None:
            raise FileNotFoundError(
                f"No pre-built export or compile input found for {corpus_name} ({pipeline_id})"
            )
        build_dir = studio / ".remodel_engine_exports" / corpus_name
        compile_export(studio, source_file, build_dir)
        export_dir = find_export_bundle(studio, pipeline_id) or build_dir
        source_used = str(source_file.relative_to(studio))

    if export_dir is None:
        raise FileNotFoundError(f"No export bundle found for pipeline_id={pipeline_id}")

    dest = FIXTURES / corpus_name
    copy_corpus_tree(export_dir, dest, corpus_name)

    seeds_src = find_seed_sql(studio, spec["seed_globs"], export_dir)
    if seeds_src is not None:
        shutil.copy2(seeds_src, dest / "seeds.sql")
    elif not (dest / "seeds.sql").is_file():
        raise FileNotFoundError(f"No seeds.sql for {corpus_name} under studio or export bundle")

    model_count = len(list((dest / "models").glob("*.sql"))) if (dest / "models").is_dir() else 0
    return {
        "corpus": corpus_name,
        "pipeline_id": pipeline_id,
        "source_export": str(export_dir.relative_to(studio)),
        "compile_source": source_used,
        "model_sql_files": model_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--studio-root",
        help="Path to ETL-Migration-Studio (default: env or ../ETL-Migration-Studio)",
    )
    parser.add_argument(
        "--compile-missing",
        action="store_true",
        help="Run python -m etl_to_dbt.api when a pre-built export bundle is not found",
    )
    args = parser.parse_args()

    studio = resolve_studio_root(args.studio_root)
    if studio is None:
        print(
            "ETL-Migration-Studio not found. Set ETL_MIGRATION_STUDIO_ROOT or clone "
            "sibling repo at ../ETL-Migration-Studio.",
            file=sys.stderr,
        )
        return 2

    print(f"Using studio root: {studio}")
    provenance: list[dict] = []
    for corpus_name, spec in CORPUS_SPECS.items():
        print(f"Ingesting {corpus_name}...")
        provenance.append(
            ingest_corpus(studio, corpus_name, spec, compile_missing=args.compile_missing)
        )

    out = FIXTURES / ".fixture_provenance.json"
    out.write_text(json.dumps({"studio_root": str(studio), "corpora": provenance}, indent=2) + "\n")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
