"""Entidade de dominio para item de estudo curado de listening."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

_ALLOWED_LEVELS = {"A1", "A2", "B1", "B2", "C1"}
_ALLOWED_PHENOMENA = {"connected_speech", "contractions", "reduction"}


@dataclass(frozen=True)
class CuratedStudyItem:
    """Representa um item curado com campos minimos para o MVP."""

    source_id: str
    source_type: str
    source_url: str
    title: str
    transcript_excerpt: str
    target_expression: str
    explanation_ptbr: str
    listening_context: str
    level: str
    accent: str
    phenomenon: str
    tags_context: tuple[str, ...]
    audio_reference: str
    duration_seconds: int
    created_from_stage: str

    def __post_init__(self) -> None:
        _require_non_empty("source_id", self.source_id)
        _require_non_empty("source_type", self.source_type)
        _require_non_empty("source_url", self.source_url)
        _require_non_empty("title", self.title)
        _require_non_empty("transcript_excerpt", self.transcript_excerpt)
        _require_non_empty("target_expression", self.target_expression)
        _require_non_empty("explanation_ptbr", self.explanation_ptbr)
        _require_non_empty("listening_context", self.listening_context)
        _require_non_empty("accent", self.accent)
        _require_non_empty("audio_reference", self.audio_reference)

        if self.level not in _ALLOWED_LEVELS:
            raise ValueError(
                f"level invalido: {self.level!r}. Use um valor entre {_sorted_values(_ALLOWED_LEVELS)}"
            )

        if self.phenomenon not in _ALLOWED_PHENOMENA:
            raise ValueError(
                "phenomenon invalido: "
                f"{self.phenomenon!r}. Use um valor entre {_sorted_values(_ALLOWED_PHENOMENA)}"
            )

        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds deve ser maior que zero")

        if not _is_stage_id(self.created_from_stage):
            raise ValueError(
                "created_from_stage invalido. Formato esperado: E#.S# (ex.: E5.S2)"
            )

        normalized_tags = _normalize_tags(self.tags_context)
        object.__setattr__(self, "tags_context", normalized_tags)

    @property
    def logical_key(self) -> str:
        """Chave logica deterministica para reconciliacao futura."""

        return "|".join(
            [
                self.source_id.strip().lower(),
                self.target_expression.strip().lower(),
                self.phenomenon,
                self.level,
            ]
        )

    def to_dict(self) -> dict[str, object]:
        """Serializa a entidade para um dicionario simples e estavel."""

        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "title": self.title,
            "transcript_excerpt": self.transcript_excerpt,
            "target_expression": self.target_expression,
            "explanation_ptbr": self.explanation_ptbr,
            "listening_context": self.listening_context,
            "level": self.level,
            "accent": self.accent,
            "phenomenon": self.phenomenon,
            "tags_context": list(self.tags_context),
            "audio_reference": self.audio_reference,
            "duration_seconds": self.duration_seconds,
            "created_from_stage": self.created_from_stage,
            "logical_key": self.logical_key,
        }


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")


def _is_stage_id(value: str) -> bool:
    if not value:
        return False

    value = value.strip()
    if not value.startswith("E") or ".S" not in value:
        return False

    try:
        stage_part, substage_part = value.split(".S", maxsplit=1)
        int(stage_part[1:])
        int(substage_part)
    except (ValueError, IndexError):
        return False

    return True


def _normalize_tags(tags: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        candidate = tag.strip().lower()
        if not candidate:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)

    if not normalized:
        raise ValueError("tags_context deve conter ao menos uma tag")

    return tuple(normalized)


def _sorted_values(values: set[str]) -> str:
    return ", ".join(sorted(values))
