from __future__ import annotations
import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

SeverityLevel = Literal["critical", "high", "medium", "low", "info"]
EventStatus = Literal["open", "investigating", "resolved"]


class SecurityEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: SeverityLevel
    title: str
    description: str
    source: str
    category: str
    status: EventStatus = "open"
    host: str | None = None
    ip: str | None = None


class EventCreate(BaseModel):
    severity: SeverityLevel
    title: str
    description: str
    source: str
    category: str
    host: str | None = None
    ip: str | None = None


class Metrics(BaseModel):
    total_events: int
    open_events: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    resolved_last_24h: int
    mttr_minutes: float
