import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app_estudo.domain import CuratedTranscript, RawTranscript, SourceMedia, SourceMetadata, segment_curated_transcript
from app_estudo.integrations.ankiconnect_client import AnkiSyncResult
from app_estudo.integrations.media_sqlite_store import SqliteMediaArtifactStore
from app_estudo.integrations.youtube_ingestion import YoutubeIngestionResult
from app_estudo.integrations.youtube_anki_sync import ingest_youtube_video_and_sync_anki


class _FakeAnkiClient:
    def __init__(self) -> None:
        self.notes = []

    def sync_logical_note(self, note):
        self.notes.append(note)
        return AnkiSyncResult(
            state="synced",
            action="created",
            note_id=100 + len(self.notes),
            error_type=None,
            error_message=None,
        )


class YouTubeAnkiSyncTests(unittest.TestCase):
    def _seed_store(self, store: SqliteMediaArtifactStore) -> None:
        source_media = SourceMedia(
            source_media_id="src-yt-abc123XYZ",
            platform="youtube",
            external_id="abc123XYZ",
            canonical_url="https://www.youtube.com/watch?v=abc123XYZ",
            media_type="interview",
            language="en",
            duration_seconds=90,
            created_at="2026-05-27T18:00:00Z",
            captured_at="2026-05-27T18:00:00Z",
            last_seen_at="2026-05-27T18:00:00Z",
            source_hash="sha256:src",
        )
        source_metadata = SourceMetadata(
            source_metadata_id="meta-yt-abc123XYZ",
            source_media_id=source_media.source_media_id,
            accent_profile="mixed",
            speech_rate_profile="medium_fast",
            subtitle_type="official",
            transcript_quality=0.9,
            connected_speech_density=0.6,
            noise_level=0.2,
            pedagogical_category="listening_authentic",
            context_tags=("modulo:ingles", "origem:youtube"),
        )
        raw_transcript = RawTranscript(
            raw_transcript_id="raw-yt-abc123XYZ",
            source_media_id=source_media.source_media_id,
            provider="youtube_transcript_api",
            raw_text="I am gonna call you now. We should practice listening today.",
            raw_timestamps=("00:00:01.000", "00:00:05.000", "00:00:08.200"),
            locale="en",
            ingestion_version="v1",
            content_hash="sha256:raw",
            captured_at="2026-05-27T18:00:00Z",
        )
        curated_transcript = CuratedTranscript(
            curated_transcript_id="cur-yt-abc123XYZ",
            source_media_id=source_media.source_media_id,
            raw_transcript_id=raw_transcript.raw_transcript_id,
            curated_text="I am going to call you now. We should practice listening today.",
            curation_status="approved",
            curation_notes="normalizado",
            quality_score=4.5,
            curated_version="v1",
            approved_at="2026-05-27T18:00:00Z",
        )
        segments = segment_curated_transcript(
            curated_transcript_id=curated_transcript.curated_transcript_id,
            source_media_id=source_media.source_media_id,
            curated_text=curated_transcript.curated_text,
            total_duration_seconds=source_media.duration_seconds,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
        )

        store.upsert_source_media(source_media)
        store.upsert_source_metadata(source_metadata)
        store.upsert_raw_transcript(raw_transcript)
        store.upsert_curated_transcript(curated_transcript)
        store.upsert_study_segments(segments)

    def test_ingest_and_sync_anki_with_mocked_ingestion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteMediaArtifactStore(Path(tmp) / "media.db")
            self._seed_store(store)
            client = _FakeAnkiClient()

            with patch(
                "app_estudo.integrations.youtube_anki_sync.ingest_first_youtube_video_from_source",
                return_value=YoutubeIngestionResult(
                    source_media_id="src-yt-abc123XYZ",
                    raw_transcript_id="raw-yt-abc123XYZ",
                    curated_transcript_id="cur-yt-abc123XYZ",
                    study_segments_created=1,
                    quality_gate_status="approved",
                ),
            ):
                summary = ingest_youtube_video_and_sync_anki(
                    youtube_url="https://www.youtube.com/watch?v=abc123XYZ",
                    title="Sample interview",
                    store=store,
                    anki_client=client,
                )

        self.assertEqual(summary.quality_gate_status, "approved")
        self.assertGreaterEqual(summary.total_segments, 1)
        self.assertEqual(summary.attempted_notes, summary.total_segments)
        self.assertEqual(summary.synced_notes, summary.total_segments)


if __name__ == "__main__":
    unittest.main()
