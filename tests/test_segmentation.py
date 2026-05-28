import unittest

from app_estudo.domain import StudySegment, segment_curated_transcript


class StudySegmentTests(unittest.TestCase):
    def test_reject_duration_outside_operational_range(self) -> None:
        with self.assertRaises(ValueError):
            StudySegment(
                study_segment_id="seg-1",
                curated_transcript_id="cur-1",
                source_media_id="src-1",
                segment_index=0,
                segment_start_ms=0,
                segment_end_ms=9000,
                segment_text="Short.",
                pedagogical_unit="connected_speech",
                difficulty_band="B1",
                segment_hash="sha1:test",
            )


class SegmentationPipelineTests(unittest.TestCase):
    def test_generates_multiple_segments_for_multi_sentence_text(self) -> None:
        text = (
            "This is the first sentence for context. "
            "This is the second sentence to keep progression. "
            "Here comes a third sentence with more content. "
            "Finally a fourth sentence to close the section."
        )

        segments = segment_curated_transcript(
            curated_transcript_id="cur-0001",
            source_media_id="src-0001",
            curated_text=text,
            total_duration_seconds=80,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
        )

        self.assertGreater(len(segments), 1)
        self.assertTrue(all(isinstance(segment, StudySegment) for segment in segments))
        self.assertEqual(segments[0].study_segment_id, "seg-cur-0001-000")

    def test_generates_deterministic_hashes_for_same_input(self) -> None:
        text = "Sentence one. Sentence two. Sentence three."

        first_run = segment_curated_transcript(
            curated_transcript_id="cur-0002",
            source_media_id="src-0002",
            curated_text=text,
            total_duration_seconds=45,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
        )
        second_run = segment_curated_transcript(
            curated_transcript_id="cur-0002",
            source_media_id="src-0002",
            curated_text=text,
            total_duration_seconds=45,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
        )

        self.assertEqual(
            [segment.segment_hash for segment in first_run],
            [segment.segment_hash for segment in second_run],
        )

    def test_reject_invalid_total_duration(self) -> None:
        with self.assertRaises(ValueError):
            segment_curated_transcript(
                curated_transcript_id="cur-0003",
                source_media_id="src-0003",
                curated_text="Only one sentence.",
                total_duration_seconds=0,
                pedagogical_unit="listening_core",
                difficulty_band="B1",
            )


if __name__ == "__main__":
    unittest.main()
