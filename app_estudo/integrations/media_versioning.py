"""Politica de versionamento e reprocessamento para artefatos de midia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

VersionAction = Literal[
    "no_change",
    "update",
    "substitute",
    "reconcile",
    "invalidate",
    "reprocess",
]


@dataclass(frozen=True)
class ArtifactSnapshot:
    """Estado de um artefato para avaliacao de transicao de versao."""

    artifact_type: str
    artifact_id: str
    version: str
    content_hash: str
    status: str


@dataclass(frozen=True)
class VersionDecision:
    """Resultado de decisao de versionamento com rastreabilidade de motivo."""

    action: VersionAction
    reason: str
    requires_reprocess: bool


def decide_version_action(
    previous: ArtifactSnapshot,
    current: ArtifactSnapshot,
    *,
    has_metadata_conflict: bool = False,
    normalization_rule_changed: bool = False,
    marked_unreliable: bool = False,
) -> VersionDecision:
    """Decide acao de versionamento conforme politica E2.S4."""

    _validate_snapshot_pair(previous, current)

    previous_status = previous.status.strip().lower()
    current_status = current.status.strip().lower()

    if marked_unreliable or current_status in {"rejected", "invalid"}:
        return VersionDecision(
            action="invalidate",
            reason="artefato marcado como nao confiavel",
            requires_reprocess=False,
        )

    if normalization_rule_changed:
        return VersionDecision(
            action="reprocess",
            reason="versao de regra alterada; pipeline deve ser reexecutado",
            requires_reprocess=True,
        )

    if has_metadata_conflict:
        return VersionDecision(
            action="reconcile",
            reason="divergencia de metadados detectada",
            requires_reprocess=False,
        )

    if current.content_hash != previous.content_hash:
        return VersionDecision(
            action="update",
            reason="hash de conteudo alterado",
            requires_reprocess=False,
        )

    if (
        previous.artifact_type == "curated_transcript"
        and current.version != previous.version
        and previous_status == "approved"
        and current_status == "approved"
    ):
        return VersionDecision(
            action="substitute",
            reason="nova versao curada aprovada substitui versao anterior",
            requires_reprocess=False,
        )

    return VersionDecision(
        action="no_change",
        reason="nenhuma mudanca relevante detectada",
        requires_reprocess=False,
    )


def _validate_snapshot_pair(previous: ArtifactSnapshot, current: ArtifactSnapshot) -> None:
    if previous.artifact_type != current.artifact_type:
        raise ValueError("artifact_type deve ser o mesmo para comparacao")

    if previous.artifact_id != current.artifact_id:
        raise ValueError("artifact_id deve ser o mesmo para comparacao")

    _require_non_empty("previous.version", previous.version)
    _require_non_empty("current.version", current.version)
    _require_non_empty("previous.content_hash", previous.content_hash)
    _require_non_empty("current.content_hash", current.content_hash)
    _require_non_empty("previous.status", previous.status)
    _require_non_empty("current.status", current.status)


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")
