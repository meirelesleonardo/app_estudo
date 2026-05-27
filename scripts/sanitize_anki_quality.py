#!/usr/bin/env python3
"""Saneamento qualitativo de notas Anki no padrao AppEstudo."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


def normalize_spaces(value: str) -> str:
    return " ".join(value.split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Saneia tags e metadados de notas migradas")
    parser.add_argument("--deck", default="Ingles::Listening::B1")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    cards = invoke("findCards", {"query": f"deck:{args.deck}"})
    infos = invoke("cardsInfo", {"cards": cards}) if cards else []
    note_ids = sorted({c["note"] for c in infos})
    notes = invoke("notesInfo", {"notes": note_ids}) if note_ids else []

    touched_notes = 0
    changed_fields = 0
    removed_legacy_tags = 0
    added_standard_tags = 0

    base_tags = {
        "modulo:ingles",
        "habilidade:listening",
        "nivel:b1",
        "status:curated",
        "origem:curated",
        "avaliacao:pending_review",
    }

    for note in notes:
        note_id = note.get("noteId")
        tags = [t.strip().lower() for t in note.get("tags", []) if t and t.strip()]
        fields = note.get("fields", {})

        legacy_tags = [t for t in tags if t in {"origem:legacy_anki", "avaliacao:legacy_migrated"}]
        clean_tags = [t for t in tags if t not in {"origem:legacy_anki", "avaliacao:legacy_migrated"}]
        merged_tags = sorted(set(clean_tags) | base_tags)

        field_updates: dict[str, str] = {}

        source_type = str(fields.get("source_type", {}).get("value", "")).strip()
        if source_type == "legacy_anki":
            field_updates["source_type"] = "curated_migration"

        eval_class = str(fields.get("evaluation_classification", {}).get("value", "")).strip()
        if eval_class in {"legacy_migrated", ""}:
            field_updates["evaluation_classification"] = "pending_review"

        context = str(fields.get("listening_context", {}).get("value", "")).strip()
        if context:
            norm_context = normalize_spaces(context)
            if norm_context != context:
                field_updates["listening_context"] = norm_context

        if not legacy_tags and not field_updates and set(tags) == set(merged_tags):
            continue

        touched_notes += 1
        removed_legacy_tags += len(legacy_tags)

        extra_tags_added = len(set(merged_tags) - set(tags))
        added_standard_tags += extra_tags_added

        if field_updates:
            changed_fields += len(field_updates)

        if args.apply:
            if legacy_tags:
                invoke("removeTags", {"notes": [note_id], "tags": " ".join(sorted(set(legacy_tags)))})
            if merged_tags:
                invoke("addTags", {"notes": [note_id], "tags": " ".join(merged_tags)})
            if field_updates:
                invoke("updateNoteFields", {"note": {"id": note_id, "fields": field_updates}})

    print(
        json.dumps(
            {
                "deck": args.deck,
                "notes": len(note_ids),
                "touched_notes": touched_notes,
                "removed_legacy_tags": removed_legacy_tags,
                "added_standard_tags": added_standard_tags,
                "changed_fields": changed_fields,
                "apply": args.apply,
            },
            ensure_ascii=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
