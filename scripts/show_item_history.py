#!/usr/bin/env python3
"""Consulta historico de alteracoes por item."""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app_estudo.integrations.item_history import JsonlItemHistoryStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta historico de itens")
    parser.add_argument("--file", default="data/audit/anki_item_events.jsonl")
    parser.add_argument("--item-key")
    parser.add_argument("--event-type")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    store = JsonlItemHistoryStore(args.file)
    rows = store.query(item_key=args.item_key, event_type=args.event_type, limit=args.limit)

    print(json.dumps({"count": len(rows), "events": rows}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
