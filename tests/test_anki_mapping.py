import unittest

from app_estudo.domain import CuratedStudyItem, evaluate_listening_item
from app_estudo.integrations import map_to_anki_logical_note


class AnkiMappingTests(unittest.TestCase):
    def _item(self) -> CuratedStudyItem:
        return CuratedStudyItem(
            source_id="pod-ep-020-02:10-02:28",
            source_type="podcast",
            source_url="https://example.org/episode-20",
            title="Workplace Routines",
            transcript_excerpt="I hafta submit this by noon.",
            target_expression="hafta",
            explanation_ptbr="Reducao de have to em fala acelerada.",
            listening_context="Conversa sobre prazos de trabalho.",
            level="B1",
            accent="american",
            phenomenon="reduction",
            tags_context=("modulo:ingles", "habilidade:listening", "nivel:B1"),
            audio_reference="https://example.org/audio/ep-20-segment.mp3",
            duration_seconds=18,
            created_from_stage="E5.S2",
        )

    def _evaluation(self):
        scores = {
            "audio_clarity": 4.0,
            "speech_speed": 3.5,
            "connected_speech_presence": 4.5,
            "subtitle_transcript_quality": 4.0,
            "context_naturalness": 4.0,
            "pedagogical_reusability": 4.0,
        }
        return evaluate_listening_item(self._item(), scores)

    def test_maps_deck_fields_and_note_unique_id(self) -> None:
        item = self._item()
        note = map_to_anki_logical_note(item, self._evaluation())

        self.assertEqual(note.deck_name, "Ingles::Listening::B1")
        self.assertEqual(note.note_unique_id, item.logical_key)
        self.assertEqual(note.fields["source_id"], item.source_id)
        self.assertEqual(note.fields["evaluation_classification"], "recommended")

    def test_composes_expected_tags_without_duplicates(self) -> None:
        note = map_to_anki_logical_note(self._item(), self._evaluation())

        self.assertIn("modulo:ingles", note.tags)
        self.assertIn("habilidade:listening", note.tags)
        self.assertIn("nivel:b1", note.tags)
        self.assertIn("origem:podcast", note.tags)
        self.assertIn("sotaque:american", note.tags)
        self.assertIn("fenomeno:reduction", note.tags)
        self.assertIn("status:curated", note.tags)
        self.assertIn("avaliacao:recommended", note.tags)
        self.assertEqual(len(note.tags), len(set(note.tags)))

    def test_serialization_contains_required_top_level_keys(self) -> None:
        payload = map_to_anki_logical_note(self._item(), self._evaluation()).to_dict()

        self.assertIn("deck_name", payload)
        self.assertIn("fields", payload)
        self.assertIn("tags", payload)
        self.assertIn("media", payload)
        self.assertIn("note_unique_id", payload)


if __name__ == "__main__":
    unittest.main()
