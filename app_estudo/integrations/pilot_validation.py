"""Validacao de lote piloto do MVP com metricas objetivas."""

from __future__ import annotations

from collections import Counter
from typing import Any

_TRACEABILITY_FIELDS = {
    "source_id",
    "source_type",
    "title",
    "transcript_excerpt",
    "target_expression",
    "explanation_ptbr",
    "listening_context",
    "level",
    "accent",
    "audio_reference",
    "created_from_stage",
    "logical_key",
    "evaluation_score",
    "evaluation_classification",
}


def _field_value(note: dict[str, Any], field_name: str) -> str:
    fields = note.get("fields")
    if not isinstance(fields, dict):
        return ""

    raw = fields.get(field_name)
    if isinstance(raw, dict):
        raw = raw.get("value")

    if raw is None:
        return ""

    value = str(raw).strip()
    return value


def _percent(value: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((value / total) * 100.0, 2)


def validate_pilot_notes(
    notes_info: list[dict[str, Any]],
    min_items: int = 20,
    traceability_threshold: float = 95.0,
    duplicate_rate_threshold: float = 2.0,
    classification_threshold: float = 100.0,
) -> dict[str, Any]:
    total_notes = len(notes_info)
    fully_traceable = 0
    pedagogically_classified = 0
    missing_field_counts: dict[str, int] = {field: 0 for field in sorted(_TRACEABILITY_FIELDS)}

    source_ids: list[str] = []

    for note in notes_info:
        source_id = _field_value(note, "source_id")
        if source_id:
            source_ids.append(source_id)

        missing_fields_in_note = []
        for field in _TRACEABILITY_FIELDS:
            if not _field_value(note, field):
                missing_fields_in_note.append(field)
                missing_field_counts[field] += 1

        has_all_traceability_fields = not missing_fields_in_note
        if has_all_traceability_fields:
            fully_traceable += 1

        has_level = bool(_field_value(note, "level"))
        has_eval_classification = bool(_field_value(note, "evaluation_classification"))
        if has_level and has_eval_classification:
            pedagogically_classified += 1

    source_counter = Counter(source_ids)
    duplicates = sum(count - 1 for count in source_counter.values() if count > 1)

    traceability_pct = _percent(fully_traceable, total_notes)
    duplicate_rate_pct = _percent(duplicates, total_notes)
    classification_pct = _percent(pedagogically_classified, total_notes)

    criteria = {
        "min_items": total_notes >= min_items,
        "traceability": traceability_pct >= traceability_threshold,
        "duplicate_rate": duplicate_rate_pct <= duplicate_rate_threshold,
        "classification": classification_pct >= classification_threshold,
    }

    failed_criteria = [name for name, ok in criteria.items() if not ok]
    approved = not failed_criteria

    return {
        "status": "approved" if approved else "needs_review",
        "criteria": criteria,
        "failed_criteria": failed_criteria,
        "metrics": {
            "total_notes": total_notes,
            "min_items_target": min_items,
            "fully_traceable_notes": fully_traceable,
            "traceability_pct": traceability_pct,
            "duplicates": duplicates,
            "duplicate_rate_pct": duplicate_rate_pct,
            "pedagogically_classified_notes": pedagogically_classified,
            "classification_pct": classification_pct,
            "thresholds": {
                "traceability_pct": traceability_threshold,
                "duplicate_rate_pct": duplicate_rate_threshold,
                "classification_pct": classification_threshold,
            },
            "missing_field_counts": {
                field: count for field, count in missing_field_counts.items() if count > 0
            },
        },
    }
