"""Pydantic request/response models — Section 6 API contract."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class RawDbtModel(BaseModel):
    model_name: str
    sql: str
    materialization: str = "view"


class RemodelPreferences(BaseModel):
    target_pattern: str = "star_schema"
    collapse_ctes: bool = True
    modernize_window_functions: bool = True


class RemodelRequest(BaseModel):
    pipeline_id: str
    source_platform: str
    raw_dbt_models: list[RawDbtModel]
    preferences: RemodelPreferences = Field(default_factory=RemodelPreferences)
    legacy_targets: dict[str, dict[str, str]] = Field(default_factory=dict)
    lookup_rewrites: list[dict[str, Any]] = Field(default_factory=list)
    parity_context: dict[str, Any] | None = None
    legacy_transformations_count: int | None = None
    legacy_graph_nodes: list[dict[str, Any]] = Field(default_factory=list)
    legacy_graph_edges: list[dict[str, Any]] = Field(default_factory=list)


class RefactoringSummary(BaseModel):
    legacy_transformations_count: int = 0
    modern_models_count: int = 0
    ctes_collapsed: int = 0
    window_functions_applied: int = 0
    models_needs_manual_review: int = 0


class GraphNode(BaseModel):
    id: str
    label: str
    layer: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source: str
    target: str


class TransformationGraph(BaseModel):
    type: Literal["transformation_graph"] = "transformation_graph"
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class DbtModelGraph(BaseModel):
    type: Literal["dbt_model_graph"] = "dbt_model_graph"
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class ParityCheck(BaseModel):
    status: str
    row_count_match: bool | None = None
    column_diff: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None


class RemodeledModel(BaseModel):
    model_name: str
    layer: str
    sql: str
    inner_ctes: list[str] = Field(default_factory=list)
    classification_reason: str
    parity_check: ParityCheck
    flagged: bool = False
    merge_audits: list[dict[str, Any]] = Field(default_factory=list)


class RemodelResponse(BaseModel):
    pipeline_id: str
    status: Literal["success", "needs_manual_review", "failed_parity"]
    refactoring_summary: RefactoringSummary
    before_graph: TransformationGraph
    after_graph: DbtModelGraph
    remodeled_models: list[RemodeledModel]
