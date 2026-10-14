"""Turn catalog hits + citations into a structured recommendation."""

from __future__ import annotations

from scout_ai.agent.constraints import Constraints
from scout_ai.models import Citation, Product, ResearchResponse
from scout_ai.rag.store import RetrievedChunk


def _score_product(product: Product, constraints: Constraints) -> float:
    score = 0.0
    ram = product.specs.ram_gb

    if ram >= 32:
        score += 40
    elif ram >= 16:
        score += 25
    else:
        score -= 20

    if "programming" in product.tags:
        score += 15
    if constraints.prefer_light:
        if product.specs.weight_lbs <= 3.0:
            score += 20
        elif product.specs.weight_lbs <= 3.3:
            score += 10
        else:
            score -= 10
    if constraints.needs_gaming:
        if "rtx" in product.specs.gpu.lower() or "gaming" in product.tags:
            score += 25
        else:
            score -= 15
    if constraints.max_price is not None:
        # prefer spending less of the budget when specs are similar
        score += max(0, (constraints.max_price - product.price_usd) / 100)

    # hard reject tiny RAM for coding questions
    if "programming" in constraints.tags and ram < 16:
        score -= 50

    return score


def build_recommendation(
    question: str,
    constraints: Constraints,
    products: list[Product],
    chunks: list[RetrievedChunk],
) -> ResearchResponse:
    if not products:
        return ResearchResponse(
            question=question,
            top_pick=None,
            alternatives=[],
            why=[],
            disadvantages=["No products matched the filters."],
            missing_info=[
                "Catalog may not cover every market configuration.",
                "Prices are snapshots, not live store prices.",
            ],
            citations=[],
        )

    ranked = sorted(products, key=lambda p: _score_product(p, constraints), reverse=True)
    top = ranked[0]
    alts = ranked[1:3]

    why = [
        f"{top.name} is the top pick at ${top.price_usd}.",
        f"It has {top.specs.ram_gb}GB RAM and weighs {top.specs.weight_lbs} lb.",
    ]
    if constraints.max_price is not None:
        why.append(f"It fits the max budget of ${constraints.max_price}.")
    if "programming" in top.tags or top.specs.ram_gb >= 16:
        why.append("Memory and positioning look reasonable for software work.")

    disadvantages = [top.summary]
    if top.specs.ram_gb < 32:
        disadvantages.append("More RAM would be safer for heavy Docker use.")
    if constraints.needs_gaming and "rtx" not in top.specs.gpu.lower():
        disadvantages.append("This pick is weak for serious gaming.")

    missing_info = [
        "Prices are catalog snapshots and may differ in stores.",
        "We do not have live inventory or current street prices.",
        "Keyboard feel and real-world battery hours are only summarized in local notes.",
    ]

    citations = [
        Citation(
            source=chunk.source,
            quote=chunk.content,
            chunk_index=chunk.chunk_index,
            score=round(chunk.score, 4),
        )
        for chunk in chunks
    ]

    return ResearchResponse(
        question=question,
        top_pick=top,
        alternatives=alts,
        why=why,
        disadvantages=disadvantages[:4],
        missing_info=missing_info,
        citations=citations,
        tools_used=["search_catalog", "retrieve_evidence", "compare_products"],
    )
