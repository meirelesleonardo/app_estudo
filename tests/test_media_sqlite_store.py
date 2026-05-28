import tempfile
import unittest
from pathlib import Path

from app_estudo.domain import (
    CuratedTranscript,
    RawTranscript,
    SourceMedia,
    SourceMetadata,
    segment_curated_transcript,
)
from app_estudo.integrations import SqliteMediaArtifactStore


class SqliteMediaArtifactStoreTests(unittest.TestCase):
    def _source_media(self) -> SourceMedia:
        return SourceMedia(
            source_media_id="src-yt-100",
            platform="youtube",
            external_id="video-abc-100",
            canonical_url="https://youtube.com/watch?v=video-abc-100",
            media_type="podcast",
            language="en",
            duration_seconds=90,
            created_at="2026-05-27T15:00:00Z",
            captured_at="2026-05-27T15:10:00Z",
            last_seen_at="2026-05-27T15:11:00Z",
            source_hash="sha256:source100",
        )

    def _source_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            source_metadata_id="meta-100",
            source_media_id="src-yt-100",
            accent_profile="american",
            speech_rate_profile="medium_fast",
            subtitle_type="official",
            transcript_quality=0.9,
            connected_speech_density=0.7,
            noise_level=0.2,
            pedagogical_category="listening_authentic",
            context_tags=("modulo:ingles", "nivel:b1"),
        )

    def _raw_transcript(self) -> RawTranscript:
        return RawTranscript(
            raw_transcript_id="raw-100",
            source_media_id="src-yt-100",
            provider="youtube_auto",
            raw_text="I am gonna call you now. We should practice listening today.",
            raw_timestamps=("00:00:01.000", "00:00:05.000"),
            locale="en-us",
            ingestion_version="v1",
            content_hash="sha256:raw100",
            captured_at="2026-05-27T15:12:00Z",
        )

    def _curated_transcript(self) -> CuratedTranscript:
        return CuratedTranscript(
            curated_transcript_id="cur-100",
            source_media_id="src-yt-100",
            raw_transcript_id="raw-100",
            curated_text="I am going to call you now. We should practice listening today.",
            curation_status="approved",
            curation_notes="Expanded contractions for readability.",
            quality_score=4.6,
            curated_version="v1",
            approved_at="2026-05-27T15:13:00Z",
        )

    def test_persists_artifacts_and_audit_events_in_sqlite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media_artifacts.db"
            store = SqliteMediaArtifactStore(db_path)

            source_media = self._source_media()
            source_metadata = self._source_metadata()
            raw_transcript = self._raw_transcript()
            curated_transcript = self._curated_transcript()
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

            counts = store.get_table_counts()
            self.assertEqual(counts["source_media"], 1)
            self.assertEqual(counts["source_metadata"], 1)
            self.assertEqual(counts["raw_transcript"], 1)
            self.assertEqual(counts["curated_transcript"], 1)
            self.assertEqual(counts["study_segment"], len(segments))
            self.assertEqual(counts["audit_event"], 4 + len(segments))

            segment_events = store.query_audit_events(artifact_type="study_segment")
            self.assertEqual(len(segment_events), len(segments))
            self.assertTrue(all(event["artifact_hash"].startswith("sha1:") for event in segment_events))

    def test_upsert_source_media_updates_row_without_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media_artifacts.db"
            store = SqliteMediaArtifactStore(db_path)

            source_media = self._source_media()
            store.upsert_source_media(source_media)

            updated = SourceMedia(
                source_media_id=source_media.source_media_id,
                platform=source_media.platform,
                external_id=source_media.external_id,
                canonical_url=source_media.canonical_url,
                media_type=source_media.media_type,
                language=source_media.language,
                duration_seconds=120,
                created_at=source_media.created_at,
                captured_at=source_media.captured_at,
                last_seen_at="2026-05-27T16:00:00Z",
                source_hash="sha256:source100-updated",
            )
            store.upsert_source_media(updated)

            counts = store.get_table_counts()
            self.assertEqual(counts["source_media"], 1)
            self.assertEqual(counts["audit_event"], 2)

    def test_reads_curated_and_segments_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media_artifacts.db"
            store = SqliteMediaArtifactStore(db_path)

            source_media = self._source_media()
            source_metadata = self._source_metadata()
            raw_transcript = self._raw_transcript()
            curated_transcript = self._curated_transcript()
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

            curated_payload = store.get_curated_transcript_payload(curated_transcript.curated_transcript_id)
            segment_payloads = store.list_study_segment_payloads(curated_transcript.curated_transcript_id)

            self.assertIsNotNone(curated_payload)
            self.assertEqual(curated_payload["curated_transcript_id"], curated_transcript.curated_transcript_id)
            self.assertEqual(len(segment_payloads), len(segments))
            self.assertEqual(segment_payloads[0]["segment_index"], 0)


if __name__ == "__main__":
    unittest.main()
