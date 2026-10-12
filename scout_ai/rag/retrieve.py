"""Retrieve cited passages for a research question."""

from __future__ import annotations

from scout_ai.rag.embeddings import embed_text
from scout_ai.rag.store import RetrievedChunk, similarity_search


def retrieve(query: str, *, limit: int = 5) -> list[RetrievedChunk]:
    query = query.strip()
    if not query:
        return []
    embedding = embed_text(query)
    return similarity_search(embedding, limit=limit)
