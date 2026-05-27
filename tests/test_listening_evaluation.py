import unittest

from app_estudo.domain import CuratedStudyItem
from app_estudo.domain.listening_evaluation import evaluate_listening_item


class ListeningEvaluationTests(unittest.TestCase):
    def _item(self) -> CuratedStudyItem:
        return CuratedStudyItem(
            source_id="pod-ep-011-01:00-01:20",
            source_type="podcast",
            source_url="https://example.org/episode-11",
            title="Weekend Plans",
            transcript_excerpt="I kinda need to leave now.",
            target_expression="kinda",
            explanation_ptbr="Reducao comum de kind of em fala natural.",
            listening_context="Conversa rapida entre amigos.",
            level="B1",
            accent="american",
            phenomenon="reduction",
            tags_context=("modulo:ingles", "habilidade:listening", "nivel:B1"),
            audio_reference="https://example.org/audio/ep-11-segment.mp3",
            duration_seconds=20,
            created_from_stage="E5.S2",
        )

    def _full_scores(self, value: float) -> dict[str, float]:
        return {
            "audio_clarity": value,
            "speech_speed": value,
            "connected_speech_presence": value,
            "subtitle_transcript_quality": value,
            "context_naturalness": value,
            "pedagogical_reusability": value,
        }

    def test_score_is_5_and_recommended_when_all_criteria_are_5(self) -> None:
        result = evaluate_listening_item(self._item(), self._full_scores(5.0))

        self.assertEqual(result.score_final, 5.0)
        self.assertEqual(result.classification, "recommended")

    def test_score_is_3_and_recommended_with_reservations(self) -> None:
        result = evaluate_listening_item(self._item(), self._full_scores(3.0))

        self.assertEqual(result.score_final, 3.0)
        self.assertEqual(result.classification, "recommended_with_reservations")

    def test_score_below_3_is_not_recommended(self) -> None:
        result = evaluate_listening_item(self._item(), self._full_scores(2.5))

        self.assertEqual(result.score_final, 2.5)
        self.assertEqual(result.classification, "not_recommended")

    def test_reject_missing_criterion(self) -> None:
        scores = self._full_scores(4.0)
        del scores["audio_clarity"]

        with self.assertRaises(ValueError):
            evaluate_listening_item(self._item(), scores)

    def test_reject_value_out_of_range(self) -> None:
        scores = self._full_scores(4.0)
        scores["speech_speed"] = 5.5

        with self.assertRaises(ValueError):
            evaluate_listening_item(self._item(), scores)


if __name__ == "__main__":
    unittest.main()
