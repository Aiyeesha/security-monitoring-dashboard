from __future__ import annotations
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from models import EventCreate, Metrics, SecurityEvent

_TEMPLATES = [
    dict(severity="critical", title="Ransomware activity detected",
         description="Mass file encryption on WORKSTATION-14 — possible WannaCry variant",
         source="EDR", category="Malware", host="WORKSTATION-14", ip="192.168.1.14"),
    dict(severity="critical", title="Domain admin account compromised",
         description="admin@corp.local logged in from 2 countries within 30 minutes",
         source="SIEM", category="Account Compromise", host="DC-01", ip="203.0.113.5"),
    dict(severity="high", title="SSH brute-force attack",
         description="450 failed SSH attempts from 203.0.113.42 in under 10 minutes",
         source="Firewall", category="Authentication", host="SERVER-01", ip="203.0.113.42"),
    dict(severity="high", title="Lateral movement — SMB scanning",
         description="WORKSTATION-07 probing 12 internal hosts on TCP/445",
         source="NDR", category="Lateral Movement", host="WORKSTATION-07", ip="192.168.1.7"),
    dict(severity="high", title="Data exfiltration attempt",
         description="8 GB outbound to unknown IP on port 443 in 15 minutes",
         source="DLP", category="Exfiltration", host="SERVER-DB", ip="198.51.100.7"),
    dict(severity="medium", title="Suspicious PowerShell execution",
         description="Encoded command executed with -EncodedCommand flag on WORKSTATION-22",
         source="EDR", category="Execution", host="WORKSTATION-22", ip="192.168.1.22"),
    dict(severity="medium", title="User added to Domain Admins",
         description="john.doe added to Domain Admins outside business hours",
         source="Active Directory", category="Privilege Escalation", host="DC-01", ip="192.168.1.1"),
    dict(severity="medium", title="Phishing email delivered",
         description="Email with malicious macro attachment bypassed spam filter — 3 recipients",
         source="Email Gateway", category="Phishing", host=None, ip=None),
    dict(severity="low", title="SSL certificate expiring",
         description="Certificate on WEB-01 expires in 7 days",
         source="Vulnerability Scanner", category="Configuration", host="WEB-01", ip="192.168.1.50"),
    dict(severity="low", title="Outdated software detected",
         description="OpenSSL 1.0.2 (EOL) on 4 endpoints — CVE-2022-0778 applicable",
         source="Vulnerability Scanner", category="Patch Management", host=None, ip=None),
    dict(severity="info", title="AV definitions updated",
         description="MalwareBytes definitions pushed to 42 endpoints via Datto RMM",
         source="RMM", category="Maintenance", host=None, ip=None),
    dict(severity="info", title="Scheduled backup completed",
         description="Acronis full backup for SRVWIN22 completed successfully",
         source="Backup", category="Maintenance", host="SRVWIN22", ip=None),
]


class EventStore:
    def __init__(self) -> None:
        self._events: List[SecurityEvent] = []
        self._seed()

    def _seed(self) -> None:
        now = datetime.utcnow()
        statuses = ["open", "open", "open", "investigating", "resolved"]
        for template in _TEMPLATES:
            event = SecurityEvent(
                id=str(uuid.uuid4()),
                timestamp=now - timedelta(minutes=random.randint(2, 480)),
                status=random.choice(statuses),
                **template,
            )
            self._events.append(event)

    def get_events(
        self,
        severity: Optional[str] = None,
        limit: int = 50,
    ) -> List[SecurityEvent]:
        events = self._events
        if severity:
            events = [e for e in events if e.severity == severity]
        return sorted(events, key=lambda e: e.timestamp, reverse=True)[:limit]

    def add_event(self, payload: EventCreate) -> SecurityEvent:
        event = SecurityEvent(**payload.model_dump())
        self._events.append(event)
        return event

    def generate_random_event(self) -> SecurityEvent:
        return self.add_event(EventCreate(**random.choice(_TEMPLATES)))

    def compute_metrics(self) -> Metrics:
        events = self._events
        cutoff = datetime.utcnow() - timedelta(hours=24)
        resolved_24h = [e for e in events if e.status == "resolved" and e.timestamp >= cutoff]
        mttr = (
            sum((datetime.utcnow() - e.timestamp).total_seconds() / 60 for e in resolved_24h)
            / len(resolved_24h)
            if resolved_24h
            else 0.0
        )
        return Metrics(
            total_events=len(events),
            open_events=sum(1 for e in events if e.status == "open"),
            critical_count=sum(1 for e in events if e.severity == "critical"),
            high_count=sum(1 for e in events if e.severity == "high"),
            medium_count=sum(1 for e in events if e.severity == "medium"),
            low_count=sum(1 for e in events if e.severity == "low"),
            resolved_last_24h=len(resolved_24h),
            mttr_minutes=round(mttr, 1),
        )
