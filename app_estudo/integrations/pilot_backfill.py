"""Backfill de campos criticos para validacao do lote piloto."""

from __future__ import annotations

from typing import Any

_CLASSIFICATION_TO_SCORE = {
    "recommended": "4.0",
    "recommended_with_reservations": "3.0",
    "not_recommended": "2.0",
    "pending_review": "3.0",
}


def _field_value(fields: dict[str, Any], field_name: str) -> str:
    raw = fields.get(field_name)
    if isinstance(raw, dict):
        raw = raw.get("value")
    if raw is None:
        return ""
    return str(raw).strip()


def plan_backfill_updates(note: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    fields = note.get("fields")
    if not isinstance(fields, dict):
        return {}, set()

    updates: dict[str, str] = {}
    extra_tags: set[str] = set()

    evaluation_score = _field_value(fields, "evaluation_score")
    if not evaluation_score:
        classification = _field_value(fields, "evaluation_classification")
        updates["evaluation_score"] = _CLASSIFICATION_TO_SCORE.get(classification, "3.0")

    audio_reference = _field_value(fields, "audio_reference")
    if not audio_reference:
        source_id = _field_value(fields, "source_id")
        source_for_ref = source_id if source_id else f"note-{note.get('noteId', 'unknown')}"
        updates["audio_reference"] = f"pending://audio/{source_for_ref}"
        extra_tags.add("status:pending_audio_reference")

    return updates, extra_tags
