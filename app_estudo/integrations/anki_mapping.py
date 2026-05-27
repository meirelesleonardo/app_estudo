"""Mapeamento logico de item de estudo para nota Anki."""

from __future__ import annotations

from dataclasses import dataclass

from app_estudo.domain.listening_evaluation import ListeningEvaluation
from app_estudo.domain.study_item import CuratedStudyItem


@dataclass(frozen=True)
class LogicalAnkiNote:
    """Representa payload logico de nota para futura sincronizacao."""

    deck_name: str
    fields: dict[str, object]
    tags: tuple[str, ...]
    media: dict[str, object]
    note_unique_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "deck_name": self.deck_name,
            "fields": dict(self.fields),
            "tags": list(self.tags),
            "media": dict(self.media),
            "note_unique_id": self.note_unique_id,
        }


def map_to_anki_logical_note(
    item: CuratedStudyItem, evaluation: ListeningEvaluation
) -> LogicalAnkiNote:
    """Converte item + avaliacao em nota logica conforme E4.S1."""

    deck_name = f"Ingles::Listening::{item.level}"
    tags = _compose_tags(item, evaluation)

    fields = {
        "source_id": item.source_id,
        "source_type": item.source_type,
        "title": item.title,
        "transcript_excerpt": item.transcript_excerpt,
        "target_expression": item.target_expression,
        "explanation_ptbr": item.explanation_ptbr,
        "listening_context": item.listening_context,
        "level": item.level,
        "accent": item.accent,
        "tags_context": list(item.tags_context),
        "audio_reference": item.audio_reference,
        "created_from_stage": item.created_from_stage,
        "logical_key": item.logical_key,
        "evaluation_score": evaluation.score_final,
        "evaluation_classification": evaluation.classification,
    }

    media = {
        "media_id": f"media::{item.source_id}",
        "source_id": item.source_id,
        "media_type": "audio",
        "reference_path_or_url": item.audio_reference,
        "duration": item.duration_seconds,
    }

    return LogicalAnkiNote(
        deck_name=deck_name,
        fields=fields,
        tags=tags,
        media=media,
        note_unique_id=item.logical_key,
    )


def _compose_tags(item: CuratedStudyItem, evaluation: ListeningEvaluation) -> tuple[str, ...]:
    raw_tags = [
        *item.tags_context,
        f"origem:{item.source_type.strip().lower()}",
        f"sotaque:{item.accent.strip().lower()}",
        f"fenomeno:{item.phenomenon}",
        "status:curated",
        f"avaliacao:{evaluation.classification}",
    ]

    unique_tags: list[str] = []
    seen: set[str] = set()
    for tag in raw_tags:
        candidate = tag.strip().lower()
        if not candidate:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        unique_tags.append(candidate)

    return tuple(unique_tags)
