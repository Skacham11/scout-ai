import json

import pytest
from fastmcp import Client

from scout_ai.mcp_server import mcp
from scout_ai.rag.ingest import ingest_docs


@pytest.mark.asyncio
async def test_mcp_lists_expected_tools():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools}
        assert "search_catalog" in names
        assert "get_product" in names
        assert "retrieve_evidence" in names
        assert "compare_products" in names
        assert "research_laptops" in names


@pytest.mark.asyncio
async def test_mcp_search_and_retrieve():
    ingest_docs()
    async with Client(mcp) as client:
        search = await client.call_tool(
            "search_catalog",
            {"max_price": 1000, "tag": "programming"},
        )
        products = json.loads(search.data)
        assert isinstance(products, list)

        evidence = await client.call_tool(
            "retrieve_evidence",
            {"query": "coding laptop under 1000 RAM", "limit": 2},
        )
        citations = json.loads(evidence.data)
        assert citations
        assert "source" in citations[0]


@pytest.mark.asyncio
async def test_mcp_research_laptops():
    ingest_docs()
    async with Client(mcp) as client:
        result = await client.call_tool(
            "research_laptops",
            {"question": "best laptop under $1000 for programming"},
        )
        payload = json.loads(result.data)
        assert payload["top_pick"] is not None
        assert payload["citations"]
