# Scout AI

Laptop buying assistant. You ask a question, it recommends a few machines and shows where the facts came from.

Prices in the catalog are US list-ish snapshots, not live store prices.

## Stack so far

- FastAPI product API
- Postgres + pgvector RAG over local product docs
- LangGraph / FastMCP / React still coming

## Setup

Needs Docker Desktop and Python 3.11+ (3.12 recommended).

```bash
# start Postgres with pgvector
docker compose up -d

python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# chunk + embed docs into pgvector
scout-ingest
```

Copy `.env.example` to `.env` if you want to override the DB URL.

## Run the API

```bash
uvicorn scout_ai.main:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs

Routes:

- `GET /health`
- `GET /products`
- `GET /products?max_price=1000&tag=programming`
- `GET /products/{id}`
- `GET /retrieve?query=best%20coding%20laptop%20under%201000`

## Tests

```bash
docker compose up -d
pytest -q
```

## Data

- `data/catalog/laptops.json` — structured product rows
- `data/docs/*.md` — notes used by RAG (citations come from here)

## Git

- `main` — stable / demo
- `develop` — integration
- `feat/<name>` — off `develop`, then merge via PR
