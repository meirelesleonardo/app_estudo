#!/usr/bin/env python3
"""Backfill de campos faltantes para validacao do lote piloto (CSP-006)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app_estudo.integrations.pilot_backfill import plan_backfill_updates

ENDPOINT = "http://127.0.0.1:8765"


def invoke(action: str, params: dict | None = None) -> object:
    if params is None:
        params = {}
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = request.Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with request.urlopen(req, timeout=20) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if body.get("error") is not None:
        raise RuntimeError(str(body["error"]))
    return body.get("result")


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill de campos do lote piloto")
    parser.add_argument("--deck", default="Ingles::Listening::B1")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    cards = invoke("findCards", {"query": f"deck:{args.deck}"})
    infos = invoke("cardsInfo", {"cards": cards}) if cards else []
    note_ids = sorted({c["note"] for c in infos})
    notes = invoke("notesInfo", {"notes": note_ids}) if note_ids else []

    touched_notes = 0
    changed_fields = 0
    backfilled_evaluation_score = 0
    backfilled_audio_reference = 0
    pending_audio_tagged = 0

    for note in notes:
        note_id = note.get("noteId")
        updates, extra_tags = plan_backfill_updates(note)
        if not updates and not extra_tags:
            continue

        touched_notes += 1
        changed_fields += len(updates)
        if "evaluation_score" in updates:
            backfilled_evaluation_score += 1
        if "audio_reference" in updates:
            backfilled_audio_reference += 1
        if "status:pending_audio_reference" in extra_tags:
            pending_audio_tagged += 1

        if args.apply:
            if updates:
                invoke("updateNoteFields", {"note": {"id": note_id, "fields": updates}})
            if extra_tags:
                invoke("addTags", {"notes": [note_id], "tags": " ".join(sorted(extra_tags))})

    print(
        json.dumps(
            {
                "deck": args.deck,
                "notes": len(note_ids),
                "touched_notes": touched_notes,
                "changed_fields": changed_fields,
                "backfilled_evaluation_score": backfilled_evaluation_score,
                "backfilled_audio_reference": backfilled_audio_reference,
                "pending_audio_tagged": pending_audio_tagged,
                "apply": args.apply,
            },
            ensure_ascii=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
