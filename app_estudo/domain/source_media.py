"""Entidades de dominio para origem de midia e metadados de fonte."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

_ALLOWED_MEDIA_TYPES = {
    "podcast",
    "interview",
    "ted_talk",
    "series",
    "movie",
    "gameplay",
    "documentary",
    "class",
    "news",
    "vlog",
    "spontaneous_conversation",
}
_ALLOWED_SUBTITLE_TYPES = {"official", "auto", "hybrid", "none"}


@dataclass(frozen=True)
class SourceMedia:
    """Representa a origem de midia antes do processamento textual."""

    source_media_id: str
    platform: str
    external_id: str
    canonical_url: str
    media_type: str
    language: str
    duration_seconds: int
    created_at: str
    captured_at: str
    last_seen_at: str
    source_hash: str

    def __post_init__(self) -> None:
        _require_non_empty("source_media_id", self.source_media_id)
        _require_non_empty("platform", self.platform)
        _require_non_empty("external_id", self.external_id)
        _require_non_empty("canonical_url", self.canonical_url)
        _require_non_empty("media_type", self.media_type)
        _require_non_empty("language", self.language)
        _require_non_empty("created_at", self.created_at)
        _require_non_empty("captured_at", self.captured_at)
        _require_non_empty("last_seen_at", self.last_seen_at)
        _require_non_empty("source_hash", self.source_hash)

        normalized_platform = self.platform.strip().lower()
        normalized_media_type = self.media_type.strip().lower()
        normalized_language = self.language.strip().lower()

        if normalized_media_type not in _ALLOWED_MEDIA_TYPES:
            raise ValueError(
                "media_type invalido: "
                f"{self.media_type!r}. Use um valor entre {_sorted_values(_ALLOWED_MEDIA_TYPES)}"
            )

        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds deve ser maior que zero")

        _ensure_iso8601("created_at", self.created_at)
        _ensure_iso8601("captured_at", self.captured_at)
        _ensure_iso8601("last_seen_at", self.last_seen_at)

        if not self.canonical_url.startswith(("http://", "https://")):
            raise ValueError("canonical_url deve iniciar com http:// ou https://")

        object.__setattr__(self, "platform", normalized_platform)
        object.__setattr__(self, "media_type", normalized_media_type)
        object.__setattr__(self, "language", normalized_language)

    @property
    def source_key(self) -> str:
        """Chave univoca logica para identificar origem (platform + external_id)."""

        return f"{self.platform}|{self.external_id.strip().lower()}"

    def to_dict(self) -> dict[str, object]:
        """Serializa a entidade para formato estavel."""

        return {
            "source_media_id": self.source_media_id,
            "platform": self.platform,
            "external_id": self.external_id,
            "canonical_url": self.canonical_url,
            "media_type": self.media_type,
            "language": self.language,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at,
            "captured_at": self.captured_at,
            "last_seen_at": self.last_seen_at,
            "source_hash": self.source_hash,
            "source_key": self.source_key,
        }


@dataclass(frozen=True)
class SourceMetadata:
    """Representa metadados de curadoria e classificacao da origem."""

    source_metadata_id: str
    source_media_id: str
    accent_profile: str
    speech_rate_profile: str
    subtitle_type: str
    transcript_quality: float
    connected_speech_density: float
    noise_level: float
    pedagogical_category: str
    context_tags: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_empty("source_metadata_id", self.source_metadata_id)
        _require_non_empty("source_media_id", self.source_media_id)
        _require_non_empty("accent_profile", self.accent_profile)
        _require_non_empty("speech_rate_profile", self.speech_rate_profile)
        _require_non_empty("subtitle_type", self.subtitle_type)
        _require_non_empty("pedagogical_category", self.pedagogical_category)

        normalized_subtitle_type = self.subtitle_type.strip().lower()
        normalized_accent_profile = self.accent_profile.strip().lower()
        normalized_speech_rate_profile = self.speech_rate_profile.strip().lower()
        normalized_pedagogical_category = self.pedagogical_category.strip().lower()

        if normalized_subtitle_type not in _ALLOWED_SUBTITLE_TYPES:
            raise ValueError(
                "subtitle_type invalido: "
                f"{self.subtitle_type!r}. Use um valor entre {_sorted_values(_ALLOWED_SUBTITLE_TYPES)}"
            )

        _require_score_range("transcript_quality", self.transcript_quality)
        _require_score_range("connected_speech_density", self.connected_speech_density)
        _require_score_range("noise_level", self.noise_level)

        normalized_tags = _normalize_tags(self.context_tags)

        object.__setattr__(self, "subtitle_type", normalized_subtitle_type)
        object.__setattr__(self, "accent_profile", normalized_accent_profile)
        object.__setattr__(self, "speech_rate_profile", normalized_speech_rate_profile)
        object.__setattr__(self, "pedagogical_category", normalized_pedagogical_category)
        object.__setattr__(self, "context_tags", normalized_tags)

    def to_dict(self) -> dict[str, object]:
        """Serializa metadados para formato estavel."""

        return {
            "source_metadata_id": self.source_metadata_id,
            "source_media_id": self.source_media_id,
            "accent_profile": self.accent_profile,
            "speech_rate_profile": self.speech_rate_profile,
            "subtitle_type": self.subtitle_type,
            "transcript_quality": self.transcript_quality,
            "connected_speech_density": self.connected_speech_density,
            "noise_level": self.noise_level,
            "pedagogical_category": self.pedagogical_category,
            "context_tags": list(self.context_tags),
        }


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")


def _ensure_iso8601(field_name: str, value: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} deve estar em formato ISO-8601") from exc


def _require_score_range(field_name: str, value: float) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{field_name} deve estar entre 0.0 e 1.0")


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
        raise ValueError("context_tags deve conter ao menos uma tag")

    return tuple(normalized)


def _sorted_values(values: set[str]) -> str:
    return ", ".join(sorted(values))
