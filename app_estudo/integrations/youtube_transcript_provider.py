"""Provider de transcript para videos YouTube usando fonte externa oficial."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any


@dataclass(frozen=True)
class YoutubeTranscriptFetchResult:
    """Transcript bruto obtido de um video YouTube."""

    video_id: str
    raw_text: str
    raw_timestamps: tuple[str, ...]
    locale: str
    provider: str
    estimated_duration_seconds: int


def fetch_transcript_from_youtube(
    *,
    video_id: str,
    preferred_languages: tuple[str, ...] = ("en",),
) -> YoutubeTranscriptFetchResult:
    """Busca transcript publico do YouTube por video_id."""

    if not video_id.strip():
        raise ValueError("video_id e obrigatorio")

    language_codes = tuple(lang.strip() for lang in preferred_languages if lang and lang.strip())
    if not language_codes:
        raise ValueError("preferred_languages deve conter ao menos um idioma")

    api = _load_transcript_api()
    items = api.get_transcript(video_id.strip(), languages=list(language_codes))

    if not items:
        raise ValueError("Transcript retornou vazio para o video informado")

    cleaned_text_parts: list[str] = []
    timestamps: list[str] = []
    max_end = 0.0

    for item in items:
        text = str(item.get("text", "")).strip()
        start = float(item.get("start", 0.0))
        duration = float(item.get("duration", 0.0))

        if text:
            cleaned_text_parts.append(text)
        timestamps.append(_format_seconds(start))

        end = start + duration
        if end > max_end:
            max_end = end

    raw_text = " ".join(cleaned_text_parts).strip()
    if not raw_text:
        raise ValueError("Transcript sem texto util apos normalizacao basica")

    return YoutubeTranscriptFetchResult(
        video_id=video_id.strip(),
        raw_text=raw_text,
        raw_timestamps=tuple(timestamps),
        locale=language_codes[0],
        provider="youtube_transcript_api",
        estimated_duration_seconds=max(1, int(ceil(max_end))),
    )


def _format_seconds(seconds_value: float) -> str:
    if seconds_value < 0:
        seconds_value = 0.0

    total_ms = int(round(seconds_value * 1000))
    hours = total_ms // 3_600_000
    remainder = total_ms % 3_600_000
    minutes = remainder // 60_000
    remainder = remainder % 60_000
    seconds = remainder // 1000
    millis = remainder % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"


def _load_transcript_api() -> Any:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Dependencia ausente: instale 'youtube-transcript-api' para coletar transcript real do YouTube"
        ) from exc

    return YouTubeTranscriptApi
