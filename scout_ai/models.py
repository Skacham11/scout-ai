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


class ResearchRequest(BaseModel):
    question: str = Field(min_length=3)


class ResearchResponse(BaseModel):
    question: str
    top_pick: Product | None
    alternatives: list[Product]
    why: list[str]
    disadvantages: list[str]
    missing_info: list[str]
    citations: list[Citation]
    tools_used: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
