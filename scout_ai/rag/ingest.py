"""Ingest markdown docs into Postgres/pgvector."""

from __future__ import annotations

from pathlib import Path

from scout_ai.rag.chunking import load_doc_chunks
from scout_ai.rag.embeddings import embed_texts
from scout_ai.rag.store import clear_chunks, init_schema, insert_chunks

DOCS_DIR = Path(__file__).resolve().parents[2] / "data" / "docs"


def ingest_docs(docs_dir: Path | None = None) -> int:
    docs_dir = docs_dir or DOCS_DIR
    chunks = load_doc_chunks(docs_dir)
    embeddings = embed_texts([c.content for c in chunks])

    init_schema()
    clear_chunks()
    rows = [
        (chunk.source, chunk.chunk_index, chunk.content, embedding)
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]
    return insert_chunks(rows)


def main() -> None:
    count = ingest_docs()
    print(f"Ingested {count} chunks from {DOCS_DIR}")


if __name__ == "__main__":
    main()
