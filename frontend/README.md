# Scout AI frontend

Simple React + TypeScript UI for the research API.

```bash
yarn install
yarn dev
```

`npm install` can misbehave in folders with spaces in the path, so this app uses Yarn.

Open http://127.0.0.1:5173

The Vite proxy sends `/api/...` to FastAPI on port 8000, so run the backend too.
