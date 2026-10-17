from scout_ai.agent.constraints import extract_constraints
from scout_ai.agent.graph import run_research
from scout_ai.rag.ingest import ingest_docs


def test_extract_constraints_price_and_coding():
    constraints = extract_constraints(
        "Find me the best laptop under $1000 for software development"
    )
    assert constraints.max_price == 1000
    assert "programming" in constraints.tags


def test_run_research_returns_structured_answer():
    ingest_docs()
    result = run_research(
        "Find me the best laptop under $1000 for software development"
    )
    assert result.top_pick is not None
    assert result.top_pick.price_usd <= 1000
    assert result.why
    assert result.disadvantages
    assert result.missing_info
    assert result.citations
    assert "extract_constraints" in result.steps
    assert any(step.startswith("search_catalog") for step in result.steps)
    assert "retrieve_evidence" in result.steps
    assert "recommend" in result.steps
