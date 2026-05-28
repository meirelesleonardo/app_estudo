"""Integracoes logicas e adaptadores externos do projeto."""

from .ankiconnect_healthcheck import AnkiHealthcheckResult, check_ankiconnect
from .anki_mapping import LogicalAnkiNote, map_to_anki_logical_note
from .ankiconnect_client import AnkiConnectClient, AnkiSyncResult
from .anki_reconciliation import DuplicateGroup, ReconciliationReport, build_duplicate_groups
from .item_history import ItemHistoryEvent, JsonlItemHistoryStore, new_event
from .media_sqlite_store import SqliteMediaArtifactStore
from .media_quality_gate import QualityGateResult, evaluate_e4_quality_gate
from .media_versioning import ArtifactSnapshot, VersionDecision, decide_version_action
from .youtube_audio_extraction import YoutubeAudioExtractionResult, extract_youtube_audio
from .youtube_transcript_provider import YoutubeTranscriptFetchResult, fetch_transcript_from_youtube
from .youtube_ingestion import (
	YoutubeIngestionResult,
	YoutubeTranscriptPayload,
	extract_youtube_video_id,
	ingest_first_youtube_video,
	ingest_first_youtube_video_from_source,
)
from .pilot_validation import validate_pilot_notes
from .pilot_backfill import plan_backfill_updates

__all__ = [
	"LogicalAnkiNote",
	"map_to_anki_logical_note",
	"AnkiHealthcheckResult",
	"check_ankiconnect",
	"AnkiConnectClient",
	"AnkiSyncResult",
	"DuplicateGroup",
	"ReconciliationReport",
	"build_duplicate_groups",
	"ItemHistoryEvent",
	"JsonlItemHistoryStore",
	"new_event",
	"SqliteMediaArtifactStore",
	"QualityGateResult",
	"evaluate_e4_quality_gate",
	"ArtifactSnapshot",
	"VersionDecision",
	"decide_version_action",
	"YoutubeAudioExtractionResult",
	"extract_youtube_audio",
	"YoutubeTranscriptFetchResult",
	"fetch_transcript_from_youtube",
	"YoutubeIngestionResult",
	"YoutubeTranscriptPayload",
	"extract_youtube_video_id",
	"ingest_first_youtube_video",
	"ingest_first_youtube_video_from_source",
	"validate_pilot_notes",
	"plan_backfill_updates",
]
