"""FastAPI entrypoint for Scout AI."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from scout_ai.agent.graph import run_research
from scout_ai.catalog import get_product, search_products
from scout_ai.models import (
    Citation,
    Product,
    ResearchRequest,
    ResearchResponse,
    RetrieveResponse,
)
from scout_ai.rag.retrieve import retrieve

app = FastAPI(
    title="Scout AI",
    description="Laptop research assistant API",
    version="0.5.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/retrieve", response_model=RetrieveResponse)
def retrieve_evidence(
    query: str = Query(min_length=1),
    limit: int = Query(default=5, ge=1, le=20),
) -> RetrieveResponse:
    """RAG search over local product docs. Returns cited passages."""
    chunks = retrieve(query, limit=limit)
    citations = [
        Citation(
            source=chunk.source,
            quote=chunk.content,
            chunk_index=chunk.chunk_index,
            score=round(chunk.score, 4),
        )
        for chunk in chunks
    ]
    return RetrieveResponse(query=query, citations=citations)


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    """Run the LangGraph research workflow for a buying question."""
    return run_research(request.question)
