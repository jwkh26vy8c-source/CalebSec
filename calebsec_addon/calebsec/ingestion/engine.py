from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Iterable

from calebsec.core.models import Alert, LogEvent
from calebsec.sigma.rules import SigmaRule


class IngestionEngine:
    def __init__(self) -> None:
        self.events: list[LogEvent] = []
        self.alerts: list[Alert] = []
        self.rules: list[SigmaRule] = []

    def set_rules(self, rules: Iterable[SigmaRule]) -> None:
        self.rules = list(rules)

    def ingest(self, event: LogEvent) -> list[Alert]:
        self.events.append(event)
        generated: list[Alert] = []
        for rule in self.rules:
            matched, fields = rule.match(event)
            if matched:
                alert = Alert(
                    rule_id=rule.rule_id,
                    title=rule.title,
                    level=rule.level,
                    event=event,
                    matched_fields=fields,
                )
                self.alerts.append(alert)
                generated.append(alert)
        return generated

    async def tail_file(self, file_path: str) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

        with path.open("r", encoding="utf-8", errors="replace") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    await asyncio.sleep(0.5)
                    continue
                line = line.strip()
                if not line:
                    continue
                self.ingest(parse_log_line(line, source=str(path)))


def parse_log_line(line: str, source: str = "file") -> LogEvent:
    try:
        payload = json.loads(line)
        if isinstance(payload, dict):
            raw = dict(payload)
            message = str(raw.pop("message", line))
            return LogEvent(
                source=str(raw.pop("source", source)),
                message=message,
                event_id=raw.pop("event_id", None),
                user=raw.pop("user", None),
                src_ip=raw.pop("src_ip", None),
                host=raw.pop("host", None),
                raw=raw,
            )
    except json.JSONDecodeError:
        pass

    return LogEvent(source=source, message=line)
