# Security Monitoring Dashboard

Real-time security event monitoring dashboard built with **FastAPI** (Python) and **React** (TypeScript).

## Features

- Real-time security event streaming via WebSocket
- Alert severity classification (Critical / High / Medium / Low / Info)
- Metrics overview: open alerts, MTTR, resolved in 24h
- Filter by severity, source, and status
- Dark-theme responsive UI

## Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11, FastAPI, WebSocket |
| Frontend | React 18, TypeScript, Vite |
| Styling | CSS (dark theme, no framework) |
| Containers | Docker Compose |

## Quick Start

### With Docker Compose

```bash
docker-compose up
```

Then open [http://localhost:5173](http://localhost:5173).

### Manual Setup

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/events` | List events (optional `?severity=high&limit=50`) |
| `POST` | `/api/events` | Ingest a new event |
| `GET` | `/api/metrics` | Dashboard KPIs |
| `WS` | `/ws/events` | Real-time event stream |

## Project Structure

```
.
├── backend/
│   ├── main.py          # FastAPI app + WebSocket hub
│   ├── models.py        # Pydantic schemas
│   ├── data/
│   │   └── events.py    # In-memory store + event generator
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── App.css
│       ├── types.ts
│       └── components/
│           ├── Dashboard.tsx
│           ├── MetricsPanel.tsx
│           └── AlertList.tsx
└── docker-compose.yml
```

## License

MIT
