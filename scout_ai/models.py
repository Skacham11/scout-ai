"""Product and RAG response shapes used by the API."""

from pydantic import BaseModel, Field


class ProductSpecs(BaseModel):
    cpu: str
    ram_gb: int
    storage_gb: int
    display_inches: float
    display_resolution: str
    weight_lbs: float
    battery_wh: float
    gpu: str
    ports: list[str]
    os: str


class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    price_usd: int = Field(ge=0)
    source_url: str
    tags: list[str]
    summary: str
    specs: ProductSpecs


class Citation(BaseModel):
    source: str
    quote: str
    chunk_index: int
    score: float


class RetrieveResponse(BaseModel):
    query: str
    citations: list[Citation]
