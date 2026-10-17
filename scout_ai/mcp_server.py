"""FastMCP server for Scout AI.

Exposes the same catalog/RAG tools that the LangGraph agent uses, so Cursor
or another MCP client can research laptops without going through the React UI.
"""

from __future__ import annotations

from fastmcp import FastMCP

from scout_ai.agent.graph import run_research
from scout_ai.agent.tools import (
    tool_compare_products,
    tool_get_product,
    tool_retrieve_evidence,
    tool_search_catalog,
)

mcp = FastMCP(
    name="Scout AI",
    instructions=(
        "Laptop research tools backed by a local catalog and document store. "
        "Use search_catalog and retrieve_evidence before recommending a product."
    ),
)


@mcp.tool
def search_catalog(
    max_price: int | None = None,
    brand: str | None = None,
    tag: str | None = None,
) -> str:
    """Search the laptop catalog. Optional filters: max_price, brand, tag."""
    return tool_search_catalog(max_price=max_price, brand=brand, tag=tag)


@mcp.tool
def get_product(product_id: str) -> str:
    """Get one product by id, including full specs."""
    return tool_get_product(product_id)


@mcp.tool
def retrieve_evidence(query: str, limit: int = 5) -> str:
    """Retrieve cited passages from local product docs (RAG / pgvector)."""
    return tool_retrieve_evidence(query, limit=limit)


@mcp.tool
def compare_products(product_ids: list[str]) -> str:
    """Compare products side by side on price, RAM, weight, GPU, and OS."""
    return tool_compare_products(product_ids)


@mcp.tool
def research_laptops(question: str) -> str:
    """Run the full research workflow and return a structured recommendation."""
    result = run_research(question)
    return result.model_dump_json()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
