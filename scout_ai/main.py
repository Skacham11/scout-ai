"""FastAPI entrypoint for Scout AI."""

from fastapi import FastAPI, HTTPException, Query

from scout_ai.catalog import get_product, search_products
from scout_ai.models import Product

app = FastAPI(
    title="Scout AI",
    description="Laptop research assistant API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[Product])
def list_products(
    max_price: int | None = Query(default=None, ge=0),
    brand: str | None = Query(default=None),
    tag: str | None = Query(default=None),
) -> list[Product]:
    """Return catalog products, optionally filtered."""
    return search_products(max_price=max_price, brand=brand, tag=tag)


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: str) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product not found: {product_id}")
    return product
