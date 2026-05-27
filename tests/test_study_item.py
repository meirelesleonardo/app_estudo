import unittest

from app_estudo.domain import CuratedStudyItem


class CuratedStudyItemTests(unittest.TestCase):
    def _valid_payload(self) -> dict:
        return {
            "source_id": "pod-ep-010-00:30-00:47",
            "source_type": "podcast",
            "source_url": "https://example.org/episode-10",
            "title": "Commuting and Daily Routines",
            "transcript_excerpt": "I was gonna call you later.",
            "target_expression": "gonna",
            "explanation_ptbr": "Reducao comum de 'going to' em fala natural.",
            "listening_context": "Dialogo informal sobre rotina diaria.",
            "level": "B1",
            "accent": "american",
            "phenomenon": "reduction",
            "tags_context": ("modulo:ingles", "habilidade:listening", "nivel:B1"),
            "audio_reference": "https://example.org/audio/ep-10-segment.mp3",
            "duration_seconds": 17,
            "created_from_stage": "E5.S2",
        }

    def test_build_valid_item_and_generate_logical_key(self) -> None:
        item = CuratedStudyItem(**self._valid_payload())

        self.assertEqual(item.level, "B1")
        self.assertEqual(item.tags_context, ("modulo:ingles", "habilidade:listening", "nivel:b1"))
        self.assertEqual(
            item.logical_key,
            "pod-ep-010-00:30-00:47|gonna|reduction|B1",
        )

    def test_reject_invalid_level(self) -> None:
        payload = self._valid_payload()
        payload["level"] = "D1"

        with self.assertRaises(ValueError):
            CuratedStudyItem(**payload)

    def test_reject_empty_required_field(self) -> None:
        payload = self._valid_payload()
        payload["title"] = "   "

        with self.assertRaises(ValueError):
            CuratedStudyItem(**payload)

    def test_reject_invalid_stage_pattern(self) -> None:
        payload = self._valid_payload()
        payload["created_from_stage"] = "E5"

        with self.assertRaises(ValueError):
            CuratedStudyItem(**payload)

    def test_reject_tags_when_empty_after_normalization(self) -> None:
        payload = self._valid_payload()
        payload["tags_context"] = ("   ", "")

        with self.assertRaises(ValueError):
            CuratedStudyItem(**payload)


if __name__ == "__main__":
    unittest.main()
