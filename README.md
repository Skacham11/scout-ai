# Scout AI

Laptop buying assistant. You ask a question, it recommends a few machines and shows where the facts came from.

This is still early. Right now the repo is just the project layout and a small catalog of real laptops. Prices are US list-ish snapshots, not live store prices.

## Stack (planned)

- FastAPI
- Postgres + pgvector (RAG)
- LangGraph
- FastMCP
- React (simple UI)

## Setup

Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Catalog

See `data/catalog/laptops.json`. Specs come from public product listings. I am not scraping stores at query time.

## Git

- `main` — stable / demo
- `develop` — integration
- `feat/<name>` — off `develop`, then merge back

Do not commit straight to `main`.
