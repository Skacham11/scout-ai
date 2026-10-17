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

## Claude Desktop (MCP)

Keep Postgres up and docs ingested first:

```bash
docker compose up -d
scout-ingest
```

Add this to Claude Desktop → Settings → Developer → Edit Config
(`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "scout-ai": {
      "command": "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI/.venv/bin/python",
      "args": ["-m", "scout_ai.mcp_server"],
      "cwd": "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI"
    }
  }
}
```

Fully quit Claude Desktop (Cmd+Q) and reopen. You should see tools like
`search_catalog`, `retrieve_evidence`, and `research_laptops`.

Same config is saved in `mcp.claude.example.json`.

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
