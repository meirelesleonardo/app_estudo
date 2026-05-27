import unittest
from unittest.mock import patch

from app_estudo.integrations.anki_mapping import LogicalAnkiNote
from app_estudo.integrations.ankiconnect_client import (
    AnkiConnectClient,
    AnkiConnectConnectivityError,
)


def _build_note() -> LogicalAnkiNote:
    return LogicalAnkiNote(
        deck_name="Ingles::Listening::B1",
        fields={
            "source_id": "pod-ep-030-03:00-03:16",
            "source_type": "podcast",
            "title": "Budget Planning",
            "transcript_excerpt": "I gotta check that later.",
            "target_expression": "gotta",
            "explanation_ptbr": "Reducao de got to.",
            "listening_context": "Conversa informal sobre tarefas.",
            "level": "B1",
            "accent": "american",
            "audio_reference": "https://example.org/audio/ep-30-segment.mp3",
            "created_from_stage": "E5.S2",
            "tags_context": ["modulo:ingles", "habilidade:listening"],
        },
        tags=("modulo:ingles", "habilidade:listening", "nivel:b1"),
        media={
            "reference_path_or_url": "https://example.org/audio/ep-30-segment.mp3",
            "duration": 16,
        },
        note_unique_id="pod-ep-030-03:00-03:16|gotta|reduction|B1",
    )


class AnkiConnectClientTests(unittest.TestCase):
    def test_sync_creates_note_when_not_found(self) -> None:
        client = AnkiConnectClient()
        note = _build_note()

        with patch.object(client, "_invoke", side_effect=[[], 101]) as invoke_mock:
            result = client.sync_logical_note(note)

        self.assertEqual(result.state, "synced")
        self.assertEqual(result.action, "created")
        self.assertEqual(result.note_id, 101)
        self.assertEqual(invoke_mock.call_count, 2)

    def test_sync_updates_existing_note(self) -> None:
        client = AnkiConnectClient()
        note = _build_note()

        with patch.object(client, "_invoke", side_effect=[[88], None, None]):
            result = client.sync_logical_note(note)

        self.assertEqual(result.state, "updated")
        self.assertEqual(result.action, "updated")
        self.assertEqual(result.note_id, 88)

    def test_sync_returns_conflict_when_multiple_notes_are_found(self) -> None:
        client = AnkiConnectClient()

        with patch.object(client, "_invoke", side_effect=[[10, 11]]):
            result = client.sync_logical_note(_build_note())

        self.assertEqual(result.state, "conflict")
        self.assertEqual(result.error_type, "conflict")

    def test_sync_returns_pending_on_connectivity_failure(self) -> None:
        client = AnkiConnectClient()

        with patch.object(client, "_invoke", side_effect=AnkiConnectConnectivityError("timeout")):
            result = client.sync_logical_note(_build_note())

        self.assertEqual(result.state, "pending")
        self.assertEqual(result.error_type, "connectivity")

    def test_sync_returns_blocked_on_validation_error(self) -> None:
        client = AnkiConnectClient()
        note = _build_note()
        note.fields.pop("source_id")

        result = client.sync_logical_note(note)

        self.assertEqual(result.state, "blocked")
        self.assertEqual(result.error_type, "validation")


if __name__ == "__main__":
    unittest.main()
