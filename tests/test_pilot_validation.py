import unittest

from app_estudo.integrations.pilot_validation import validate_pilot_notes


def _build_note(note_id: int, source_id: str, complete: bool = True) -> dict[str, object]:
    fields = {
        "source_id": {"value": source_id},
        "source_type": {"value": "podcast"},
        "title": {"value": f"Title {note_id}"},
        "transcript_excerpt": {"value": "I gotta check that later."},
        "target_expression": {"value": "gotta"},
        "explanation_ptbr": {"value": "Reducao de got to."},
        "listening_context": {"value": "Conversa informal."},
        "level": {"value": "B1"},
        "accent": {"value": "american"},
        "audio_reference": {"value": "https://example.org/audio.mp3"},
        "created_from_stage": {"value": "E5.S2"},
        "logical_key": {"value": f"{source_id}|gotta|reduction|B1"},
        "evaluation_score": {"value": "4.1"},
        "evaluation_classification": {"value": "recommended"},
    }

    if not complete:
        fields["evaluation_classification"] = {"value": ""}
        fields["audio_reference"] = {"value": ""}

    return {"noteId": note_id, "fields": fields}


class PilotValidationTests(unittest.TestCase):
    def test_validate_pilot_notes_approved(self) -> None:
        notes = [_build_note(note_id=i, source_id=f"src-{i}") for i in range(1, 21)]

        report = validate_pilot_notes(
            notes,
            min_items=20,
            traceability_threshold=95.0,
            duplicate_rate_threshold=2.0,
            classification_threshold=100.0,
        )

        self.assertEqual(report["status"], "approved")
        self.assertEqual(report["failed_criteria"], [])
        self.assertEqual(report["metrics"]["total_notes"], 20)

    def test_validate_pilot_notes_needs_review(self) -> None:
        notes = [
            _build_note(note_id=1, source_id="dup-1", complete=False),
            _build_note(note_id=2, source_id="dup-1", complete=True),
            _build_note(note_id=3, source_id="src-3", complete=True),
        ]

        report = validate_pilot_notes(
            notes,
            min_items=5,
            traceability_threshold=95.0,
            duplicate_rate_threshold=2.0,
            classification_threshold=100.0,
        )

        self.assertEqual(report["status"], "needs_review")
        self.assertIn("min_items", report["failed_criteria"])
        self.assertIn("traceability", report["failed_criteria"])
        self.assertIn("duplicate_rate", report["failed_criteria"])
        self.assertIn("classification", report["failed_criteria"])
        self.assertGreater(report["metrics"]["missing_field_counts"]["audio_reference"], 0)


if __name__ == "__main__":
    unittest.main()
