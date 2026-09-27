#!/usr/bin/env python3
"""Copy real etl_to_dbt export bundles from ETL-Migration-Studio into tests/fixtures/."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
FIXTURES = ROOT / "tests" / "fixtures"
STUDIO_COMPILE_DEFAULTS = SCRIPTS / "studio_compile_defaults.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import informatica_fixtures as infa  # noqa: E402

INGEST_CONFIG_NAMES = ("ingest_config.json", ".ingest_config.json")
SKIP_DIR_NAMES = frozenset({"node_modules", ".git"})


def sanitize_corpus_name(pipeline_id: str) -> str:
    name = re.sub(r"[^\w.\-]+", "_", pipeline_id.strip())
    name = name.strip("._")
    return (name or "corpus").lower()


def _skip_path(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def iter_studio_manifests(studio: Path):
    for manifest in studio.rglob("manifest.json"):
        if _skip_path(manifest):
            continue
        yield manifest


@dataclass
class CorpusIngestPlan:
    pipeline_id: str
    corpus_name: str
    export_dir: Path | None = None
    seed_globs: list[str] = field(default_factory=list)
    compile_inputs: list[str] = field(default_factory=list)
    fixture_namespace: str | None = None


def load_studio_compile_defaults() -> list[dict]:
    if not STUDIO_COMPILE_DEFAULTS.is_file():
        return []
    try:
        data = json.loads(STUDIO_COMPILE_DEFAULTS.read_text())
    except (json.JSONDecodeError, OSError):
        return []
    if isinstance(data, list):
        return [entry for entry in data if isinstance(entry, dict)]
    if isinstance(data, dict):
        corpora = data.get("corpora")
        if isinstance(corpora, list):
            return [entry for entry in corpora if isinstance(entry, dict)]
    return []


def load_ingest_config(directory: Path) -> dict:
    for name in INGEST_CONFIG_NAMES:
        path = directory / name
        if path.is_file():
            try:
                return json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
    return {}


def unique_corpus_name(pipeline_id: str, used: set[str]) -> str:
    base = sanitize_corpus_name(pipeline_id)
    if base not in used:
        used.add(base)
        return base
    n = 2
    while True:
        candidate = f"{base}_{n}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        n += 1


def discover_export_corpora(
    studio: Path,
    pipeline_ids: set[str] | None,
) -> list[CorpusIngestPlan]:
    used_names: set[str] = set()
    plans: list[CorpusIngestPlan] = []
    for manifest_path in iter_studio_manifests(studio):
        try:
            data = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        pipeline_id = data.get("pipeline_id")
        if not pipeline_id or not isinstance(pipeline_id, str):
            continue
        if pipeline_ids is not None and pipeline_id not in pipeline_ids:
            continue
        export_dir = manifest_path.parent
        if not (export_dir / "models").is_dir() and not data.get("raw_dbt_models"):
            continue
        cfg = load_ingest_config(export_dir)
        plans.append(
            CorpusIngestPlan(
                pipeline_id=pipeline_id,
                corpus_name=unique_corpus_name(pipeline_id, used_names),
                export_dir=export_dir,
                seed_globs=list(cfg.get("seed_globs") or []),
                compile_inputs=list(cfg.get("compile_inputs") or []),
            )
        )
    plans.sort(key=lambda p: p.corpus_name)
    return plans


def _glob_studio(studio: Path, pattern: str) -> list[Path]:
    pattern = pattern.replace("\\", "/")
    if pattern.startswith("/"):
        pattern = pattern.lstrip("/")
    if "**" in pattern:
        return sorted(p for p in studio.glob(pattern) if p.is_file() and not _skip_path(p))
    return sorted(p for p in studio.glob(pattern) if p.is_file() and not _skip_path(p))


def discover_compile_only_plans(
    studio: Path,
    *,
    compile_inputs_glob: str | None,
    pipeline_ids: set[str] | None,
    existing_pipeline_ids: set[str],
) -> list[CorpusIngestPlan]:
    """Plans for pipelines that need etl_to_dbt export before ingest (no pre-built bundle)."""
    used_names: set[str] = set()
    plans: list[CorpusIngestPlan] = []
    seen_source_files: set[Path] = set()

    def add_plan(
        pipeline_id: str,
        compile_inputs: list[str],
        seed_globs: list[str],
        config_dir: Path,
    ) -> None:
        if pipeline_ids is not None and pipeline_id not in pipeline_ids:
            return
        if pipeline_id in existing_pipeline_ids:
            return
        resolved_inputs: list[str] = []
        for rel in compile_inputs:
            path = (config_dir / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
            if not path.is_file():
                path = (studio / rel).resolve()
            if path.is_file() and path not in seen_source_files:
                seen_source_files.add(path)
                resolved_inputs.append(str(path.relative_to(studio)))
        if not resolved_inputs:
            return
        plans.append(
            CorpusIngestPlan(
                pipeline_id=pipeline_id,
                corpus_name=unique_corpus_name(pipeline_id, used_names),
                export_dir=None,
                seed_globs=seed_globs,
                compile_inputs=resolved_inputs,
            )
        )

    if compile_inputs_glob:
        for source_file in _glob_studio(studio, compile_inputs_glob):
            cfg = load_ingest_config(source_file.parent)
            pid = cfg.get("pipeline_id") or infa.pipeline_id_for_fixture(studio, source_file)
            inputs = cfg.get("compile_inputs") or [str(source_file.relative_to(studio))]
            add_plan(
                pid,
                list(inputs),
                list(cfg.get("seed_globs") or []),
                source_file.parent,
            )

    for config_name in INGEST_CONFIG_NAMES:
        for config_path in studio.rglob(config_name):
            if _skip_path(config_path):
                continue
            cfg = load_ingest_config(config_path.parent)
            if not cfg.get("compile_inputs"):
                continue
            pid = cfg.get("pipeline_id")
            if not pid:
                continue
            add_plan(
                pid,
                list(cfg["compile_inputs"]),
                list(cfg.get("seed_globs") or []),
                config_path.parent,
            )

    for spec in load_studio_compile_defaults():
        pid = spec.get("pipeline_id")
        if not pid:
            continue
        add_plan(
            pid,
            list(spec.get("compile_inputs") or []),
            list(spec.get("seed_globs") or []),
            studio,
        )

    plans.sort(key=lambda p: p.corpus_name)
    return plans


def discover_informatica_ingest_plans(
    studio: Path,
    pipeline_ids: set[str] | None,
    existing_pipeline_ids: set[str],
) -> list[CorpusIngestPlan]:
    used_names: set[str] = set()
    plans: list[CorpusIngestPlan] = []
    for xml_path in infa.iter_informatica_fixture_paths(studio):
        pipeline_id = infa.pipeline_id_for_fixture(studio, xml_path)
        if pipeline_ids is not None and pipeline_id not in pipeline_ids:
            continue
        if pipeline_id in existing_pipeline_ids:
            continue
        rel = str(xml_path.relative_to(studio))
        plans.append(
            CorpusIngestPlan(
                pipeline_id=pipeline_id,
                corpus_name=unique_corpus_name(pipeline_id, used_names),
                export_dir=None,
                compile_inputs=[rel],
                fixture_namespace=infa.FIXTURE_NAMESPACE,
            )
        )
    plans.sort(key=lambda p: p.corpus_name)
    return plans


def fixture_dest(plan: CorpusIngestPlan) -> Path:
    if plan.fixture_namespace:
        return FIXTURES / plan.fixture_namespace / plan.corpus_name
    return FIXTURES / plan.corpus_name


def fixture_seeds_relpath(plan: CorpusIngestPlan) -> str:
    if plan.fixture_namespace:
        return f"tests/fixtures/{plan.fixture_namespace}/{plan.corpus_name}/seeds.sql"
    return f"tests/fixtures/{plan.corpus_name}/seeds.sql"


def explain_no_export_corpora(studio: Path) -> None:
    manifests = list(iter_studio_manifests(studio))
    print(f"Scanned {len(manifests)} manifest.json file(s) under {studio}", file=sys.stderr)
    for manifest_path in manifests:
        rel = manifest_path.relative_to(studio)
        try:
            data = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  skipped {rel}: unreadable ({exc})", file=sys.stderr)
            continue
        pipeline_id = data.get("pipeline_id")
        has_models = (manifest_path.parent / "models").is_dir()
        has_raw = bool(data.get("raw_dbt_models"))
        if pipeline_id and (has_models or has_raw):
            print(f"  eligible: {rel} (pipeline_id={pipeline_id})", file=sys.stderr)
            continue
        reasons: list[str] = []
        if not pipeline_id:
            reasons.append("no pipeline_id")
        if not has_models and not has_raw:
            reasons.append("no models/ directory and no raw_dbt_models")
        print(f"  skipped {rel}: {'; '.join(reasons)}", file=sys.stderr)
    print(
        "\nETL-Migration-Studio typically does not commit pre-built remodel export bundles "
        "(manifest.json + models/*.sql + seeds.sql).\n"
        "Re-run with --compile-missing to build from legacy sources listed in "
        f"{STUDIO_COMPILE_DEFAULTS.relative_to(ROOT)} and/or ingest_config.json beside "
        "compile inputs in Studio.\n"
        "Until then, keep using the corpora already under tests/fixtures/.",
        file=sys.stderr,
    )


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
    for manifest in iter_studio_manifests(studio):
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


STUDIO_COMPILE_EXPORT = ROOT / "scripts" / "studio_compile_export.py"


def compile_export(
    studio: Path,
    source_file: Path,
    out_dir: Path,
    *,
    pipeline_id: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(STUDIO_COMPILE_EXPORT),
        "--studio-root",
        str(studio),
        "--source",
        str(source_file),
        "--pipeline-id",
        pipeline_id,
        "--out-dir",
        str(out_dir),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(
            f"Studio compile export failed for {source_file}:\n{detail}"
        ) from exc
    if not (out_dir / "manifest.json").is_file():
        raise RuntimeError(
            f"Studio compile export did not write manifest.json under {out_dir}"
        )


def find_seed_sql(studio: Path, seed_globs: list[str], export_dir: Path) -> Path | None:
    local_seeds = export_dir / "seeds.sql"
    if local_seeds.is_file():
        return local_seeds
    for pattern in seed_globs:
        matches = sorted(studio.glob(pattern))
        if matches:
            return matches[0]
    return None


def rewrite_manifest_seeds_path(manifest_path: Path, seeds_relpath: str) -> None:
    from remodel_engine.seed_introspection import extract_source_table_map

    data = json.loads(manifest_path.read_text())
    parity = data.get("parity_context") or {}
    parity["seeds_sql"] = seeds_relpath
    seeds_path = manifest_path.parent / Path(seeds_relpath).name
    if seeds_path.is_file():
        table_map = extract_source_table_map(seeds_path.read_text())
        parity["source_table_map"] = {
            f"{schema}.{table}": physical
            for (schema, table), physical in table_map.items()
        }
    data["parity_context"] = parity
    manifest_path.write_text(json.dumps(data, indent=2) + "\n")


def copy_corpus_tree(src: Path, dest: Path, seeds_relpath: str) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy2(src / "manifest.json", dest / "manifest.json")
    for sub in ("models", "raw_models"):
        src_sub = src / sub
        if src_sub.is_dir():
            shutil.copytree(src_sub, dest / sub)
    rewrite_manifest_seeds_path(dest / "manifest.json", seeds_relpath)


def ingest_corpus(studio: Path, plan: CorpusIngestPlan, *, compile_missing: bool) -> dict:
    export_dir = plan.export_dir
    source_used: str | None = None

    if export_dir is None and compile_missing and plan.compile_inputs:
        source_file = first_existing(studio, plan.compile_inputs)
        if source_file is None:
            raise FileNotFoundError(
                f"No compile input found for {plan.corpus_name} ({plan.pipeline_id}): "
                f"{plan.compile_inputs}"
            )
        build_dir = studio / ".remodel_engine_exports" / plan.corpus_name
        compile_export(
            studio,
            source_file,
            build_dir,
            pipeline_id=plan.pipeline_id,
        )
        export_dir = find_export_bundle(studio, plan.pipeline_id) or build_dir
        source_used = str(source_file.relative_to(studio))

    if export_dir is None:
        raise FileNotFoundError(f"No export bundle found for pipeline_id={plan.pipeline_id}")

    manifest_path = export_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Export bundle at {export_dir} is missing manifest.json "
            f"(pipeline_id={plan.pipeline_id})"
        )

    dest = fixture_dest(plan)
    copy_corpus_tree(export_dir, dest, fixture_seeds_relpath(plan))

    seeds_src = find_seed_sql(studio, plan.seed_globs, export_dir)
    if seeds_src is not None:
        shutil.copy2(seeds_src, dest / "seeds.sql")
    elif not (dest / "seeds.sql").is_file():
        raise FileNotFoundError(f"No seeds.sql for {plan.corpus_name} under studio or export bundle")

    rewrite_manifest_seeds_path(dest / "manifest.json", fixture_seeds_relpath(plan))

    model_count = (
        len(list((dest / "models").rglob("*.sql"))) if (dest / "models").is_dir() else 0
    )
    return {
        "corpus": plan.corpus_name,
        "pipeline_id": plan.pipeline_id,
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
        help=(
            "Compile legacy sources via ETL-Migration-Studio (parse + convert) when no "
            "pre-built export bundle is found"
        ),
    )
    parser.add_argument(
        "--compile-inputs-glob",
        metavar="GLOB",
        help=(
            "When used with --compile-missing, studio-relative glob of compile inputs "
            "(e.g. 'fixtures/**/*.dtsx'). Optional ingest_config.json beside each input "
            "may set pipeline_id, compile_inputs, and seed_globs."
        ),
    )
    parser.add_argument(
        "--pipeline-id",
        action="append",
        dest="pipeline_ids",
        metavar="ID",
        help="Restrict ingest to one or more pipeline_id values (repeatable)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List discovered corpora without copying or deleting tests/fixtures/*",
    )
    parser.add_argument(
        "--all-informatica",
        action="store_true",
        help=(
            "With --compile-missing, compile every Informatica XML under Studio fixtures/ "
            f"into tests/fixtures/{infa.FIXTURE_NAMESPACE}/ (excludes workflow-only negatives)."
        ),
    )
    args = parser.parse_args()

    if args.all_informatica and not args.compile_missing:
        print("--all-informatica requires --compile-missing", file=sys.stderr)
        return 2

    studio = resolve_studio_root(args.studio_root)
    if studio is None:
        print(
            "ETL-Migration-Studio not found. Set ETL_MIGRATION_STUDIO_ROOT or clone "
            "sibling repo at ../ETL-Migration-Studio.",
            file=sys.stderr,
        )
        return 2

    pipeline_filter = set(args.pipeline_ids) if args.pipeline_ids else None

    print(f"Using studio root: {studio}")
    if args.all_informatica:
        plans = discover_informatica_ingest_plans(studio, pipeline_filter, set())
    else:
        plans = discover_export_corpora(studio, pipeline_filter)
        if not plans and not args.compile_missing:
            print("No export corpora discovered.", file=sys.stderr)
            explain_no_export_corpora(studio)
            return 1

        if args.compile_missing:
            discovered_ids = {p.pipeline_id for p in plans}
            compile_plans = discover_compile_only_plans(
                studio,
                compile_inputs_glob=args.compile_inputs_glob,
                pipeline_ids=pipeline_filter,
                existing_pipeline_ids=discovered_ids,
            )
            plans = sorted(plans + compile_plans, key=lambda p: p.corpus_name)

    if not plans:
        print("No corpora matched the given filters.", file=sys.stderr)
        if pipeline_filter:
            print(f"  --pipeline-id filter: {sorted(pipeline_filter)}", file=sys.stderr)
        return 1

    if args.dry_run:
        for plan in plans:
            origin = (
                str(plan.export_dir.relative_to(studio))
                if plan.export_dir is not None
                else f"compile via {plan.compile_inputs}"
            )
            print(f"  {plan.corpus_name} ({plan.pipeline_id}) <- {origin}")
        print(f"Dry run: {len(plans)} corpus/corpora; no files written.")
        return 0

    provenance: list[dict] = []
    for plan in plans:
        print(f"Ingesting {plan.corpus_name} (pipeline_id={plan.pipeline_id})...")
        provenance.append(ingest_corpus(studio, plan, compile_missing=args.compile_missing))

    out = FIXTURES / ".fixture_provenance.json"
    out.write_text(json.dumps({"studio_root": str(studio), "corpora": provenance}, indent=2) + "\n")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
