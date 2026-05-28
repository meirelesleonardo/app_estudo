import unittest

from app_estudo.domain import normalize_transcript_text


class TranscriptNormalizationTests(unittest.TestCase):
    def test_normalization_pipeline_applies_expected_flags(self) -> None:
        raw_text = "[00:00:03.200] I'm gonna uh call you @@ now now (noise)."

        result = normalize_transcript_text(raw_text, normalization_version="v1")

        self.assertEqual(result.normalized_text, "i am going to call you now.")
        self.assertEqual(result.normalization_version, "v1")
        self.assertFalse(result.incomplete_sentence)
        self.assertEqual(
            result.transformation_flags,
            (
                "timestamps_removed",
                "contractions_expanded",
                "fillers_removed",
                "noise_markers_removed",
                "special_chars_removed",
                "duplicate_tokens_removed",
                "whitespace_normalized",
            ),
        )

    def test_marks_incomplete_sentence_for_review(self) -> None:
        raw_text = "we are testing normalization"

        result = normalize_transcript_text(raw_text, normalization_version="v2")

        self.assertTrue(result.incomplete_sentence)
        self.assertIn("incomplete_sentence_detected", result.transformation_flags)

    def test_reject_empty_input_text(self) -> None:
        with self.assertRaises(ValueError):
            normalize_transcript_text("   ", normalization_version="v1")

    def test_reject_invalid_version_pattern(self) -> None:
        with self.assertRaises(ValueError):
            normalize_transcript_text("Simple text.", normalization_version="1")

    def test_removes_fillers_and_noise_markers(self) -> None:
        raw_text = "um this is (laughter) a clean line."

        result = normalize_transcript_text(raw_text, normalization_version="v1")

        self.assertEqual(result.normalized_text, "this is a clean line.")
        self.assertIn("fillers_removed", result.transformation_flags)
        self.assertIn("noise_markers_removed", result.transformation_flags)


if __name__ == "__main__":
    unittest.main()
