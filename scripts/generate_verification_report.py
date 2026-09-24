#!/usr/bin/env python3
"""Generate remodeling_verification_report.md from real corpus manifests."""

from __future__ import annotations

import json
from pathlib import Path

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine
from remodel_engine.layer_synthesizer import Layer

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
PROVENANCE_PATH = FIXTURES / ".fixture_provenance.json"
CORPORA = [
    ("WWI corpus (etl_to_dbt export format)", FIXTURES / "wwi_corpus" / "manifest.json"),
    (
        "DailyETLMain / Informatica corpus (etl_to_dbt export format)",
        FIXTURES / "daily_etl_main_corpus" / "manifest.json",
    ),
]


def _provenance_banner() -> list[str]:
    if not PROVENANCE_PATH.is_file():
        return [
            "> **Fixture provenance:** Placeholder or manually copied corpora. Run",
            "> `python scripts/ingest_fixtures_from_studio.py --compile-missing` with",
            "> ETL-Migration-Studio checked out at `../ETL-Migration-Studio` to refresh.",
        ]
    data = json.loads(PROVENANCE_PATH.read_text())
    studio = data.get("studio_root", "unknown")
    lines = [
        "> **Fixture provenance:** Ingested from ETL-Migration-Studio via",
        "> `scripts/ingest_fixtures_from_studio.py`.",
        f"> **Studio root:** `{studio}`",
    ]
    for entry in data.get("corpora", []):
        lines.append(
            f"> - `{entry.get('corpus')}` (`{entry.get('pipeline_id')}`): "
            f"{entry.get('model_sql_files')} models from `{entry.get('source_export')}`"
        )
    return lines


def main() -> None:
    engine = RemodelEngine()
    lines: list[str] = [
        "# Remodeling Verification Report",
        "",
        "Phase A headless engine run against copied corpora under `tests/fixtures/`.",
        "",
        *_provenance_banner(),
        "",
    ]

    failures: list[str] = []
    manual: list[str] = []

    for title, manifest_path in CORPORA:
        req = load_corpus_manifest(manifest_path)
        resp = engine.remodel(req)
        lines.extend(
            [
                f"## {title}",
                "",
                f"- **pipeline_id:** `{resp.pipeline_id}`",
                f"- **overall status:** `{resp.status}`",
                f"- **legacy transformations (manifest):** {resp.refactoring_summary.legacy_transformations_count}",
                f"- **modern models:** {resp.refactoring_summary.modern_models_count}",
                f"- **CTEs collapsed:** {resp.refactoring_summary.ctes_collapsed}",
                f"- **models NEEDS_MANUAL_REVIEW:** {resp.refactoring_summary.models_needs_manual_review}",
                "",
                "### Per-model results",
                "",
                "| Model | Layer | Parity | Classification reason | CTE merges |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for model in resp.remodeled_models:
            merges = ", ".join(
                str(a.get("cte_merged_from")) for a in model.merge_audits
            ) or "—"
            lines.append(
                f"| `{model.model_name}` | `{model.layer}` | `{model.parity_check.status}` | "
                f"{model.classification_reason} | {merges} |"
            )
            if model.parity_check.status == "fail":
                detail = json.dumps(model.parity_check.model_dump(), indent=2)
                failures.append(f"**{resp.pipeline_id} / {model.model_name}**\n\n```json\n{detail}\n```")
            if model.layer == Layer.NEEDS_MANUAL_REVIEW.value or model.flagged:
                manual.append(
                    f"- `{resp.pipeline_id}` → `{model.model_name}`: {model.classification_reason}"
                )
        lines.append("")

    lines.extend(["## Failures (unfiltered)", ""])
    if failures:
        lines.extend(failures)
    else:
        lines.append("_No parity failures._")
    lines.extend(["", "## NEEDS_MANUAL_REVIEW (unfiltered)", ""])
    if manual:
        lines.extend(manual)
    else:
        lines.append("_None._")
    lines.append("")

    out = ROOT / "remodeling_verification_report.md"
    out.write_text("\n".join(lines))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
