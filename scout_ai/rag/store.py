"""Postgres + pgvector persistence for document chunks."""

from __future__ import annotations

from dataclasses import dataclass

import psycopg
from pgvector.psycopg import register_vector

from scout_ai.config import settings


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    content: str
    chunk_index: int
    score: float


SCHEMA_SQL = f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector({settings.embedding_dims}) NOT NULL
);

CREATE INDEX IF NOT EXISTS document_chunks_source_idx
    ON document_chunks (source);
"""


def connect(*, register: bool = True) -> psycopg.Connection:
    conn = psycopg.connect(settings.database_url)
    if register:
        register_vector(conn)
    return conn


def init_schema() -> None:
    # Extension must exist before pgvector can register the vector type.
    with connect(register=False) as conn:
        conn.execute(SCHEMA_SQL)
        conn.commit()


def clear_chunks() -> None:
    with connect() as conn:
        conn.execute("DELETE FROM document_chunks")
        conn.commit()


def insert_chunks(
    rows: list[tuple[str, int, str, list[float]]],
) -> int:
    if not rows:
        return 0
    with connect() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO document_chunks (source, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                rows,
            )
        conn.commit()
    return len(rows)


def similarity_search(
    query_embedding: list[float],
    *,
    limit: int = 5,
) -> list[RetrievedChunk]:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT source, content, chunk_index,
                       1 - (embedding <=> %s::vector) AS score
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, query_embedding, limit),
            )
            rows = cur.fetchall()

    return [
        RetrievedChunk(
            source=row[0],
            content=row[1],
            chunk_index=row[2],
            score=float(row[3]),
        )
        for row in rows
    ]
