"""Orquestracao de ingestao YouTube e sincronizacao de cards no Anki."""

from __future__ import annotations

from dataclasses import dataclass
import re

from app_estudo.domain import CuratedStudyItem, evaluate_listening_item
from app_estudo.integrations.anki_mapping import map_to_anki_logical_note
from app_estudo.integrations.ankiconnect_client import AnkiConnectClient
from app_estudo.integrations.media_sqlite_store import SqliteMediaArtifactStore
from app_estudo.integrations.youtube_audio_extraction import extract_youtube_audio
from app_estudo.integrations.youtube_ingestion import (
    YoutubeTranscriptPayload,
    ingest_first_youtube_video,
    ingest_first_youtube_video_from_source,
)


@dataclass(frozen=True)
class YoutubeAnkiSyncSummary:
    """Resumo da sincronizacao de um video YouTube para notas Anki."""

    source_media_id: str
    curated_transcript_id: str
    quality_gate_status: str
    total_segments: int
    attempted_notes: int
    synced_notes: int
    updated_notes: int
    pending_notes: int
    conflict_notes: int
    blocked_notes: int


def ingest_youtube_video_and_sync_anki(
    *,
    youtube_url: str,
    title: str,
    store: SqliteMediaArtifactStore,
    anki_client: AnkiConnectClient,
    preferred_languages: tuple[str, ...] = ("en",),
    level: str = "B1",
    accent: str = "mixed",
    phenomenon: str = "connected_speech",
    created_from_stage: str = "E2.S4",
    tags_context: tuple[str, ...] = ("modulo:ingles", "habilidade:listening", "origem:youtube"),
    transcript_quality: float = 0.9,
    connected_speech_density: float = 0.6,
    noise_level: float = 0.2,
    extract_audio_enabled: bool = False,
    audio_output_dir: str = "data/media/audio",
    transcript_payload: YoutubeTranscriptPayload | None = None,
) -> YoutubeAnkiSyncSummary:
    """Executa ingestao de um video e sincroniza segmentos como notas no Anki."""

    if transcript_payload is None:
        ingestion = ingest_first_youtube_video_from_source(
            youtube_url=youtube_url,
            title=title,
            store=store,
            preferred_languages=preferred_languages,
            transcript_quality=transcript_quality,
            connected_speech_density=connected_speech_density,
            noise_level=noise_level,
            accent_profile=accent,
        )
    else:
        ingestion = ingest_first_youtube_video(
            youtube_url=youtube_url,
            transcript_payload=transcript_payload,
            store=store,
            transcript_quality=transcript_quality,
            connected_speech_density=connected_speech_density,
            noise_level=noise_level,
            accent_profile=accent,
        )

    segment_payloads = store.list_study_segment_payloads(ingestion.curated_transcript_id)

    audio_reference = youtube_url
    if extract_audio_enabled:
        audio_result = extract_youtube_audio(youtube_url=youtube_url, output_dir=audio_output_dir)
        audio_reference = audio_result.audio_file_path

    synced = 0
    updated = 0
    pending = 0
    conflict = 0
    blocked = 0

    for segment_payload in segment_payloads:
        item = _build_study_item_from_segment(
            segment_payload=segment_payload,
            source_url=youtube_url,
            title=title,
            level=level,
            accent=accent,
            phenomenon=phenomenon,
            created_from_stage=created_from_stage,
            tags_context=tags_context,
            audio_reference=audio_reference,
        )

        evaluation = evaluate_listening_item(
            item,
            _build_default_criteria_scores(
                transcript_quality=transcript_quality,
                connected_speech_density=connected_speech_density,
                noise_level=noise_level,
            ),
        )

        note = map_to_anki_logical_note(item, evaluation)
        result = anki_client.sync_logical_note(note)
        if result.state == "synced":
            synced += 1
        elif result.state == "updated":
            updated += 1
        elif result.state == "pending":
            pending += 1
        elif result.state == "conflict":
            conflict += 1
        elif result.state == "blocked":
            blocked += 1

    return YoutubeAnkiSyncSummary(
        source_media_id=ingestion.source_media_id,
        curated_transcript_id=ingestion.curated_transcript_id,
        quality_gate_status=ingestion.quality_gate_status,
        total_segments=len(segment_payloads),
        attempted_notes=len(segment_payloads),
        synced_notes=synced,
        updated_notes=updated,
        pending_notes=pending,
        conflict_notes=conflict,
        blocked_notes=blocked,
    )


def _build_study_item_from_segment(
    *,
    segment_payload: dict[str, object],
    source_url: str,
    title: str,
    level: str,
    accent: str,
    phenomenon: str,
    created_from_stage: str,
    tags_context: tuple[str, ...],
    audio_reference: str,
) -> CuratedStudyItem:
    source_media_id = str(segment_payload["source_media_id"])
    segment_index = int(segment_payload["segment_index"])
    segment_start_ms = int(segment_payload["segment_start_ms"])
    segment_end_ms = int(segment_payload["segment_end_ms"])
    segment_text = str(segment_payload["segment_text"]).strip()

    duration_seconds = max(1, int(round((segment_end_ms - segment_start_ms) / 1000)))

    source_id = f"{source_media_id}:{segment_start_ms}-{segment_end_ms}"

    return CuratedStudyItem(
        source_id=source_id,
        source_type="youtube",
        source_url=source_url,
        title=f"{title} [seg {segment_index:03d}]",
        transcript_excerpt=segment_text,
        target_expression=_extract_target_expression(segment_text),
        explanation_ptbr="Trecho curado automaticamente do video YouTube para treino de listening.",
        listening_context="Listening guiado por segmento de video com foco em compreensao oral.",
        level=level,
        accent=accent,
        phenomenon=phenomenon,
        tags_context=tags_context,
        audio_reference=audio_reference,
        duration_seconds=duration_seconds,
        created_from_stage=created_from_stage,
    )


def _extract_target_expression(text: str) -> str:
    tokens = re.findall(r"[A-Za-z']+", text)
    if not tokens:
        return "listening-focus"
    return " ".join(tokens[: min(3, len(tokens))]).lower()


def _build_default_criteria_scores(
    *,
    transcript_quality: float,
    connected_speech_density: float,
    noise_level: float,
) -> dict[str, float]:
    audio_clarity = _clamp_score((1.0 - noise_level) * 5)
    speech_speed = 3.5
    connected_speech_presence = _clamp_score(connected_speech_density * 5)
    subtitle_transcript_quality = _clamp_score(transcript_quality * 5)
    context_naturalness = 4.0
    pedagogical_reusability = 4.0

    return {
        "audio_clarity": audio_clarity,
        "speech_speed": speech_speed,
        "connected_speech_presence": connected_speech_presence,
        "subtitle_transcript_quality": subtitle_transcript_quality,
        "context_naturalness": context_naturalness,
        "pedagogical_reusability": pedagogical_reusability,
    }


def _clamp_score(value: float) -> float:
    if value < 0:
        return 0.0
    if value > 5:
        return 5.0
    return round(value, 2)
