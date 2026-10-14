"""LangGraph research workflow.

Flow:
  extract_constraints -> search_catalog -> retrieve_evidence -> recommend -> END

This is a real multi-step graph. Each node calls a tool or builds structured output.
"""

from __future__ import annotations

import json
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from scout_ai.agent.constraints import Constraints, extract_constraints
from scout_ai.agent.recommender import build_recommendation
from scout_ai.agent.tools import (
    tool_compare_products,
    tool_retrieve_evidence,
    tool_search_catalog,
)
from scout_ai.catalog import get_product
from scout_ai.models import Product, ResearchResponse
from scout_ai.rag.store import RetrievedChunk


def _append_steps(existing: list[str], new: list[str]) -> list[str]:
    return existing + new


class AgentState(TypedDict):
    question: str
    max_price: int | None
    tags: list[str]
    prefer_light: bool
    needs_gaming: bool
    product_ids: list[str]
    products: list[Product]
    chunks: list[RetrievedChunk]
    recommendation: ResearchResponse | None
    steps: Annotated[list[str], _append_steps]


def extract_constraints_node(state: AgentState) -> dict:
    constraints = extract_constraints(state["question"])
    return {
        "max_price": constraints.max_price,
        "tags": constraints.tags,
        "prefer_light": constraints.prefer_light,
        "needs_gaming": constraints.needs_gaming,
        "steps": ["extract_constraints"],
    }


def search_catalog_node(state: AgentState) -> dict:
    # Prefer programming/value tags when present; fall back to price-only.
    tag = None
    for candidate in ("programming", "gaming", "travel", "budget"):
        if candidate in state["tags"]:
            tag = candidate
            break

    raw = tool_search_catalog(max_price=state["max_price"], tag=tag)
    rows = json.loads(raw)

    # If a strict tag filter returned nothing, retry with price only.
    if not rows and tag is not None:
        raw = tool_search_catalog(max_price=state["max_price"])
        rows = json.loads(raw)

    products = []
    for row in rows:
        product = get_product(row["id"])
        if product is not None:
            products.append(product)

    return {
        "products": products,
        "product_ids": [p.id for p in products],
        "steps": [f"search_catalog(tag={tag}, max_price={state['max_price']})"],
    }


def retrieve_evidence_node(state: AgentState) -> dict:
    raw = tool_retrieve_evidence(state["question"], limit=4)
    rows = json.loads(raw)
    chunks = [
        RetrievedChunk(
            source=row["source"],
            content=row["quote"],
            chunk_index=row["chunk_index"],
            score=row["score"],
        )
        for row in rows
    ]
    return {
        "chunks": chunks,
        "steps": ["retrieve_evidence"],
    }


def recommend_node(state: AgentState) -> dict:
    # Optional compare step for the top few candidates.
    top_ids = state["product_ids"][:3]
    if top_ids:
        tool_compare_products(top_ids)

    constraints = Constraints(
        max_price=state["max_price"],
        tags=state["tags"],
        prefer_light=state["prefer_light"],
        needs_gaming=state["needs_gaming"],
    )
    recommendation = build_recommendation(
        question=state["question"],
        constraints=constraints,
        products=state["products"],
        chunks=state["chunks"],
    )
    return {
        "recommendation": recommendation,
        "steps": ["recommend"],
    }


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("extract_constraints", extract_constraints_node)
    graph.add_node("search_catalog", search_catalog_node)
    graph.add_node("retrieve_evidence", retrieve_evidence_node)
    graph.add_node("recommend", recommend_node)

    graph.add_edge(START, "extract_constraints")
    graph.add_edge("extract_constraints", "search_catalog")
    graph.add_edge("search_catalog", "retrieve_evidence")
    graph.add_edge("retrieve_evidence", "recommend")
    graph.add_edge("recommend", END)
    return graph.compile()


_GRAPH = None


def get_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_graph()
    return _GRAPH


def run_research(question: str) -> ResearchResponse:
    graph = get_graph()
    result = graph.invoke(
        {
            "question": question,
            "max_price": None,
            "tags": [],
            "prefer_light": False,
            "needs_gaming": False,
            "product_ids": [],
            "products": [],
            "chunks": [],
            "recommendation": None,
            "steps": [],
        }
    )
    recommendation = result["recommendation"]
    assert recommendation is not None
    recommendation.steps = result["steps"]
    return recommendation
