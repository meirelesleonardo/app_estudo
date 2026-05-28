import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app_estudo.integrations.youtube_audio_extraction import extract_youtube_audio


class _FakeYdlClient:
    def __init__(self, options):
        self.options = options

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def extract_info(self, url, download=True):
        _ = (url, download)
        return {
            "title": "Sample video",
            "duration": 125,
            "requested_downloads": [{"filepath": self.options["outtmpl"].replace("%(ext)s", "webm")}],
        }


class _FakeYtDlpModule:
    YoutubeDL = _FakeYdlClient


class YouTubeAudioExtractionTests(unittest.TestCase):
    @patch("app_estudo.integrations.youtube_audio_extraction._load_yt_dlp", return_value=_FakeYtDlpModule)
    def test_extract_audio_returns_expected_result(self, _load_yt_dlp) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = extract_youtube_audio(
                youtube_url="https://www.youtube.com/watch?v=abc123XYZ",
                output_dir=Path(tmp) / "audio",
            )

            self.assertEqual(result.video_id, "abc123XYZ")
            self.assertEqual(result.title, "Sample video")
            self.assertEqual(result.duration_seconds, 125)
            self.assertTrue(result.audio_file_path.endswith("abc123XYZ.webm"))

    def test_rejects_invalid_youtube_url(self) -> None:
        with self.assertRaises(ValueError):
            extract_youtube_audio(youtube_url="https://example.com/video")


if __name__ == "__main__":
    unittest.main()