#!/usr/bin/env python3
"""Importa cards de concurso em CSV para o Anki via AnkiConnect."""

from __future__ import annotations

import argparse
import csv
import json
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

DEFAULT_ENDPOINT = "http://127.0.0.1:8765"
DEFAULT_DECK = "Concursos::BNDES::Ciberseguranca::Prova2"
DEFAULT_MODEL = "AppEstudoConcurso"


def invoke(endpoint: str, action: str, params: dict | None = None) -> object:
    payload = {"action": action, "version": 6, "params": params or {}}
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Falha de conectividade com AnkiConnect: {exc}") from exc

    data = json.loads(raw)
    if data.get("error"):
        raise RuntimeError(f"Erro AnkiConnect em {action}: {data['error']}")
    return data.get("result")


def ensure_deck(endpoint: str, deck_name: str) -> None:
    invoke(endpoint, "createDeck", {"deck": deck_name})


def ensure_model(endpoint: str, model_name: str) -> None:
    names = invoke(endpoint, "modelNames", {})
    if isinstance(names, list) and model_name in names:
        return

    invoke(
        endpoint,
        "createModel",
        {
            "modelName": model_name,
            "inOrderFields": ["QuestionID", "Front", "Back", "Topic", "Source"],
            "css": ".card { font-family: Arial; font-size: 18px; text-align: left; color: black; background-color: white; }",
            "isCloze": False,
            "cardTemplates": [
                {
                    "Name": "Card 1",
                    "Front": "{{Front}}",
                    "Back": "{{FrontSide}}<hr id=answer><div><b>Resposta e explicacao</b></div>{{Back}}<hr><div><b>Tema:</b> {{Topic}}</div><div><b>ID:</b> {{QuestionID}}</div><div><b>Fonte:</b> {{Source}}</div>",
                }
            ],
        },
    )


def normalize_token(value: str) -> str:
    compact = " ".join((value or "").split())
    ascii_text = unicodedata.normalize("NFKD", compact).encode("ascii", "ignore").decode("ascii")

    chars: list[str] = []
    for ch in ascii_text:
        if ch.isalnum():
            chars.append(ch)
        else:
            chars.append("_")

    normalized = "".join(chars)
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


def resolve_target_deck(default_deck: str, deck_by_topic_root: str | None, topic: str) -> str:
    if not deck_by_topic_root:
        return default_deck

    materia, submateria = split_topic(topic)
    return f"{deck_by_topic_root}::{materia}::{submateria}"


def find_by_question_id(endpoint: str, deck_name: str, question_id: str) -> list[int]:
    query = f'deck:"{deck_name}" "QuestionID:{question_id}"'
    result = invoke(endpoint, "findNotes", {"query": query})
    if not isinstance(result, list):
        return []
    return [item for item in result if isinstance(item, int)]


def import_cards(
    endpoint: str,
    csv_path: Path,
    deck_name: str,
    model_name: str,
    source_label: str,
    allow_duplicate: bool,
    deck_by_topic_root: str | None,
) -> dict[str, object]:
    ensure_model(endpoint, model_name)

    created = 0
    skipped = 0
    errors: list[dict[str, str]] = []
    ensured_decks: set[str] = set()
    created_by_deck: Counter[str] = Counter()
    skipped_by_deck: Counter[str] = Counter()

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            question_id = (row.get("question_id") or "").strip()
            if not question_id:
                skipped += 1
                continue

            topic = row.get("topic") or ""
            target_deck = resolve_target_deck(deck_name, deck_by_topic_root, topic)
            if target_deck not in ensured_decks:
                ensure_deck(endpoint, target_deck)
                ensured_decks.add(target_deck)

            if not allow_duplicate:
                existing = find_by_question_id(endpoint, target_deck, question_id)
                if existing:
                    skipped += 1
                    skipped_by_deck[target_deck] += 1
                    continue

            tags = [tag for tag in (row.get("tags") or "").split() if tag]
            note = {
                "deckName": target_deck,
                "modelName": model_name,
                "fields": {
                    "QuestionID": question_id,
                    "Front": row.get("front") or "",
                    "Back": row.get("back") or "",
                    "Topic": topic,
                    "Source": source_label,
                },
                "tags": tags,
                "options": {"allowDuplicate": allow_duplicate},
            }

            try:
                result = invoke(endpoint, "addNote", {"note": note})
                if isinstance(result, int):
                    created += 1
                    created_by_deck[target_deck] += 1
                else:
                    errors.append({"question_id": question_id, "error": "Retorno invalido do addNote"})
            except RuntimeError as exc:
                errors.append({"question_id": question_id, "error": str(exc)})

    return {
        "csv_path": str(csv_path),
        "deck_name": deck_name,
        "deck_by_topic_root": deck_by_topic_root,
        "model_name": model_name,
        "created": created,
        "skipped": skipped,
        "created_by_deck": dict(sorted(created_by_deck.items())),
        "skipped_by_deck": dict(sorted(skipped_by_deck.items())),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa cards de concurso para o Anki")
    parser.add_argument(
        "--csv",
        default="data/sources/concursos/processed/bndes_2024_prova2_cards_final_reviewed.csv",
    )
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--deck", default=DEFAULT_DECK)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--source", default="BNDES 2024 Prova 2")
    parser.add_argument(
        "--deck-by-topic-root",
        default=None,
        help="Raiz de subdecks por materia/submateria. Ex.: Concursos::BNDES::Ciberseguranca::Materias",
    )
    parser.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="Permite duplicidade de QuestionID para criar decks paralelos de treino.",
    )
    parser.add_argument(
        "--report",
        default="data/sources/concursos/processed/bndes_2024_prova2_anki_import_report.json",
    )
    args = parser.parse_args()

    report = import_cards(
        endpoint=args.endpoint,
        csv_path=Path(args.csv),
        deck_name=args.deck,
        model_name=args.model,
        source_label=args.source,
        allow_duplicate=args.allow_duplicate,
        deck_by_topic_root=args.deck_by_topic_root,
    )

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False))
    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
