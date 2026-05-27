import unittest

from app_estudo.integrations.anki_reconciliation import build_duplicate_groups


class AnkiReconciliationTests(unittest.TestCase):
    def _note(self, note_id: int, source_id: str) -> dict:
        return {
            "noteId": note_id,
            "fields": {
                "source_id": {"value": source_id}
            },
        }

    def test_build_duplicate_groups_keep_oldest(self) -> None:
        notes = [
            self._note(10, "src-1"),
            self._note(20, "src-1"),
            self._note(30, "src-2"),
            self._note(40, "src-2"),
            self._note(50, "src-2"),
            self._note(60, "src-3"),
        ]

        groups = build_duplicate_groups(notes, strategy="keep_oldest")

        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].source_id, "src-1")
        self.assertEqual(groups[0].canonical_note_id, 10)
        self.assertEqual(groups[0].duplicate_note_ids, (20,))
        self.assertEqual(groups[1].source_id, "src-2")
        self.assertEqual(groups[1].canonical_note_id, 30)
        self.assertEqual(groups[1].duplicate_note_ids, (40, 50))

    def test_build_duplicate_groups_keep_newest(self) -> None:
        notes = [
            self._note(1, "same-src"),
            self._note(9, "same-src"),
        ]

        groups = build_duplicate_groups(notes, strategy="keep_newest")

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].canonical_note_id, 9)
        self.assertEqual(groups[0].duplicate_note_ids, (1,))

    def test_invalid_strategy_raises(self) -> None:
        with self.assertRaises(ValueError):
            build_duplicate_groups([self._note(1, "x"), self._note(2, "x")], strategy="foo")


if __name__ == "__main__":
    unittest.main()
