"""Trilha de historico de alteracoes por item (JSONL)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ItemHistoryEvent:
    timestamp: str
    event_type: str
    item_key: str
    state: str
    action: str
    note_id: int | None
    error_type: str | None
    error_message: str | None
    metadata: dict[str, object]


class JsonlItemHistoryStore:
    """Persistencia simples de eventos em arquivo JSONL."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: ItemHistoryEvent) -> None:
        with self.file_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(event), ensure_ascii=True) + "\n")

    def query(
        self,
        item_key: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, object]]:
        if not self.file_path.exists():
            return []

        rows: list[dict[str, object]] = []
        with self.file_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                row = json.loads(line)
                if item_key is not None and row.get("item_key") != item_key:
                    continue
                if event_type is not None and row.get("event_type") != event_type:
                    continue
                rows.append(row)

        if limit is not None and limit >= 0:
            return rows[-limit:]
        return rows


def new_event(
    event_type: str,
    item_key: str,
    state: str,
    action: str,
    note_id: int | None,
    error_type: str | None,
    error_message: str | None,
    metadata: dict[str, object] | None = None,
) -> ItemHistoryEvent:
    return ItemHistoryEvent(
        timestamp=datetime.now(timezone.utc).isoformat(),
        event_type=event_type,
        item_key=item_key,
        state=state,
        action=action,
        note_id=note_id,
        error_type=error_type,
        error_message=error_message,
        metadata=metadata or {},
    )
