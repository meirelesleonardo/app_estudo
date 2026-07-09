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

# --- Constantes da trilha IA ---
IA_DECK_ROOT = "IA"
IA_MODEL = "AppEstudoIA"
IA_SUBDECKS = [
    "IA::01 - Fundamentos",
    "IA::02 - LLMs",
    "IA::03 - Prompt Engineering",
    "IA::04 - Context Engineering",
    "IA::05 - Skills",
    "IA::06 - MCP",
    "IA::07 - RAG",
    "IA::08 - Agentes",
    "IA::09 - Multiagentes",
    "IA::10 - DevOps IA",
    "IA::11 - Arquiteturas",
    "IA::12 - Casos Reais",
]


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


# --- Funcoes da trilha IA ---

def ensure_ia_model(endpoint: str) -> None:
    """Cria o modelo AppEstudoIA (Frente/Verso + CardID interno) de forma idempotente."""
    names = invoke(endpoint, "modelNames", {})
    if isinstance(names, list) and IA_MODEL in names:
        return

    invoke(
        endpoint,
        "createModel",
        {
            "modelName": IA_MODEL,
            "inOrderFields": ["CardID", "Front", "Back"],
            "css": ".card { font-family: Arial; font-size: 18px; text-align: left; color: black; background-color: white; }",
            "isCloze": False,
            "cardTemplates": [
                {
                    "Name": "Card 1",
                    "Front": "{{Front}}",
                    "Back": "{{FrontSide}}<hr id=answer>{{Back}}",
                }
            ],
        },
    )


def ensure_ia_deck_hierarchy(endpoint: str) -> None:
    """Cria todos os subdecks da trilha IA de forma idempotente."""
    for deck_name in IA_SUBDECKS:
        ensure_deck(endpoint, deck_name)


def find_by_card_id(endpoint: str, deck_name: str, card_id: str) -> list[int]:
    """Busca notas existentes por card_id no deck destino."""
    query = f'deck:"{deck_name}" "CardID:{card_id}"'
    result = invoke(endpoint, "findNotes", {"query": query})
    if not isinstance(result, list):
        return []
    return [item for item in result if isinstance(item, int)]


def _row_has_extra_columns(row: dict[str | None, str]) -> bool:
    extra_columns = row.get(None)
    if not extra_columns:
        return False
    if isinstance(extra_columns, list):
        return any(str(value).strip() for value in extra_columns)
    return bool(str(extra_columns).strip())


def import_ia_cards(
    endpoint: str,
    csv_path: Path,
    allow_duplicate: bool,
) -> dict[str, object]:
    """Importa cards da trilha IA para o Anki.

    O CSV deve ter colunas: card_id, front, back, deck, tags.
    A coluna deck pode omitida; o padrao e IA::01 - Fundamentos.
    """
    ensure_ia_model(endpoint)
    ensure_ia_deck_hierarchy(endpoint)

    created = 0
    skipped = 0
    errors: list[dict[str, str]] = []
    created_by_deck: Counter[str] = Counter()
    skipped_by_deck: Counter[str] = Counter()

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            card_id = (row.get("card_id") or "").strip()

            if _row_has_extra_columns(row):
                errors.append(
                    {
                        "card_id": card_id or "<sem-card-id>",
                        "error": "Linha CSV malformada: campos com virgula devem estar entre aspas.",
                    }
                )
                continue

            if not card_id:
                skipped += 1
                continue

            deck = (row.get("deck") or IA_SUBDECKS[0]).strip()
            if not allow_duplicate:
                existing = find_by_card_id(endpoint, deck, card_id)
                if existing:
                    skipped += 1
                    skipped_by_deck[deck] += 1
                    continue

            tags = [tag for tag in (row.get("tags") or "").split() if tag]
            note = {
                "deckName": deck,
                "modelName": IA_MODEL,
                "fields": {
                    "CardID": card_id,
                    "Front": row.get("front") or "",
                    "Back": row.get("back") or "",
                },
                "tags": tags,
                "options": {"allowDuplicate": allow_duplicate},
            }

            try:
                result = invoke(endpoint, "addNote", {"note": note})
                if isinstance(result, int):
                    created += 1
                    created_by_deck[deck] += 1
                else:
                    errors.append({"card_id": card_id, "error": "Retorno invalido do addNote"})
            except RuntimeError as exc:
                errors.append({"card_id": card_id, "error": str(exc)})

    return {
        "mode": "ia",
        "csv_path": str(csv_path),
        "model_name": IA_MODEL,
        "created": created,
        "skipped": skipped,
        "created_by_deck": dict(sorted(created_by_deck.items())),
        "skipped_by_deck": dict(sorted(skipped_by_deck.items())),
        "errors": errors,
    }


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
    parser = argparse.ArgumentParser(
        description="Importa cards de concurso ou IA para o Anki via AnkiConnect"
    )
    parser.add_argument(
        "--mode",
        choices=["concurso", "ia"],
        default="concurso",
        help="Modo de importacao: concurso (default) ou ia",
    )
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
        help="Permite duplicidade de identificador do card.",
    )
    parser.add_argument(
        "--report",
        default="data/sources/concursos/processed/bndes_2024_prova2_anki_import_report.json",
    )
    args = parser.parse_args()

    if args.mode == "ia":
        report = import_ia_cards(
            endpoint=args.endpoint,
            csv_path=Path(args.csv),
            allow_duplicate=args.allow_duplicate,
        )
    else:
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
