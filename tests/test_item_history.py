import tempfile
import unittest
from pathlib import Path

from app_estudo.integrations.item_history import JsonlItemHistoryStore, new_event


class ItemHistoryTests(unittest.TestCase):
    def test_append_and_query_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "events.jsonl"
            store = JsonlItemHistoryStore(file_path)

            store.append(
                new_event(
                    event_type="sync",
                    item_key="src-1",
                    state="synced",
                    action="created",
                    note_id=101,
                    error_type=None,
                    error_message=None,
                    metadata={"deck": "Ingles::Listening::B1"},
                )
            )
            store.append(
                new_event(
                    event_type="sync",
                    item_key="src-2",
                    state="updated",
                    action="updated",
                    note_id=102,
                    error_type=None,
                    error_message=None,
                    metadata={"deck": "Ingles::Listening::B1"},
                )
            )

            all_rows = store.query()
            self.assertEqual(len(all_rows), 2)

            src1_rows = store.query(item_key="src-1")
            self.assertEqual(len(src1_rows), 1)
            self.assertEqual(src1_rows[0]["state"], "synced")

            limited_rows = store.query(limit=1)
            self.assertEqual(len(limited_rows), 1)
            self.assertEqual(limited_rows[0]["item_key"], "src-2")


if __name__ == "__main__":
    unittest.main()
