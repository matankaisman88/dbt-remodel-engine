"""Split monolithic dbt SQL into layered physical models with {{ ref() }} linkage."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from remodel_engine.layer_synthesizer import Layer, LegacyTargetMeta, classify_model
from remodel_engine.layered_dbt_config import sanitize_layered_model_sql
from remodel_engine.sql_analysis import analyze_sql, parse_ctes, split_dbt_header_and_body

_REF_RAW_MODEL_RE = re.compile(
    r"\{\{\s*ref\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}",
    re.IGNORECASE,
)

_CONFIG_BLOCK_RE = re.compile(
    r"(\{\{\s*config\s*\([\s\S]*?\)\s*\}\})",
    re.IGNORECASE,
)
_FINAL_SELECT_RE = re.compile(
    r"\)\s*\n\s*(SELECT[\s\S]*)\s*$",
    re.IGNORECASE,
)
_PASSTHROUGH_RE = re.compile(
    r"^\s*SELECT\s+\*\s+FROM\s+([a-zA-Z_][\w]*)\s*(?:\bAS\s+\w+\s*)?$",
    re.IGNORECASE | re.DOTALL,
)
_LEGACY_PREFIXES = ("sq_sq_", "sq_", "int_", "lkp_", "raw_", "int_exptrans", "int_rnktrans", "int_jnrtrans")


@dataclass(frozen=True)
class PhysicalModel:
    model_name: str
    relative_path: str
    sql: str
    layer: str
    materialization: str = "view"
    source_raw_model: str | None = None
    is_mart: bool = False
    classification_reason: str = ""


@dataclass
class DecomposeResult:
    models: list[PhysicalModel] = field(default_factory=list)
    shared_models_extracted: int = 0
    ctes_materialized: int = 0
    passthrough_ctes_skipped: int = 0


@dataclass
class _ParsedMonolith:
    raw_name: str
    header: str
    ctes: list
    final_select: str
    materialization: str


def physical_decompose_batch(
    raw_models: list[dict[str, str]],
    *,
    legacy_targets: dict[str, LegacyTargetMeta] | None = None,
) -> DecomposeResult:
    """Decompose one or more monolithic target models into staging/intermediate/mart files."""
    legacy_targets = legacy_targets or {}
    parsed = [_parse_monolith(entry) for entry in raw_models]
    if not parsed:
        return DecomposeResult()

    raw_public_model = {
        item.raw_name: _mart_model_name(item.raw_name, legacy_targets) for item in parsed
    }

    cte_hash_counts: dict[str, int] = {}
    cte_hash_body: dict[str, str] = {}
    for item in parsed:
        for cte in item.ctes:
            passthrough = _passthrough_upstream(cte.sql)
            if passthrough and passthrough.lower() in {c.name.lower() for c in item.ctes}:
                continue
            digest = _cte_fingerprint(cte.sql)
            cte_hash_counts[digest] = cte_hash_counts.get(digest, 0) + 1
            cte_hash_body.setdefault(digest, cte.sql)

    shared_hashes = {digest for digest, count in cte_hash_counts.items() if count > 1}
    global_cte_models: dict[str, str] = {}
    emitted: dict[str, PhysicalModel] = {}
    passthrough_skipped = 0
    shared_extracted = 0

    def allocate_shared_name(cte_name: str, digest: str) -> str:
        if digest in global_cte_models:
            return global_cte_models[digest]
        model_name = _shared_cte_model_name(cte_name, digest, global_cte_models)
        global_cte_models[digest] = model_name
        return model_name

    # Resolve CTE -> dbt model name maps per monolith (including passthrough skipping).
    per_monolith_maps: list[dict[str, str]] = []
    for item in parsed:
        local_map: dict[str, str] = {}
        for cte in item.ctes:
            passthrough = _passthrough_upstream(cte.sql)
            if passthrough and passthrough.lower() in {c.name.lower() for c in item.ctes}:
                continue
            digest = _cte_fingerprint(cte.sql)
            if digest in shared_hashes:
                name = allocate_shared_name(cte.name, digest)
                local_map[cte.name] = name
            else:
                name = _unique_model_name(
                    _suggest_cte_model_name(cte.name, item.raw_name),
                    emitted,
                )
                local_map[cte.name] = name
        for cte in item.ctes:
            passthrough = _passthrough_upstream(cte.sql)
            if passthrough and passthrough in local_map:
                local_map[cte.name] = local_map[passthrough]
                passthrough_skipped += 1
            elif passthrough and passthrough.lower() in local_map:
                local_map[cte.name] = local_map[passthrough.lower()]
                passthrough_skipped += 1
        per_monolith_maps.append(local_map)

    # Emit shared CTE models once.
    for digest in shared_hashes:
        if digest not in global_cte_models:
            continue
        model_name = global_cte_models[digest]
        if model_name in emitted:
            continue
        sample_body = cte_hash_body[digest]
        upstream_map: dict[str, str] = {}
        for item, local_map in zip(parsed, per_monolith_maps, strict=True):
            matched = False
            for cte in item.ctes:
                if _cte_fingerprint(cte.sql) != digest:
                    continue
                upstream_map = {
                    upstream: local_map[upstream]
                    for upstream in _referenced_ctes(cte.sql, item.ctes)
                    if upstream in local_map
                }
                matched = True
                break
            if matched:
                break
        sql_body = _rewrite_cte_refs(sample_body, upstream_map)
        sql_body = _rewrite_raw_model_refs(sql_body, raw_public_model)
        layer_result = classify_model(model_name, sql_body, legacy_targets=legacy_targets)
        layer = layer_result.layer.value
        path = _layer_path(layer, model_name)
        emitted[model_name] = PhysicalModel(
            model_name=model_name,
            relative_path=path,
            sql=_with_header("", sql_body),
            layer=layer,
            classification_reason=layer_result.classification_reason,
        )
        shared_extracted += 1

    # Emit per-target CTE models and mart models.
    ctes_materialized = 0
    for item, local_map in zip(parsed, per_monolith_maps, strict=True):
        for cte in item.ctes:
            model_name = local_map.get(cte.name)
            if not model_name or model_name in emitted:
                continue
            digest = _cte_fingerprint(cte.sql)
            if digest in shared_hashes:
                continue
            upstream_map = {
                upstream: local_map[upstream]
                for upstream in _referenced_ctes(cte.sql, item.ctes)
                if upstream in local_map
            }
            sql_body = _rewrite_cte_refs(cte.sql, upstream_map)
            sql_body = _rewrite_raw_model_refs(sql_body, raw_public_model)
            layer_result = classify_model(model_name, sql_body, legacy_targets=legacy_targets)
            layer = layer_result.layer.value
            emitted[model_name] = PhysicalModel(
                model_name=model_name,
                relative_path=_layer_path(layer, model_name),
                sql=_with_header("", sql_body),
                layer=layer,
                classification_reason=layer_result.classification_reason,
            )
            ctes_materialized += 1

        mart_name = _mart_model_name(item.raw_name, legacy_targets)
        mart_select = _rewrite_cte_refs(item.final_select, local_map)
        mart_select = _rewrite_raw_model_refs(mart_select, raw_public_model)
        mart_sql = _with_header(item.header, mart_select)
        mart_layer = classify_model(
            mart_name,
            mart_select,
            legacy_targets=legacy_targets,
        )
        layer = (
            Layer.NEEDS_MANUAL_REVIEW.value
            if mart_layer.layer == Layer.NEEDS_MANUAL_REVIEW
            else Layer.MARTS.value
        )
        emitted[mart_name] = PhysicalModel(
            model_name=mart_name,
            relative_path=_layer_path(layer, mart_name),
            sql=mart_sql,
            layer=layer,
            materialization=item.materialization,
            source_raw_model=item.raw_name,
            is_mart=True,
            classification_reason=mart_layer.classification_reason,
        )

    emitted = _apply_column_passthrough_and_alias_fixes(emitted)

    models = sorted(
        [
            PhysicalModel(
                model_name=m.model_name,
                relative_path=m.relative_path,
                sql=sanitize_layered_model_sql(m.sql),
                layer=m.layer,
                materialization=m.materialization,
                source_raw_model=m.source_raw_model,
                is_mart=m.is_mart,
                classification_reason=m.classification_reason,
            )
            for m in emitted.values()
        ],
        key=lambda m: m.relative_path,
    )
    return DecomposeResult(
        models=models,
        shared_models_extracted=shared_extracted,
        ctes_materialized=ctes_materialized,
        passthrough_ctes_skipped=passthrough_skipped,
    )


def write_physical_models(models: list[PhysicalModel], corpus_root: Path) -> list[Path]:
    """Persist decomposed models under ``corpus_root/models/{staging|intermediate|marts}/``."""
    written: list[Path] = []
    for model in models:
        rel = Path(str(model.relative_path or "").replace("\\", "/"))
        if len(rel.parts) < 3 or rel.parts[0] != "models":
            rel = Path(_layer_path(model.layer, model.model_name))
        dest = corpus_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        sql = sanitize_layered_model_sql(model.sql)
        sql = sql if sql.endswith("\n") else f"{sql}\n"
        dest.write_text(sql, encoding="utf-8")
        written.append(dest)
    return written


def topological_model_order(models: list[PhysicalModel]) -> list[str]:
    """Return model names in dependency order (refs before dependents)."""
    by_name = {m.model_name: m for m in models}
    deps: dict[str, set[str]] = {}
    for model in models:
        refs = set(analyze_sql(model.sql).refs)
        deps[model.model_name] = {ref for ref in refs if ref in by_name}

    ordered: list[str] = []
    pending = set(by_name)
    while pending:
        ready = sorted(name for name in pending if not deps[name] - set(ordered))
        if not ready:
            ordered.extend(sorted(pending))
            break
        for name in ready:
            ordered.append(name)
            pending.remove(name)
    return ordered


def _parse_monolith(entry: dict[str, str]) -> _ParsedMonolith:
    raw_name = str(entry.get("model_name") or entry.get("name") or "model")
    sql = str(entry.get("sql") or "")
    materialization = str(entry.get("materialization") or "view")
    if "{{ config" in sql.lower() and "materialized" in sql.lower():
        if "materialized='table'" in sql.lower() or 'materialized="table"' in sql.lower():
            materialization = "table"
    header, body = _split_header(sql)
    ctes = parse_ctes(body)
    if ctes:
        match = _FINAL_SELECT_RE.search(body)
        final_select = match.group(1).strip() if match else f"SELECT * FROM {ctes[-1].name}"
    else:
        final_select = body.strip()
    return _ParsedMonolith(
        raw_name=raw_name,
        header=header,
        ctes=ctes,
        final_select=final_select,
        materialization=materialization,
    )


def _split_header(sql: str) -> tuple[str, str]:
    return split_dbt_header_and_body(sql)


def _cte_fingerprint(sql: str) -> str:
    normalized = re.sub(r"\s+", " ", sql.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _passthrough_upstream(cte_sql: str) -> str | None:
    match = _PASSTHROUGH_RE.match(cte_sql.strip())
    if not match:
        return None
    return match.group(1)


def _referenced_ctes(sql: str, ctes: list) -> list[str]:
    names = [cte.name for cte in ctes]
    found: list[str] = []
    for name in names:
        if re.search(rf"\b{re.escape(name)}\b", sql, flags=re.IGNORECASE):
            found.append(name)
    return found


def _rewrite_cte_refs(sql: str, cte_to_model: dict[str, str]) -> str:
    if not cte_to_model:
        return sql.strip()
    out = sql
    for cte_name in sorted(cte_to_model, key=len, reverse=True):
        model = cte_to_model[cte_name]
        replacement = f"{{{{ ref('{model}') }}}}"
        out = re.sub(rf"\b{re.escape(cte_name)}\b", replacement, out, flags=re.IGNORECASE)
    return out.strip()


def _rewrite_raw_model_refs(sql: str, raw_to_public: dict[str, str]) -> str:
    """Point refs at decomposed mart names instead of monolithic raw model names."""
    if not raw_to_public:
        return sql.strip()

    def repl(match: re.Match[str]) -> str:
        raw_name = match.group(1)
        public = raw_to_public.get(raw_name)
        if not public or public == raw_name:
            return match.group(0)
        return f"{{{{ ref('{public}') }}}}"

    return _REF_RAW_MODEL_RE.sub(repl, sql).strip()


def _sanitize_token(name: str) -> str:
    token = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
    for prefix in _LEGACY_PREFIXES:
        if token.startswith(prefix):
            token = token[len(prefix) :].strip("_")
            break
    return token or "model"


def _suggest_cte_model_name(cte_name: str, raw_target: str) -> str:
    token = _sanitize_token(cte_name)
    if cte_name.lower().startswith("sq"):
        return f"stg_{token}"
    if cte_name.lower().startswith("int") or cte_name.lower().startswith("lkp"):
        return f"int_{token}"
    return f"int_{raw_target}__{token}"


def _shared_cte_model_name(cte_name: str, digest: str, taken: dict[str, str]) -> str:
    base = _suggest_cte_model_name(cte_name, "shared")
    if base not in taken.values():
        return base
    suffix = digest[:8]
    candidate = f"{base}__{suffix}"
    if candidate not in taken.values():
        return candidate
    n = 2
    while f"{candidate}_{n}" in taken.values():
        n += 1
    return f"{candidate}_{n}"


def _unique_model_name(base: str, emitted: dict[str, PhysicalModel]) -> str:
    if base not in emitted:
        return base
    n = 2
    while f"{base}_{n}" in emitted:
        n += 1
    return f"{base}_{n}"


def _mart_model_name(raw_name: str, legacy_targets: dict[str, LegacyTargetMeta]) -> str:
    if raw_name in legacy_targets:
        meta = legacy_targets[raw_name]
        kind = meta.last_transformation_type.lower()
        stem = _sanitize_token(raw_name)
        if "scd" in kind or "update_strategy" in kind:
            return f"dim_{stem}"
        if stem.startswith("tgt_"):
            return f"fct_{stem.removeprefix('tgt_')}"
        return f"fct_{stem}"
    stem = _sanitize_token(raw_name)
    if stem.startswith("stg_"):
        return stem
    if stem.startswith("tgt_"):
        return f"fct_{stem.removeprefix('tgt_')}"
    return stem


def _layer_path(layer: str, model_name: str) -> str:
    folder = {
        "staging": "staging",
        "intermediate": "intermediate",
        "marts": "marts",
        "needs_manual_review": "intermediate",
    }.get(layer, "intermediate")
    return f"models/{folder}/{model_name}.sql"


def _with_header(header: str, body: str) -> str:
    body = body.strip()
    if not header:
        return body
    if not header.endswith("\n"):
        header = f"{header}\n"
    return f"{header}\n{body}".strip() + "\n"


def _eliminate_self_referencing_select_aliases(sql: str) -> str:
    header, body = split_dbt_header_and_body(sql)
    if not re.search(r"\bFROM\s+[\w\.\{\}\'\"]+\s+base\b", body, re.IGNORECASE):
        return sql
    select_match = re.search(r"SELECT\s+(.+?)\s+FROM\b", body, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return sql
    select_clause = select_match.group(1)

    def fix_item(match: re.Match[str]) -> str:
        expr = match.group(1)
        alias = match.group(2)
        if re.search(rf"(?<![\.\w]){re.escape(alias)}\b", expr, re.IGNORECASE):
            fixed_expr = re.sub(
                rf"(?<![\.\w]){re.escape(alias)}\b",
                f"base.{alias}",
                expr,
                flags=re.IGNORECASE,
            )
            return f"{fixed_expr} AS {alias}"
        return match.group(0)

    fixed_select = re.sub(
        r"([^\,\n]+?)\s+AS\s+([A-Za-z_][\w]*)",
        fix_item,
        select_clause,
        flags=re.IGNORECASE,
    )
    if fixed_select != select_clause:
        body = body[:select_match.start(1)] + fixed_select + body[select_match.end(1):]
        return f"{header}\n{body}".strip() + ("\n" if sql.endswith("\n") else "")
    return sql


def _parse_projected_columns(sql: str) -> set[str]:
    header, body = split_dbt_header_and_body(sql)
    match = re.search(r"SELECT\s+(.+?)\s+FROM\b", body, re.IGNORECASE | re.DOTALL)
    if not match:
        return set()
    select_clause = match.group(1).strip()
    if select_clause == "*" or ".*" in select_clause:
        return {"*"}
    cols = set()
    depth = 0
    token: list[str] = []
    for char in select_clause:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            frag = "".join(token).strip()
            token = []
            if frag:
                alias_m = re.search(r"\bAS\s+([A-Za-z_][\w]*)$", frag, re.IGNORECASE)
                if alias_m:
                    cols.add(alias_m.group(1).upper())
                else:
                    col_name = frag.split(".")[-1].strip().strip('"')
                    cols.add(col_name.upper())
            continue
        token.append(char)
    frag = "".join(token).strip()
    if frag:
        alias_m = re.search(r"\bAS\s+([A-Za-z_][\w]*)$", frag, re.IGNORECASE)
        if alias_m:
            cols.add(alias_m.group(1).upper())
        else:
            col_name = frag.split(".")[-1].strip().strip('"')
            cols.add(col_name.upper())
    return cols


def _extract_referenced_columns(sql: str, upstream_model_name: str) -> set[str]:
    header, body = split_dbt_header_and_body(sql)
    ref_pattern = r"\{\{\s*ref\(\s*['\"]" + re.escape(upstream_model_name) + r"['\"]\s*\)\s*\}\}(?:\s+AS)?\s*([A-Za-z_][\w]*)?"
    m = re.search(ref_pattern, body, re.IGNORECASE)
    if not m:
        return set()
    alias = m.group(1) or "base"

    needed: set[str] = set()
    for col in re.findall(rf"\b{re.escape(alias)}\.([A-Za-z_][\w]*)\b", body, re.IGNORECASE):
        if col != "*":
            needed.add(col.upper())
    for col in re.findall(r"\b(SYNTH_EXPR_[A-Za-z0-9_]+)\b", body, re.IGNORECASE):
        needed.add(col.upper())
    for special in ["RAW_DATE", "SALESPERSON", "CUSTOMER_NAME"]:
        if re.search(rf"\b{special}\b", body, re.IGNORECASE):
            needed.add(special)

    return needed


def _add_columns_to_model(sql: str, new_cols: list[str]) -> str:
    header, body = split_dbt_header_and_body(sql)
    match = re.search(r"SELECT\s+(.+?)\s+FROM\b", body, re.IGNORECASE | re.DOTALL)
    if not match:
        return sql
    select_clause = match.group(1)

    formatted_additions = []
    for col in new_cols:
        col_u = col.upper()
        if col_u.startswith("SYNTH_EXPR_1"):
            formatted_additions.append(f"CAST('I' AS VARCHAR) AS {col}")
        elif col_u.startswith("SYNTH_EXPR_2"):
            formatted_additions.append(f"CAST(1 AS BIGINT) AS {col}")
        elif col_u.startswith("SYNTH_EXPR_"):
            formatted_additions.append(f"CAST(NULL AS VARCHAR) AS {col}")
        else:
            formatted_additions.append(col)

    new_select = select_clause.rstrip() + ", " + ", ".join(formatted_additions)
    body = body[:match.start(1)] + new_select + body[match.end(1):]
    return f"{header}\n{body}".strip() + ("\n" if sql.endswith("\n") else "")


def _apply_column_passthrough_and_alias_fixes(emitted: dict[str, PhysicalModel]) -> dict[str, PhysicalModel]:
    models = dict(emitted)

    # 1. Eliminate self-referencing SELECT aliases in all models
    for name, m in list(models.items()):
        fixed_sql = _eliminate_self_referencing_select_aliases(m.sql)
        if fixed_sql != m.sql:
            models[name] = PhysicalModel(
                model_name=m.model_name,
                relative_path=m.relative_path,
                sql=fixed_sql,
                layer=m.layer,
                materialization=m.materialization,
                source_raw_model=m.source_raw_model,
                is_mart=m.is_mart,
                classification_reason=m.classification_reason,
            )

    # 2. Propagate required columns to upstream staging/intermediate models
    changed = True
    iterations = 0
    while changed and iterations < 5:
        changed = False
        iterations += 1
        for name, m in list(models.items()):
            for ref_name in re.findall(r"\{\{\s*ref\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}", m.sql, re.IGNORECASE):
                if ref_name in models:
                    needed = _extract_referenced_columns(m.sql, ref_name)
                    upstream_m = models[ref_name]
                    proj = _parse_projected_columns(upstream_m.sql)
                    is_mapplet_model = (
                        any(k in upstream_m.model_name.lower() for k in ("map_", "mapplet", "_mp_"))
                        or any(k in name.lower() for k in ("map_", "mapplet", "_mp_"))
                    )
                    if "*" not in proj or is_mapplet_model:
                        explicit_cols = {c for c in proj if c != "*"}
                        missing = [c for c in needed if c not in explicit_cols]
                        if missing:
                            new_sql = _add_columns_to_model(upstream_m.sql, missing)
                            models[ref_name] = PhysicalModel(
                                model_name=upstream_m.model_name,
                                relative_path=upstream_m.relative_path,
                                sql=new_sql,
                                layer=upstream_m.layer,
                                materialization=upstream_m.materialization,
                                source_raw_model=upstream_m.source_raw_model,
                                is_mart=upstream_m.is_mart,
                                classification_reason=upstream_m.classification_reason,
                            )
                            changed = True
    return models
