"""Load and filter the local product catalog.

Phase 1 keeps products in JSON. Later phases can swap this for Postgres
without changing the API routes much.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from scout_ai.models import Product

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "catalog" / "laptops.json"


@lru_cache(maxsize=1)
def load_products() -> list[Product]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return [Product.model_validate(item) for item in raw]


def get_product(product_id: str) -> Product | None:
    for product in load_products():
        if product.id == product_id:
            return product
    return None


def search_products(
    *,
    max_price: int | None = None,
    brand: str | None = None,
    tag: str | None = None,
) -> list[Product]:
    results = load_products()

    if max_price is not None:
        results = [p for p in results if p.price_usd <= max_price]

    if brand is not None:
        brand_lower = brand.lower()
        results = [p for p in results if p.brand.lower() == brand_lower]

    if tag is not None:
        tag_lower = tag.lower()
        results = [p for p in results if tag_lower in [t.lower() for t in p.tags]]

    return results
