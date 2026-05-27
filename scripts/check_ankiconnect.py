#!/usr/bin/env python3
"""Script de linha de comando para validar conectividade com AnkiConnect."""

from __future__ import annotations

import argparse
import json
import sys

from app_estudo.integrations.ankiconnect_healthcheck import (
    DEFAULT_ANKI_ENDPOINT,
    check_ankiconnect,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Healthcheck local do AnkiConnect")
    parser.add_argument("--endpoint", default=DEFAULT_ANKI_ENDPOINT)
    parser.add_argument("--timeout", default=2.0, type=float)
    args = parser.parse_args()

    result = check_ankiconnect(endpoint=args.endpoint, timeout=args.timeout)
    print(json.dumps(result.__dict__, ensure_ascii=True))

    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
