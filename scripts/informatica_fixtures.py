"""Discover Informatica legacy XML fixtures under ETL-Migration-Studio."""

from __future__ import annotations

from pathlib import Path

INFORMATICA_GLOBS: tuple[str, ...] = (
    "fixtures/informatica_xml/*.xml",
    "fixtures/informatica_stress_corpus/*.xml",
    "fixtures/orchestration/infa_wrapped/*.xml",
    "fixtures/orchestration/infa/*.xml",
    "fixtures/informatica_workflow/*.xml",
)

# Negative / workflow-only fixtures (parse, but Studio emits no dbt models).
COMPILE_EXCLUDE_STEMS: frozenset[str] = frozenset(
    {
        "malformed_root",
        "malformed_unclosed_tag",
        "command_only_workflow",
        "failure_link_workflow",
        "minimal_session_worklet",
        "nested_worklet",
        "parallel_sessions",
    }
)

SKIP_DIR_NAMES = frozenset({"node_modules", ".git"})
FIXTURE_NAMESPACE = "informatica"


def _skip_path(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def pipeline_id_for_fixture(studio: Path, xml_path: Path) -> str:
    """Stable pipeline_id / corpus folder name from path under studio/fixtures/."""
    fixtures_root = studio / "fixtures"
    try:
        rel = xml_path.relative_to(fixtures_root)
    except ValueError:
        rel = xml_path.name
    slug = str(rel.with_suffix("")).replace("\\", "/").replace("/", "_")
    slug = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in slug)
    slug = slug.strip("._").lower()
    return slug or "informatica_fixture"


def iter_informatica_fixture_paths(studio: Path) -> list[Path]:
    studio = studio.resolve()
    seen: set[Path] = set()
    paths: list[Path] = []
    for pattern in INFORMATICA_GLOBS:
        for path in sorted(studio.glob(pattern)):
            if not path.is_file() or _skip_path(path):
                continue
            if path.stem in COMPILE_EXCLUDE_STEMS:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            paths.append(path)
    return paths
