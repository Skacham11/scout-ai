"""Split markdown docs into overlapping text chunks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TextChunk:
    source: str
    content: str
    chunk_index: int


def chunk_text(text: str, *, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def chunk_markdown_file(path: Path) -> list[TextChunk]:
    content = path.read_text(encoding="utf-8")
    pieces = chunk_text(content)
    return [
        TextChunk(source=path.name, content=piece, chunk_index=i)
        for i, piece in enumerate(pieces)
    ]


def load_doc_chunks(docs_dir: Path) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for path in sorted(docs_dir.glob("*.md")):
        chunks.extend(chunk_markdown_file(path))
    return chunks
