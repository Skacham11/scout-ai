# Scout AI

Laptop buying assistant. You ask a question, it recommends a few machines and shows where the facts came from.

Prices in the catalog are US list-ish snapshots, not live store prices.

## Stack

- FastAPI product API
- Postgres + pgvector RAG over local product docs
- LangGraph research agent (`POST /research`)
- FastMCP server (`scout-mcp`)
- React + TypeScript UI (`frontend/`)

## First-time setup

Needs Docker Desktop and Python 3.11+ (3.12 recommended).

```bash
cd "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI"

docker compose up -d

python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
scout-ingest

cd frontend
yarn install
```

## Run the app (every day)

Use **two terminals**.

### Terminal 1 — backend

```bash
cd "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI"
docker compose up -d
source .venv/bin/activate
scout-ingest
uvicorn scout_ai.main:app --reload --port 8000
```

- API docs: http://127.0.0.1:8000/docs

### Terminal 2 — frontend

```bash
cd "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI/frontend"
yarn dev
```

- UI: http://127.0.0.1:5173

The UI posts to `/api/research`, and Vite proxies that to the FastAPI server on port 8000.

## Claude Desktop (MCP)

Keep Postgres up and docs ingested (same as Terminal 1 above, without needing uvicorn if you only use Claude).

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
cd "/Users/surajkacham/Dropbox/Mac/Desktop/Scout AI"
docker compose up -d
source .venv/bin/activate
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
