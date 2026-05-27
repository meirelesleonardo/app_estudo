#!/usr/bin/env python3
"""Valida lote piloto do MVP contra criterios de aceite."""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app_estudo.integrations.ankiconnect_client import AnkiConnectClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida lote piloto do MVP")
    parser.add_argument("--deck", default="Ingles::Listening::B1")
    parser.add_argument("--min-items", type=int, default=20)
    parser.add_argument("--traceability-threshold", type=float, default=95.0)
    parser.add_argument("--duplicate-rate-threshold", type=float, default=2.0)
    parser.add_argument("--classification-threshold", type=float, default=100.0)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8765")
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    client = AnkiConnectClient(endpoint=args.endpoint, timeout=args.timeout, model_name="AppEstudoListening")
    report = client.validate_mvp_pilot(
        deck_name=args.deck,
        min_items=args.min_items,
        traceability_threshold=args.traceability_threshold,
        duplicate_rate_threshold=args.duplicate_rate_threshold,
        classification_threshold=args.classification_threshold,
    )

    print(json.dumps(report, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
