import unittest

from app_estudo.domain import CuratedTranscript, RawTranscript


class RawTranscriptTests(unittest.TestCase):
    def _valid_payload(self) -> dict:
        return {
            "raw_transcript_id": "raw-0001",
            "source_media_id": "src-yt-0001",
            "provider": "youtube_auto",
            "raw_text": "I was gonna call you later.",
            "raw_timestamps": ("00:00:03.000", "00:00:05.200", "00:00:03.000"),
            "locale": "EN-US",
            "ingestion_version": "v1",
            "content_hash": "sha256:raw111",
            "captured_at": "2026-05-27T12:00:00Z",
        }

    def test_build_valid_raw_transcript_and_lineage_key(self) -> None:
        transcript = RawTranscript(**self._valid_payload())

        self.assertEqual(transcript.provider, "youtube_auto")
        self.assertEqual(transcript.locale, "en-us")
        self.assertEqual(transcript.raw_timestamps, ("00:00:03.000", "00:00:05.200"))
        self.assertEqual(transcript.lineage_key, "src-yt-0001|raw-0001")

    def test_reject_empty_timestamps_after_normalization(self) -> None:
        payload = self._valid_payload()
        payload["raw_timestamps"] = (" ", "")

        with self.assertRaises(ValueError):
            RawTranscript(**payload)

    def test_reject_invalid_captured_at(self) -> None:
        payload = self._valid_payload()
        payload["captured_at"] = "27/05/2026 12:00"

        with self.assertRaises(ValueError):
            RawTranscript(**payload)


class CuratedTranscriptTests(unittest.TestCase):
    def _valid_payload(self) -> dict:
        return {
            "curated_transcript_id": "cur-0001",
            "source_media_id": "src-yt-0001",
            "raw_transcript_id": "raw-0001",
            "curated_text": "I am going to call you later.",
            "curation_status": "approved",
            "curation_notes": "Contractions expanded for readability.",
            "quality_score": 4.5,
            "curated_version": "v1",
            "approved_at": "2026-05-27T13:00:00Z",
        }

    def test_build_valid_curated_transcript_and_lineage_key(self) -> None:
        transcript = CuratedTranscript(**self._valid_payload())

        self.assertEqual(transcript.curation_status, "approved")
        self.assertEqual(transcript.lineage_key, "src-yt-0001|raw-0001|cur-0001")

    def test_reject_invalid_status(self) -> None:
        payload = self._valid_payload()
        payload["curation_status"] = "published"

        with self.assertRaises(ValueError):
            CuratedTranscript(**payload)

    def test_reject_approved_without_approved_at(self) -> None:
        payload = self._valid_payload()
        payload["approved_at"] = None

        with self.assertRaises(ValueError):
            CuratedTranscript(**payload)

    def test_reject_non_approved_with_approved_at(self) -> None:
        payload = self._valid_payload()
        payload["curation_status"] = "draft"

        with self.assertRaises(ValueError):
            CuratedTranscript(**payload)

    def test_reject_quality_score_out_of_range(self) -> None:
        payload = self._valid_payload()
        payload["quality_score"] = 5.5

        with self.assertRaises(ValueError):
            CuratedTranscript(**payload)


if __name__ == "__main__":
    unittest.main()
