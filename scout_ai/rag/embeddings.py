"""Local embeddings so the project runs without an API key.

This is a deterministic hashing embedder. Good enough for a local demo and
tests. You can swap in OpenAI / sentence-transformers later behind the same
`embed_texts` function.
"""

from __future__ import annotations

import hashlib
import math
import re

from scout_ai.config import settings

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def embed_text(text: str, dims: int | None = None) -> list[float]:
    dims = dims or settings.embedding_dims
    vec = [0.0] * dims
    tokens = _tokenize(text)
    if not tokens:
        return vec

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dims
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[index] += sign

    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def embed_texts(texts: list[str], dims: int | None = None) -> list[list[float]]:
    return [embed_text(text, dims=dims) for text in texts]
