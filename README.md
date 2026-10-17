# Scout AI

Laptop buying assistant. You ask a question, it recommends a few machines and shows where the facts came from.

Prices in the catalog are US list-ish snapshots, not live store prices.

## Stack

- FastAPI product API
- Postgres + pgvector RAG over local product docs
- LangGraph research agent (`POST /research`)
- FastMCP server (`scout-mcp`)
- React + TypeScript UI (`frontend/`)

## Setup

Needs Docker Desktop and Python 3.11+ (3.12 recommended).

```bash
docker compose up -d

python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
scout-ingest
```

## Run the API

```bash
uvicorn scout_ai.main:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs

## Run the frontend

```bash
cd frontend
yarn install
yarn dev
```

Open http://127.0.0.1:5173

The UI posts to `/api/research`, and Vite proxies that to the FastAPI server.

## Run the MCP server

```bash
scout-mcp
```

See `mcp.cursor.example.json` for a Cursor config sketch.

## Tests

```bash
docker compose up -d
pytest -q
cd frontend && yarn build
```

## Data

- `data/catalog/laptops.json` — structured product rows
- `data/docs/*.md` — notes used by RAG (citations come from here)

## Git

- `main` — stable / demo
- `develop` — integration
- `feat/<name>` — off `develop`, then merge via PR
