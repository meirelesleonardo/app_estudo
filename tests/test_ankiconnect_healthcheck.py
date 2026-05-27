import json
import unittest
from unittest.mock import patch

from app_estudo.integrations.ankiconnect_healthcheck import check_ankiconnect


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class AnkiHealthcheckTests(unittest.TestCase):
    @patch("app_estudo.integrations.ankiconnect_healthcheck.request.urlopen")
    def test_returns_ok_true_when_version_response_is_valid(self, mock_urlopen) -> None:
        mock_urlopen.return_value = _FakeResponse({"result": 6, "error": None})

        result = check_ankiconnect()

        self.assertTrue(result.ok)
        self.assertEqual(result.version, 6)
        self.assertIsNone(result.error_message)

    @patch("app_estudo.integrations.ankiconnect_healthcheck.request.urlopen")
    def test_returns_ok_false_when_remote_error_exists(self, mock_urlopen) -> None:
        mock_urlopen.return_value = _FakeResponse({"result": None, "error": "deck not found"})

        result = check_ankiconnect()

        self.assertFalse(result.ok)
        self.assertIn("deck not found", result.error_message)


if __name__ == "__main__":
    unittest.main()
