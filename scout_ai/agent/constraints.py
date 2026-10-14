"""Pull simple constraints out of a natural-language question."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Constraints:
    max_price: int | None
    tags: list[str]
    prefer_light: bool
    needs_gaming: bool


_PRICE_RE = re.compile(
    r"(?:under|below|less than|<=?)\s*\$?\s*([0-9]{3,5})",
    re.IGNORECASE,
)
_BUDGET_RE = re.compile(r"\$\s*([0-9]{3,5})", re.IGNORECASE)


def extract_constraints(question: str) -> Constraints:
    text = question.lower()

    max_price = None
    match = _PRICE_RE.search(question)
    if match:
        max_price = int(match.group(1))
    else:
        budget = _BUDGET_RE.search(question)
        if budget and any(word in text for word in ("under", "below", "budget", "max")):
            max_price = int(budget.group(1))

    tags: list[str] = []
    if any(word in text for word in ("coding", "developer", "programming", "software")):
        tags.append("programming")
    if any(word in text for word in ("travel", "portable", "lightweight", "light")):
        tags.append("travel")
    if "battery" in text:
        tags.append("battery")
    if any(word in text for word in ("budget", "cheap", "student")):
        tags.append("budget")
    if "gaming" in text or "game" in text:
        tags.append("gaming")

    prefer_light = any(word in text for word in ("travel", "portable", "lightweight", "light"))
    needs_gaming = "gaming" in text or "game" in text

    # de-dupe while keeping order
    seen: set[str] = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    return Constraints(
        max_price=max_price,
        tags=unique_tags,
        prefer_light=prefer_light,
        needs_gaming=needs_gaming,
    )
