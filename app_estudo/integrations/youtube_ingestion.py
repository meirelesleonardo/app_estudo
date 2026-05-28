"""Adaptador inicial de ingestao YouTube para pipeline E2.S4."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from urllib.parse import parse_qs, urlparse

from app_estudo.domain.segmentation import segment_curated_transcript
from app_estudo.domain.source_media import SourceMedia, SourceMetadata
from app_estudo.domain.transcript import CuratedTranscript, RawTranscript
from app_estudo.domain.transcript_normalization import normalize_transcript_text
from app_estudo.integrations.media_quality_gate import evaluate_e4_quality_gate
from app_estudo.integrations.media_sqlite_store import SqliteMediaArtifactStore
from app_estudo.integrations.youtube_transcript_provider import fetch_transcript_from_youtube


@dataclass(frozen=True)
class YoutubeTranscriptPayload:
    """Carga de transcript para ingestao inicial de um video YouTube."""

    title: str
    duration_seconds: int
    raw_text: str
    raw_timestamps: tuple[str, ...]
    locale: str
    provider: str


@dataclass(frozen=True)
class YoutubeIngestionResult:
    """Resumo da ingestao inicial de um video YouTube."""

    source_media_id: str
    raw_transcript_id: str
    curated_transcript_id: str
    study_segments_created: int
    quality_gate_status: str


def ingest_first_youtube_video_from_source(
    *,
    youtube_url: str,
    store: SqliteMediaArtifactStore,
    title: str,
    preferred_languages: tuple[str, ...] = ("en",),
    transcript_quality: float = 0.9,
    connected_speech_density: float = 0.6,
    noise_level: float = 0.2,
    subtitle_type: str = "official",
    pedagogical_category: str = "listening_authentic",
    accent_profile: str = "mixed",
    speech_rate_profile: str = "medium_fast",
    context_tags: tuple[str, ...] = ("modulo:ingles", "origem:youtube"),
    media_type: str = "interview",
    min_segment_seconds: int = 10,
    max_segment_seconds: int = 45,
    target_segment_seconds: int = 25,
) -> YoutubeIngestionResult:
    """Ingestao usando transcript real obtido do YouTube por provider externo."""

    video_id = extract_youtube_video_id(youtube_url)
    fetched = fetch_transcript_from_youtube(video_id=video_id, preferred_languages=preferred_languages)

    payload = YoutubeTranscriptPayload(
        title=title,
        duration_seconds=fetched.estimated_duration_seconds,
        raw_text=fetched.raw_text,
        raw_timestamps=fetched.raw_timestamps,
        locale=fetched.locale,
        provider=fetched.provider,
    )

    return ingest_first_youtube_video(
        youtube_url=youtube_url,
        transcript_payload=payload,
        store=store,
        subtitle_type=subtitle_type,
        transcript_quality=transcript_quality,
        connected_speech_density=connected_speech_density,
        noise_level=noise_level,
        pedagogical_category=pedagogical_category,
        accent_profile=accent_profile,
        speech_rate_profile=speech_rate_profile,
        context_tags=context_tags,
        media_type=media_type,
        min_segment_seconds=min_segment_seconds,
        max_segment_seconds=max_segment_seconds,
        target_segment_seconds=target_segment_seconds,
    )


def ingest_first_youtube_video(
    *,
    youtube_url: str,
    transcript_payload: YoutubeTranscriptPayload,
    store: SqliteMediaArtifactStore,
    subtitle_type: str = "official",
    transcript_quality: float = 0.9,
    connected_speech_density: float = 0.6,
    noise_level: float = 0.2,
    pedagogical_category: str = "listening_authentic",
    accent_profile: str = "mixed",
    speech_rate_profile: str = "medium_fast",
    context_tags: tuple[str, ...] = ("modulo:ingles", "origem:youtube"),
    media_type: str = "interview",
    min_segment_seconds: int = 10,
    max_segment_seconds: int = 45,
    target_segment_seconds: int = 25,
) -> YoutubeIngestionResult:
    """Ingestao ponta a ponta de um unico video para o baseline operacional."""

    video_id = extract_youtube_video_id(youtube_url)
    now_iso = datetime.now(timezone.utc).isoformat()

    source_media_id = f"src-yt-{video_id}"
    raw_transcript_id = f"raw-yt-{video_id}"
    curated_transcript_id = f"cur-yt-{video_id}"

    source_hash = _sha256(
        "|".join(
            [
                youtube_url,
                video_id,
                transcript_payload.title,
                str(transcript_payload.duration_seconds),
            ]
        )
    )

    source_media = SourceMedia(
        source_media_id=source_media_id,
        platform="youtube",
        external_id=video_id,
        canonical_url=youtube_url,
        media_type=media_type,
        language=transcript_payload.locale,
        duration_seconds=transcript_payload.duration_seconds,
        created_at=now_iso,
        captured_at=now_iso,
        last_seen_at=now_iso,
        source_hash=source_hash,
    )

    source_metadata = SourceMetadata(
        source_metadata_id=f"meta-yt-{video_id}",
        source_media_id=source_media_id,
        accent_profile=accent_profile,
        speech_rate_profile=speech_rate_profile,
        subtitle_type=subtitle_type,
        transcript_quality=transcript_quality,
        connected_speech_density=connected_speech_density,
        noise_level=noise_level,
        pedagogical_category=pedagogical_category,
        context_tags=context_tags,
    )

    raw_transcript = RawTranscript(
        raw_transcript_id=raw_transcript_id,
        source_media_id=source_media_id,
        provider=transcript_payload.provider,
        raw_text=transcript_payload.raw_text,
        raw_timestamps=transcript_payload.raw_timestamps,
        locale=transcript_payload.locale,
        ingestion_version="v1",
        content_hash=_sha256(transcript_payload.raw_text),
        captured_at=now_iso,
    )

    normalized = normalize_transcript_text(raw_transcript.raw_text, normalization_version="v1")

    curated_status = "approved" if transcript_quality >= 0.7 and noise_level <= 0.4 else "review_required"
    approved_at = now_iso if curated_status == "approved" else None

    curated_transcript = CuratedTranscript(
        curated_transcript_id=curated_transcript_id,
        source_media_id=source_media_id,
        raw_transcript_id=raw_transcript_id,
        curated_text=normalized.normalized_text,
        curation_status=curated_status,
        curation_notes="normalizacao inicial automatica da ingestao youtube",
        quality_score=round(transcript_quality * 5, 2),
        curated_version="v1",
        approved_at=approved_at,
    )

    segments = (
        segment_curated_transcript(
            curated_transcript_id=curated_transcript_id,
            source_media_id=source_media_id,
            curated_text=curated_transcript.curated_text,
            total_duration_seconds=source_media.duration_seconds,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
            min_segment_seconds=min_segment_seconds,
            max_segment_seconds=max_segment_seconds,
            target_segment_seconds=target_segment_seconds,
        )
        if curated_status == "approved"
        else []
    )

    gate_result = evaluate_e4_quality_gate(
        source_metadata=source_metadata,
        curated_transcript=curated_transcript,
        segments=segments,
    )

    store.upsert_source_media(source_media)
    store.upsert_source_metadata(source_metadata)
    store.upsert_raw_transcript(raw_transcript)
    store.upsert_curated_transcript(curated_transcript)
    store.upsert_study_segments(segments)

    return YoutubeIngestionResult(
        source_media_id=source_media_id,
        raw_transcript_id=raw_transcript_id,
        curated_transcript_id=curated_transcript_id,
        study_segments_created=len(segments),
        quality_gate_status=gate_result.status,
    )


def extract_youtube_video_id(youtube_url: str) -> str:
    """Extrai video_id de URLs padrao do YouTube."""

    parsed = urlparse(youtube_url.strip())
    host = parsed.netloc.lower()

    if "youtu.be" in host:
        candidate = parsed.path.strip("/")
        if candidate:
            return candidate

    if "youtube.com" in host:
        query = parse_qs(parsed.query)
        values = query.get("v", [])
        if values and values[0].strip():
            return values[0].strip()

    raise ValueError("Nao foi possivel extrair video_id da URL informada")


def _sha256(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
