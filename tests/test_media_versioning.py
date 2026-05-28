import unittest

from app_estudo.integrations.media_versioning import (
    ArtifactSnapshot,
    decide_version_action,
)


class MediaVersioningTests(unittest.TestCase):
    def _snapshot(
        self,
        *,
        artifact_type: str = "raw_transcript",
        artifact_id: str = "raw-1",
        version: str = "v1",
        content_hash: str = "sha256:a",
        status: str = "draft",
    ) -> ArtifactSnapshot:
        return ArtifactSnapshot(
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            version=version,
            content_hash=content_hash,
            status=status,
        )

    def test_returns_update_when_hash_changes(self) -> None:
        previous = self._snapshot(content_hash="sha256:old")
        current = self._snapshot(content_hash="sha256:new")

        result = decide_version_action(previous, current)

        self.assertEqual(result.action, "update")
        self.assertFalse(result.requires_reprocess)

    def test_returns_substitute_for_approved_curated_new_version(self) -> None:
        previous = self._snapshot(
            artifact_type="curated_transcript",
            artifact_id="cur-1",
            version="v1",
            content_hash="sha256:same",
            status="approved",
        )
        current = self._snapshot(
            artifact_type="curated_transcript",
            artifact_id="cur-1",
            version="v2",
            content_hash="sha256:same",
            status="approved",
        )

        result = decide_version_action(previous, current)

        self.assertEqual(result.action, "substitute")

    def test_returns_reconcile_when_metadata_conflict_exists(self) -> None:
        previous = self._snapshot()
        current = self._snapshot()

        result = decide_version_action(previous, current, has_metadata_conflict=True)

        self.assertEqual(result.action, "reconcile")

    def test_returns_invalidate_when_marked_unreliable(self) -> None:
        previous = self._snapshot()
        current = self._snapshot(status="approved")

        result = decide_version_action(previous, current, marked_unreliable=True)

        self.assertEqual(result.action, "invalidate")

    def test_returns_reprocess_when_rule_version_changes(self) -> None:
        previous = self._snapshot()
        current = self._snapshot()

        result = decide_version_action(previous, current, normalization_rule_changed=True)

        self.assertEqual(result.action, "reprocess")
        self.assertTrue(result.requires_reprocess)

    def test_returns_no_change_when_state_is_equivalent(self) -> None:
        previous = self._snapshot()
        current = self._snapshot()

        result = decide_version_action(previous, current)

        self.assertEqual(result.action, "no_change")

    def test_reject_comparison_with_distinct_artifacts(self) -> None:
        previous = self._snapshot(artifact_id="a")
        current = self._snapshot(artifact_id="b")

        with self.assertRaises(ValueError):
            decide_version_action(previous, current)


if __name__ == "__main__":
    unittest.main()
