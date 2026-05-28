import tempfile
import unittest
from pathlib import Path

from app_estudo.integrations import SqliteMediaArtifactStore
from app_estudo.integrations.youtube_ingestion import (
    YoutubeTranscriptPayload,
    extract_youtube_video_id,
    ingest_first_youtube_video,
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


if __name__ == "__main__":
    unittest.main()
