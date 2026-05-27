#!/usr/bin/env python3
"""Executa reconciliacao de duplicatas por source_id no Anki."""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app_estudo.integrations import AnkiConnectClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconciliacao de duplicatas por source_id")
    parser.add_argument("--deck", default="Ingles::Listening::B1")
    parser.add_argument("--strategy", default="keep_oldest", choices=["keep_oldest", "keep_newest"])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    client = AnkiConnectClient(model_name="AppEstudoListening")
    report = client.reconcile_duplicates_in_deck(
        deck_name=args.deck,
        strategy=args.strategy,
        dry_run=not args.apply,
    )

    print(json.dumps(report, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
