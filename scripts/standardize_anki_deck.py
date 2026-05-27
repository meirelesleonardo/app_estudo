#!/usr/bin/env python3
"""Padroniza cards do Anki para o padrao documental do projeto."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from urllib import request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

ENDPOINT = "http://127.0.0.1:8765"
SIGNATURE_FIELDS = {
    "source_id",
    "target_expression",
    "explanation_ptbr",
    "listening_context",
    "created_from_stage",
}


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
    with request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    if body.get("error") is not None:
        raise RuntimeError(str(body["error"]))

    return body.get("result")


def infer_level(note: dict, default_level: str) -> str:
    fields = note.get("fields", {})
    tags = note.get("tags", [])

    if "level" in fields:
        value = str(fields["level"].get("value", "")).strip().upper()
        if value in {"A1", "A2", "B1", "B2", "C1"}:
            return value

    for tag in tags:
        low = tag.lower().strip()
        if low.startswith("nivel:"):
            candidate = low.split(":", 1)[1].upper()
            if candidate in {"A1", "A2", "B1", "B2", "C1"}:
                return candidate

    return default_level


def is_candidate(note: dict) -> bool:
    fields = note.get("fields", {})
    tags = set(note.get("tags", []))
    if set(fields.keys()) & SIGNATURE_FIELDS:
        return True
    if "modulo:ingles" in tags and "habilidade:listening" in tags:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Padroniza cards do deck English para Ingles::Listening::<nivel>")
    parser.add_argument("--source-deck", default="English")
    parser.add_argument("--default-level", default="B1")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force-all-source", action="store_true")
    args = parser.parse_args()

    cards = invoke("findCards", {"query": f"deck:{args.source_deck}"})
    if not isinstance(cards, list):
        raise RuntimeError("findCards retornou formato invalido")

    cards_info = invoke("cardsInfo", {"cards": cards}) if cards else []
    note_ids = sorted({card["note"] for card in cards_info})
    notes_info = invoke("notesInfo", {"notes": note_ids}) if note_ids else []

    card_ids_by_note = defaultdict(list)
    for card in cards_info:
        card_ids_by_note[card["note"]].append(card["cardId"])

    plan = []
    for note in notes_info:
        if not isinstance(note, dict):
            continue
        if not args.force_all_source and not is_candidate(note):
            continue

        level = infer_level(note, args.default_level)
        target_deck = f"Ingles::Listening::{level}"
        ids = card_ids_by_note.get(note.get("noteId"), [])
        if not ids:
            continue

        plan.append(
            {
                "noteId": note.get("noteId"),
                "cardIds": ids,
                "targetDeck": target_deck,
                "modelName": note.get("modelName"),
            }
        )

    moved = 0
    if args.apply:
        grouped = defaultdict(list)
        for row in plan:
            grouped[row["targetDeck"]].extend(row["cardIds"])

        for target_deck, target_cards in grouped.items():
            invoke("createDeck", {"deck": target_deck})
            invoke("changeDeck", {"cards": target_cards, "deck": target_deck})
            moved += len(target_cards)

    print(
        json.dumps(
            {
                "sourceDeck": args.source_deck,
                "cardsInSource": len(cards),
                "candidateNotes": len(plan),
                "cardsToMove": sum(len(row["cardIds"]) for row in plan),
                "apply": args.apply,
                "movedCards": moved,
                "preview": plan[:20],
            },
            ensure_ascii=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
