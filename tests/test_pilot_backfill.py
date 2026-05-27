import unittest

from app_estudo.integrations.pilot_backfill import plan_backfill_updates


class PilotBackfillTests(unittest.TestCase):
    def test_plan_backfill_updates_fills_audio_and_score(self) -> None:
        note = {
            "noteId": 10,
            "fields": {
                "source_id": {"value": "src-10"},
                "evaluation_classification": {"value": "recommended_with_reservations"},
                "evaluation_score": {"value": ""},
                "audio_reference": {"value": ""},
            },
        }

        updates, extra_tags = plan_backfill_updates(note)

        self.assertEqual(updates["evaluation_score"], "3.0")
        self.assertEqual(updates["audio_reference"], "pending://audio/src-10")
        self.assertIn("status:pending_audio_reference", extra_tags)

    def test_plan_backfill_updates_keeps_existing_values(self) -> None:
        note = {
            "noteId": 11,
            "fields": {
                "source_id": {"value": "src-11"},
                "evaluation_classification": {"value": "recommended"},
                "evaluation_score": {"value": "4.2"},
                "audio_reference": {"value": "https://example.org/audio.mp3"},
            },
        }

        updates, extra_tags = plan_backfill_updates(note)

        self.assertEqual(updates, {})
        self.assertEqual(extra_tags, set())


if __name__ == "__main__":
    unittest.main()
