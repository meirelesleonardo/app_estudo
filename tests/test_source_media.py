import unittest

from app_estudo.domain import SourceMedia, SourceMetadata


class SourceMediaTests(unittest.TestCase):
    def _valid_media_payload(self) -> dict:
        return {
            "source_media_id": "src-yt-0001",
            "platform": "YouTube",
            "external_id": "abc123xyz",
            "canonical_url": "https://youtube.com/watch?v=abc123xyz",
            "media_type": "ted_talk",
            "language": "EN",
            "duration_seconds": 645,
            "created_at": "2026-05-27T10:00:00Z",
            "captured_at": "2026-05-27T10:30:00Z",
            "last_seen_at": "2026-05-27T10:35:00Z",
            "source_hash": "sha256:111222333",
        }

    def _valid_metadata_payload(self) -> dict:
        return {
            "source_metadata_id": "meta-0001",
            "source_media_id": "src-yt-0001",
            "accent_profile": "American",
            "speech_rate_profile": "medium_fast",
            "subtitle_type": "official",
            "transcript_quality": 0.95,
            "connected_speech_density": 0.7,
            "noise_level": 0.1,
            "pedagogical_category": "listening_authentic",
            "context_tags": ("modulo:ingles", "nivel:B1", "nivel:b1"),
        }

    def test_build_valid_source_media_and_generate_source_key(self) -> None:
        source_media = SourceMedia(**self._valid_media_payload())

        self.assertEqual(source_media.platform, "youtube")
        self.assertEqual(source_media.language, "en")
        self.assertEqual(source_media.source_key, "youtube|abc123xyz")

    def test_reject_invalid_media_type(self) -> None:
        payload = self._valid_media_payload()
        payload["media_type"] = "livestream"

        with self.assertRaises(ValueError):
            SourceMedia(**payload)

    def test_reject_invalid_timestamp(self) -> None:
        payload = self._valid_media_payload()
        payload["captured_at"] = "27-05-2026 10:00"

        with self.assertRaises(ValueError):
            SourceMedia(**payload)

    def test_reject_non_positive_duration(self) -> None:
        payload = self._valid_media_payload()
        payload["duration_seconds"] = 0

        with self.assertRaises(ValueError):
            SourceMedia(**payload)


class SourceMetadataTests(unittest.TestCase):
    def _valid_payload(self) -> dict:
        return {
            "source_metadata_id": "meta-0001",
            "source_media_id": "src-yt-0001",
            "accent_profile": "American",
            "speech_rate_profile": "medium_fast",
            "subtitle_type": "official",
            "transcript_quality": 0.95,
            "connected_speech_density": 0.7,
            "noise_level": 0.1,
            "pedagogical_category": "listening_authentic",
            "context_tags": ("modulo:ingles", "nivel:B1", "nivel:b1"),
        }

    def test_build_valid_source_metadata_and_normalize_tags(self) -> None:
        metadata = SourceMetadata(**self._valid_payload())

        self.assertEqual(metadata.subtitle_type, "official")
        self.assertEqual(metadata.accent_profile, "american")
        self.assertEqual(metadata.context_tags, ("modulo:ingles", "nivel:b1"))

    def test_reject_invalid_subtitle_type(self) -> None:
        payload = self._valid_payload()
        payload["subtitle_type"] = "manual_only"

        with self.assertRaises(ValueError):
            SourceMetadata(**payload)

    def test_reject_score_out_of_range(self) -> None:
        payload = self._valid_payload()
        payload["transcript_quality"] = 1.4

        with self.assertRaises(ValueError):
            SourceMetadata(**payload)

    def test_reject_empty_context_tags_after_normalization(self) -> None:
        payload = self._valid_payload()
        payload["context_tags"] = ("   ", "")

        with self.assertRaises(ValueError):
            SourceMetadata(**payload)


if __name__ == "__main__":
    unittest.main()
