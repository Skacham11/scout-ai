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

Python 3.11+ (3.12 recommended).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the API

```bash
uvicorn scout_ai.main:app --reload --port 8000
```

Then open http://127.0.0.1:8000/docs

Useful routes:

- `GET /health`
- `GET /products`
- `GET /products?max_price=1000&tag=programming`
- `GET /products/{id}`

## Tests

```bash
pytest -q
```

## Catalog

See `data/catalog/laptops.json`. Specs come from public product listings. I am not scraping stores at query time.

## Git

- `main` — stable / demo
- `develop` — integration
- `feat/<name>` — off `develop`, then merge back

Do not commit straight to `main`.
