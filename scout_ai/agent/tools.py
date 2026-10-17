"""Tools the agent can call. Same ideas will be reused by MCP later."""

from __future__ import annotations

import json

from scout_ai.catalog import get_product, search_products
from scout_ai.rag.retrieve import retrieve


def tool_search_catalog(
    max_price: int | None = None,
    brand: str | None = None,
    tag: str | None = None,
) -> str:
    """Search the laptop catalog with optional filters."""
    products = search_products(max_price=max_price, brand=brand, tag=tag)
    payload = [
        {
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "price_usd": p.price_usd,
            "tags": p.tags,
            "summary": p.summary,
            "ram_gb": p.specs.ram_gb,
            "weight_lbs": p.specs.weight_lbs,
            "gpu": p.specs.gpu,
            "battery_wh": p.specs.battery_wh,
        }
        for p in products
    ]
    return json.dumps(payload)


def tool_get_product(product_id: str) -> str:
    """Fetch one product by id."""
    product = get_product(product_id)
    if product is None:
        return json.dumps({"error": f"not found: {product_id}"})
    return product.model_dump_json()


def tool_retrieve_evidence(query: str, limit: int = 5) -> str:
    """Retrieve cited passages from the local document store."""
    chunks = retrieve(query, limit=limit)
    payload = [
        {
            "source": c.source,
            "quote": c.content,
            "chunk_index": c.chunk_index,
            "score": round(c.score, 4),
        }
        for c in chunks
    ]
    return json.dumps(payload)


def tool_compare_products(product_ids: list[str]) -> str:
    """Compare a few products side by side on key specs."""
    rows = []
    for product_id in product_ids:
        product = get_product(product_id)
        if product is None:
            rows.append({"id": product_id, "error": "not found"})
            continue
        rows.append(
            {
                "id": product.id,
                "name": product.name,
                "price_usd": product.price_usd,
                "ram_gb": product.specs.ram_gb,
                "storage_gb": product.specs.storage_gb,
                "weight_lbs": product.specs.weight_lbs,
                "battery_wh": product.specs.battery_wh,
                "gpu": product.specs.gpu,
                "os": product.specs.os,
            }
        )
    return json.dumps(rows)
