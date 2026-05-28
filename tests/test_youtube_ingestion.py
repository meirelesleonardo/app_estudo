import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app_estudo.integrations import SqliteMediaArtifactStore
from app_estudo.integrations.youtube_transcript_provider import YoutubeTranscriptFetchResult
from app_estudo.integrations.youtube_ingestion import (
    YoutubeTranscriptPayload,
    extract_youtube_video_id,
    ingest_first_youtube_video,
    ingest_first_youtube_video_from_source,
)


class YouTubeIngestionTests(unittest.TestCase):
    def _payload(self) -> YoutubeTranscriptPayload:
        return YoutubeTranscriptPayload(
            title="Sample interview",
            duration_seconds=90,
            raw_text="I'm gonna call you now. We should practice listening today.",
            raw_timestamps=("00:00:01.000", "00:00:05.000", "00:00:08.200"),
            locale="en",
            provider="youtube_captions",
        )

    def test_extract_video_id_from_standard_url(self) -> None:
        video_id = extract_youtube_video_id("https://www.youtube.com/watch?v=abc123XYZ")
        self.assertEqual(video_id, "abc123XYZ")

    def test_extract_video_id_from_short_url(self) -> None:
        video_id = extract_youtube_video_id("https://youtu.be/abc123XYZ")
        self.assertEqual(video_id, "abc123XYZ")

    def test_ingests_video_and_persists_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media.db"
            store = SqliteMediaArtifactStore(db_path)

            result = ingest_first_youtube_video(
                youtube_url="https://www.youtube.com/watch?v=abc123XYZ",
                transcript_payload=self._payload(),
                store=store,
            )

            self.assertEqual(result.quality_gate_status, "approved")
            self.assertGreaterEqual(result.study_segments_created, 1)

            counts = store.get_table_counts()
            self.assertEqual(counts["source_media"], 1)
            self.assertEqual(counts["raw_transcript"], 1)
            self.assertEqual(counts["curated_transcript"], 1)
            self.assertGreaterEqual(counts["study_segment"], 1)
            self.assertGreaterEqual(counts["audit_event"], 4)

    def test_ingests_with_rejected_gate_when_quality_low(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media.db"
            store = SqliteMediaArtifactStore(db_path)

            result = ingest_first_youtube_video(
                youtube_url="https://www.youtube.com/watch?v=abc123XYZ",
                transcript_payload=self._payload(),
                store=store,
                transcript_quality=0.5,
                noise_level=0.8,
            )

            self.assertEqual(result.quality_gate_status, "rejected")
            self.assertEqual(result.study_segments_created, 0)

    @patch("app_estudo.integrations.youtube_ingestion.fetch_transcript_from_youtube")
    def test_ingests_video_from_real_provider_contract(self, fetch_mock) -> None:
        fetch_mock.return_value = YoutubeTranscriptFetchResult(
            video_id="abc123XYZ",
            raw_text="hello there this is a short transcript",
            raw_timestamps=("00:00:00.000", "00:00:02.100"),
            locale="en",
            provider="youtube_transcript_api",
            estimated_duration_seconds=3,
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "media.db"
            store = SqliteMediaArtifactStore(db_path)

            result = ingest_first_youtube_video_from_source(
                youtube_url="https://www.youtube.com/watch?v=abc123XYZ",
                title="Video real",
                store=store,
            )

            self.assertEqual(result.quality_gate_status, "approved")
            self.assertGreaterEqual(result.study_segments_created, 1)
            fetch_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
