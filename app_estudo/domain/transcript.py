"""Entidades de dominio para transcricoes brutas e curadas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

_ALLOWED_CURATION_STATUSES = {"draft", "review_required", "approved", "rejected"}


@dataclass(frozen=True)
class RawTranscript:
    """Representa uma transcricao bruta ligada a uma origem de midia."""

    raw_transcript_id: str
    source_media_id: str
    provider: str
    raw_text: str
    raw_timestamps: tuple[str, ...]
    locale: str
    ingestion_version: str
    content_hash: str
    captured_at: str

    def __post_init__(self) -> None:
        _require_non_empty("raw_transcript_id", self.raw_transcript_id)
        _require_non_empty("source_media_id", self.source_media_id)
        _require_non_empty("provider", self.provider)
        _require_non_empty("raw_text", self.raw_text)
        _require_non_empty("locale", self.locale)
        _require_non_empty("ingestion_version", self.ingestion_version)
        _require_non_empty("content_hash", self.content_hash)
        _require_non_empty("captured_at", self.captured_at)

        normalized_locale = self.locale.strip().lower()
        normalized_provider = self.provider.strip().lower()

        _ensure_iso8601("captured_at", self.captured_at)
        _ensure_version_like("ingestion_version", self.ingestion_version)

        normalized_timestamps = _normalize_timestamps(self.raw_timestamps)

        object.__setattr__(self, "locale", normalized_locale)
        object.__setattr__(self, "provider", normalized_provider)
        object.__setattr__(self, "raw_timestamps", normalized_timestamps)

    @property
    def lineage_key(self) -> str:
        """Chave minima de lineage para raw transcript."""

        return f"{self.source_media_id.strip().lower()}|{self.raw_transcript_id.strip().lower()}"

    def to_dict(self) -> dict[str, object]:
        """Serializa entidade para formato estavel."""

        return {
            "raw_transcript_id": self.raw_transcript_id,
            "source_media_id": self.source_media_id,
            "provider": self.provider,
            "raw_text": self.raw_text,
            "raw_timestamps": list(self.raw_timestamps),
            "locale": self.locale,
            "ingestion_version": self.ingestion_version,
            "content_hash": self.content_hash,
            "captured_at": self.captured_at,
            "lineage_key": self.lineage_key,
        }


@dataclass(frozen=True)
class CuratedTranscript:
    """Representa uma transcricao curada vinculada ao artefato bruto."""

    curated_transcript_id: str
    source_media_id: str
    raw_transcript_id: str
    curated_text: str
    curation_status: str
    curation_notes: str
    quality_score: float
    curated_version: str
    approved_at: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty("curated_transcript_id", self.curated_transcript_id)
        _require_non_empty("source_media_id", self.source_media_id)
        _require_non_empty("raw_transcript_id", self.raw_transcript_id)
        _require_non_empty("curated_text", self.curated_text)
        _require_non_empty("curation_status", self.curation_status)
        _require_non_empty("curation_notes", self.curation_notes)
        _require_non_empty("curated_version", self.curated_version)

        normalized_status = self.curation_status.strip().lower()
        if normalized_status not in _ALLOWED_CURATION_STATUSES:
            raise ValueError(
                "curation_status invalido: "
                f"{self.curation_status!r}. Use um valor entre {_sorted_values(_ALLOWED_CURATION_STATUSES)}"
            )

        _require_score_range("quality_score", self.quality_score, 0.0, 5.0)
        _ensure_version_like("curated_version", self.curated_version)

        if normalized_status == "approved":
            if not self.approved_at:
                raise ValueError("approved_at e obrigatorio quando curation_status = approved")
            _ensure_iso8601("approved_at", self.approved_at)

        if self.approved_at and normalized_status != "approved":
            raise ValueError("approved_at so pode ser preenchido quando curation_status = approved")

        object.__setattr__(self, "curation_status", normalized_status)

    @property
    def lineage_key(self) -> str:
        """Chave minima de lineage para transicao source -> raw -> curated."""

        return "|".join(
            [
                self.source_media_id.strip().lower(),
                self.raw_transcript_id.strip().lower(),
                self.curated_transcript_id.strip().lower(),
            ]
        )

    def to_dict(self) -> dict[str, object]:
        """Serializa entidade para formato estavel."""

        return {
            "curated_transcript_id": self.curated_transcript_id,
            "source_media_id": self.source_media_id,
            "raw_transcript_id": self.raw_transcript_id,
            "curated_text": self.curated_text,
            "curation_status": self.curation_status,
            "curation_notes": self.curation_notes,
            "quality_score": self.quality_score,
            "curated_version": self.curated_version,
            "approved_at": self.approved_at,
            "lineage_key": self.lineage_key,
        }


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")


def _ensure_iso8601(field_name: str, value: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} deve estar em formato ISO-8601") from exc


def _ensure_version_like(field_name: str, value: str) -> None:
    candidate = value.strip().lower()
    if not candidate.startswith("v") or len(candidate) < 2:
        raise ValueError(f"{field_name} deve seguir padrao de versao, ex.: v1")


def _require_score_range(field_name: str, value: float, min_value: float, max_value: float) -> None:
    if value < min_value or value > max_value:
        raise ValueError(f"{field_name} deve estar entre {min_value} e {max_value}")


def _normalize_timestamps(raw_timestamps: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    seen: set[str] = set()

    for timestamp in raw_timestamps:
        candidate = timestamp.strip()
        if not candidate:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)

    if not normalized:
        raise ValueError("raw_timestamps deve conter ao menos um marcador")

    return tuple(normalized)


def _sorted_values(values: set[str]) -> str:
    return ", ".join(sorted(values))
