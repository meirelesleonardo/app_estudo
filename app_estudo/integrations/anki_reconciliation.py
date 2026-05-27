"""Politica de deduplicacao e reconciliacao de notas no Anki."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DuplicateGroup:
    """Representa um conjunto de notas com mesmo source_id."""

    source_id: str
    note_ids: tuple[int, ...]
    canonical_note_id: int
    duplicate_note_ids: tuple[int, ...]


@dataclass(frozen=True)
class ReconciliationReport:
    """Resumo de reconciliacao de duplicatas."""

    deck_name: str
    strategy: str
    dry_run: bool
    groups_found: int
    groups_processed: int
    notes_marked_for_delete: int


def build_duplicate_groups(
    notes_info: list[dict],
    strategy: str = "keep_oldest",
) -> list[DuplicateGroup]:
    """Agrupa notas por source_id e retorna apenas grupos duplicados."""

    groups: dict[str, list[int]] = {}

    for note in notes_info:
        note_id = note.get("noteId")
        if not isinstance(note_id, int):
            continue

        source_id = _get_source_id(note)
        if not source_id:
            continue

        groups.setdefault(source_id, []).append(note_id)

    duplicate_groups: list[DuplicateGroup] = []
    for source_id, note_ids in groups.items():
        if len(note_ids) <= 1:
            continue

        canonical_note_id = _choose_canonical_note_id(note_ids, strategy)
        duplicate_note_ids = tuple(sorted(nid for nid in note_ids if nid != canonical_note_id))

        duplicate_groups.append(
            DuplicateGroup(
                source_id=source_id,
                note_ids=tuple(sorted(note_ids)),
                canonical_note_id=canonical_note_id,
                duplicate_note_ids=duplicate_note_ids,
            )
        )

    return sorted(duplicate_groups, key=lambda g: (g.source_id, g.canonical_note_id))


def _get_source_id(note: dict) -> str:
    fields = note.get("fields", {})
    source_id_field = fields.get("source_id")

    if not isinstance(source_id_field, dict):
        return ""

    value = str(source_id_field.get("value", "")).strip()
    return value


def _choose_canonical_note_id(note_ids: list[int], strategy: str) -> int:
    if strategy == "keep_oldest":
        return min(note_ids)
    if strategy == "keep_newest":
        return max(note_ids)

    raise ValueError(
        f"Estrategia invalida: {strategy!r}. Use 'keep_oldest' ou 'keep_newest'"
    )
