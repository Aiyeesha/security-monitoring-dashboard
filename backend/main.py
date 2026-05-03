from __future__ import annotations
import asyncio
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from data.events import EventStore
from models import EventCreate, Metrics, SecurityEvent

app = FastAPI(title="Security Monitoring Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store = EventStore()
_connections: List[WebSocket] = []


async def _broadcast(message: str) -> None:
    dead: List[WebSocket] = []
    for ws in _connections:
        try:
            await ws.send_text(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _connections.remove(ws)


@app.get("/api/events", response_model=List[SecurityEvent])
async def list_events(severity: str | None = None, limit: int = 50):
    return store.get_events(severity=severity, limit=limit)


@app.post("/api/events", response_model=SecurityEvent, status_code=201)
async def ingest_event(payload: EventCreate):
    event = store.add_event(payload)
    await _broadcast(event.model_dump_json())
    return event


@app.get("/api/metrics", response_model=Metrics)
async def get_metrics():
    return store.compute_metrics()


@app.websocket("/ws/events")
async def ws_events(websocket: WebSocket):
    await websocket.accept()
    _connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(6)
            event = store.generate_random_event()
            await _broadcast(event.model_dump_json())
    except WebSocketDisconnect:
        if websocket in _connections:
            _connections.remove(websocket)
