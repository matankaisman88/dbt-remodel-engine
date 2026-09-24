"""Build before (transformation) and after (dbt model) graphs."""

from __future__ import annotations

from remodel_engine.schema import (
    DbtModelGraph,
    GraphEdge,
    GraphNode,
    TransformationGraph,
)
from remodel_engine.sql_analysis import extract_refs, extract_sources


def build_after_graph(models: dict[str, str], layers: dict[str, str]) -> DbtModelGraph:
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for name, sql in models.items():
        nodes.append(
            GraphNode(
                id=name,
                label=name,
                layer=layers.get(name),
            )
        )
        for ref in extract_refs(sql):
            edges.append(GraphEdge(source=ref, target=name))
        for schema, table in extract_sources(sql):
            src_id = f"source.{schema}.{table}"
            if not any(n.id == src_id for n in nodes):
                nodes.append(GraphNode(id=src_id, label=f"{schema}.{table}", layer="source"))
            edges.append(GraphEdge(source=src_id, target=name))
    return DbtModelGraph(nodes=nodes, edges=edges)


def build_before_graph(
    nodes: list[dict],
    edges: list[dict],
) -> TransformationGraph:
    return TransformationGraph(
        nodes=[GraphNode(id=n["id"], label=n["label"], meta=n.get("meta", {})) for n in nodes],
        edges=[GraphEdge(source=e["source"], target=e["target"]) for e in edges],
    )
