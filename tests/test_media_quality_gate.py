import unittest

from app_estudo.domain import CuratedTranscript, SourceMetadata
from app_estudo.domain.segmentation import segment_curated_transcript
from app_estudo.integrations.media_quality_gate import evaluate_e4_quality_gate


class MediaQualityGateTests(unittest.TestCase):
    def _metadata(self, transcript_quality: float = 0.9, noise_level: float = 0.2) -> SourceMetadata:
        return SourceMetadata(
            source_metadata_id="meta-1",
            source_media_id="src-1",
            accent_profile="american",
            speech_rate_profile="medium_fast",
            subtitle_type="official",
            transcript_quality=transcript_quality,
            connected_speech_density=0.7,
            noise_level=noise_level,
            pedagogical_category="listening_authentic",
            context_tags=("modulo:ingles", "nivel:b1"),
        )

    def _curated(self, status: str = "approved") -> CuratedTranscript:
        return CuratedTranscript(
            curated_transcript_id="cur-1",
            source_media_id="src-1",
            raw_transcript_id="raw-1",
            curated_text="Sentence one. Sentence two. Sentence three.",
            curation_status=status,
            curation_notes="notes",
            quality_score=4.5,
            curated_version="v1",
            approved_at="2026-05-27T18:00:00Z" if status == "approved" else None,
        )

    def _segments(self):
        return segment_curated_transcript(
            curated_transcript_id="cur-1",
            source_media_id="src-1",
            curated_text="Sentence one. Sentence two. Sentence three. Sentence four.",
            total_duration_seconds=80,
            pedagogical_unit="listening_core",
            difficulty_band="B1",
        )

    def test_approves_when_all_checks_pass(self) -> None:
        result = evaluate_e4_quality_gate(
            source_metadata=self._metadata(),
            curated_transcript=self._curated("approved"),
            segments=self._segments(),
        )

        self.assertTrue(result.approved)
        self.assertEqual(result.status, "approved")

    def test_rejects_when_curated_not_approved(self) -> None:
        result = evaluate_e4_quality_gate(
            source_metadata=self._metadata(),
            curated_transcript=self._curated("review_required"),
            segments=[],
        )

        self.assertFalse(result.approved)
        self.assertEqual(result.status, "rejected")
        self.assertGreaterEqual(len(result.reasons), 1)

    def test_rejects_when_noise_too_high(self) -> None:
        result = evaluate_e4_quality_gate(
            source_metadata=self._metadata(noise_level=0.8),
            curated_transcript=self._curated("approved"),
            segments=self._segments(),
        )

        self.assertFalse(result.approved)
        self.assertIn("noise_level acima do limite operacional", result.reasons)


if __name__ == "__main__":
    unittest.main()
