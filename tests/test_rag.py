from scout_ai.rag.chunking import chunk_text, load_doc_chunks
from scout_ai.rag.embeddings import embed_text
from scout_ai.rag.ingest import DOCS_DIR, ingest_docs
from scout_ai.rag.retrieve import retrieve


def test_chunk_text_overlap():
    text = "word " * 200
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)


def test_embed_text_unit_length():
    vec = embed_text("32GB RAM for docker and coding")
    assert len(vec) == 384
    norm = sum(v * v for v in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_ingest_and_retrieve():
    assert list(DOCS_DIR.glob("*.md"))
    count = ingest_docs()
    assert count == len(load_doc_chunks(DOCS_DIR))
    assert count > 0

    hits = retrieve("best laptop under 1000 for software development RAM", limit=3)
    assert hits
    assert hits[0].source.endswith(".md")
    assert hits[0].content
