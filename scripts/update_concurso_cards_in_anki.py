#!/usr/bin/env python3
"""Atualiza cards de concurso no Anki por QuestionID dentro de um deck."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_ENDPOINT = "http://127.0.0.1:8765"


def invoke(endpoint: str, action: str, params: dict | None = None) -> object:
    payload = {"action": action, "version": 6, "params": params or {}}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Falha de conectividade com AnkiConnect: {exc}") from exc

    if data.get("error"):
        raise RuntimeError(f"Erro AnkiConnect em {action}: {data['error']}")
    return data.get("result")


def find_note_ids(endpoint: str, deck_name: str, question_id: str) -> list[int]:
    query = f'deck:"{deck_name}" "QuestionID:{question_id}"'
    result = invoke(endpoint, "findNotes", {"query": query})
    if not isinstance(result, list):
        return []
    return [x for x in result if isinstance(x, int)]


def update_from_csv(endpoint: str, deck_name: str, csv_path: Path) -> dict[str, object]:
    updated = 0
    missing = 0
    errors: list[dict[str, str]] = []

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_id = (row.get("question_id") or "").strip()
            if not question_id:
                continue

            note_ids = find_note_ids(endpoint, deck_name, question_id)
            if not note_ids:
                missing += 1
                continue

            fields = {
                "Front": row.get("front") or "",
                "Back": row.get("back") or "",
                "Topic": row.get("topic") or "",
            }

            tags = [tag for tag in (row.get("tags") or "").split() if tag]

            for note_id in note_ids:
                try:
                    invoke(
                        endpoint,
                        "updateNoteFields",
                        {"note": {"id": note_id, "fields": fields}},
                    )
                    if tags:
                        invoke(endpoint, "addTags", {"notes": [note_id], "tags": " ".join(tags)})
                    updated += 1
                except RuntimeError as exc:
                    errors.append({"question_id": question_id, "error": str(exc)})

    return {
        "deck_name": deck_name,
        "csv_path": str(csv_path),
        "updated": updated,
        "missing": missing,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Atualiza cards de concurso no Anki")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    report = update_from_csv(
        endpoint=args.endpoint,
        deck_name=args.deck,
        csv_path=Path(args.csv),
    )

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))

    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
