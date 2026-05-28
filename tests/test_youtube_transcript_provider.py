import unittest
from unittest.mock import patch

from app_estudo.integrations.youtube_transcript_provider import (
    fetch_transcript_from_youtube,
)


class _FakeApi:
    @staticmethod
    def get_transcript(video_id, languages):
        return [
            {"text": "Hello", "start": 0.0, "duration": 1.2},
            {"text": "world", "start": 1.2, "duration": 1.0},
        ]


class YouTubeTranscriptProviderTests(unittest.TestCase):
    @patch("app_estudo.integrations.youtube_transcript_provider._load_transcript_api", return_value=_FakeApi)
    def test_fetch_transcript_builds_expected_result(self, _load_api) -> None:
        result = fetch_transcript_from_youtube(video_id="abc123", preferred_languages=("en",))

        self.assertEqual(result.video_id, "abc123")
        self.assertEqual(result.raw_text, "Hello world")
        self.assertEqual(result.raw_timestamps, ("00:00:00.000", "00:00:01.200"))
        self.assertEqual(result.locale, "en")
        self.assertEqual(result.provider, "youtube_transcript_api")
        self.assertEqual(result.estimated_duration_seconds, 3)

    def test_rejects_empty_video_id(self) -> None:
        with self.assertRaises(ValueError):
            fetch_transcript_from_youtube(video_id="   ")

    @patch("app_estudo.integrations.youtube_transcript_provider._load_transcript_api", return_value=_FakeApi)
    def test_rejects_empty_language_tuple(self, _load_api) -> None:
        with self.assertRaises(ValueError):
            fetch_transcript_from_youtube(video_id="abc123", preferred_languages=())


if __name__ == "__main__":
    unittest.main()