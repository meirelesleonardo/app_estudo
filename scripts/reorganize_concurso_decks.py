#!/usr/bin/env python3
"""Reorganiza cards de concurso por materia/submateria em subdecks do Anki.

Padrao seguro:
- modo preview por default (nao move nada)
- --apply para efetivar mudancas
"""

from __future__ import annotations

import argparse
import json
import unicodedata
from collections import Counter, defaultdict
from typing import Iterable
from urllib import request

ENDPOINT = "http://127.0.0.1:8765"


def invoke(action: str, params: dict | None = None) -> object:
    payload = json.dumps(
        {"action": action, "version": 6, "params": params or {}},
        ensure_ascii=True,
    ).encode("utf-8")
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


def normalize_token(value: str) -> str:
    # Normaliza espacos/quebras de linha para evitar nomes de deck instaveis.
    compact = " ".join((value or "").split())
    ascii_text = unicodedata.normalize("NFKD", compact).encode("ascii", "ignore").decode("ascii")
    cleaned = []
    for ch in ascii_text:
        if ch.isalnum():
            cleaned.append(ch)
        else:
            cleaned.append("_")

    normalized = "".join(cleaned)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    return normalized or "SemTopico"


def split_topic(topic: str) -> tuple[str, str]:
    raw = (topic or "").strip()
    if not raw:
        return ("SemTopico", "SemSubtopico")

    if " - " in raw:
        left, right = raw.split(" - ", 1)
        return (normalize_token(left), normalize_token(right))

    if "/" in raw:
        left, right = raw.split("/", 1)
        return (normalize_token(left), normalize_token(right))

    return (normalize_token(raw), "Geral")


def collect_cards(source_decks: Iterable[str]) -> tuple[list[dict], list[dict]]:
    card_ids: list[int] = []
    for deck in source_decks:
        found = invoke("findCards", {"query": f'deck:"{deck}"'})
        if isinstance(found, list):
            card_ids.extend([x for x in found if isinstance(x, int)])

    card_ids = sorted(set(card_ids))
    cards_info = invoke("cardsInfo", {"cards": card_ids}) if card_ids else []

    note_ids = sorted({card["note"] for card in cards_info if isinstance(card, dict) and "note" in card})
    notes_info = invoke("notesInfo", {"notes": note_ids}) if note_ids else []
    return cards_info, notes_info


def build_move_plan(
    cards_info: list[dict],
    notes_info: list[dict],
    target_root: str,
) -> tuple[list[dict], Counter]:
    cards_by_note: dict[int, list[int]] = defaultdict(list)
    for card in cards_info:
        note_id = card.get("note")
        card_id = card.get("cardId")
        if isinstance(note_id, int) and isinstance(card_id, int):
            cards_by_note[note_id].append(card_id)

    plan: list[dict] = []
    by_target = Counter()

    for note in notes_info:
        if not isinstance(note, dict):
            continue

        note_id = note.get("noteId")
        if not isinstance(note_id, int):
            continue

        fields = note.get("fields") or {}
        topic_obj = fields.get("Topic") or {}
        topic_value = topic_obj.get("value") if isinstance(topic_obj, dict) else ""
        materia, submateria = split_topic(str(topic_value or ""))

        target_deck = f"{target_root}::{materia}::{submateria}"
        card_ids = cards_by_note.get(note_id, [])
        if not card_ids:
            continue

        plan.append(
            {
                "noteId": note_id,
                "topic": topic_value,
                "targetDeck": target_deck,
                "cardIds": card_ids,
            }
        )
        by_target[target_deck] += len(card_ids)

    return plan, by_target


def apply_plan(plan: list[dict]) -> int:
    grouped: dict[str, list[int]] = defaultdict(list)
    for row in plan:
        grouped[row["targetDeck"]].extend(row["cardIds"])

    moved = 0
    for deck_name, card_ids in grouped.items():
        invoke("createDeck", {"deck": deck_name})
        invoke("changeDeck", {"cards": sorted(set(card_ids)), "deck": deck_name})
        moved += len(set(card_ids))
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(description="Reorganiza decks de concurso por materia/submateria")
    parser.add_argument(
        "--source-deck",
        action="append",
        required=True,
        help="Deck de origem (pode repetir o argumento)",
    )
    parser.add_argument(
        "--target-root",
        default="Concursos::BNDES::Ciberseguranca::Materias",
        help="Raiz dos novos subdecks por materia/submateria",
    )
    parser.add_argument("--apply", action="store_true", help="Aplica as mudancas no Anki")
    args = parser.parse_args()

    cards_info, notes_info = collect_cards(args.source_deck)
    plan, by_target = build_move_plan(cards_info, notes_info, args.target_root)

    moved = 0
    if args.apply:
        moved = apply_plan(plan)

    output = {
        "sourceDecks": args.source_deck,
        "targetRoot": args.target_root,
        "apply": args.apply,
        "cardsFound": len(cards_info),
        "notesFound": len(notes_info),
        "cardsPlannedToMove": sum(len(row["cardIds"]) for row in plan),
        "movedCards": moved,
        "targetDecks": [{"deck": deck, "cards": count} for deck, count in sorted(by_target.items())],
        "preview": plan[:20],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
