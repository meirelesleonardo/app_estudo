"""Gate de qualidade para entrada de segmentos no fluxo E4."""

from __future__ import annotations

from dataclasses import dataclass

from app_estudo.domain.segmentation import StudySegment
from app_estudo.domain.source_media import SourceMetadata
from app_estudo.domain.transcript import CuratedTranscript
from app_estudo.integrations.media_versioning import VersionDecision


@dataclass(frozen=True)
class QualityGateResult:
    """Resultado do gate de qualidade para elegibilidade no fluxo E4."""

    status: str
    reasons: tuple[str, ...]
    checklist: dict[str, bool]

    @property
    def approved(self) -> bool:
        return self.status == "approved"

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "approved": self.approved,
            "reasons": list(self.reasons),
            "checklist": dict(self.checklist),
        }


def evaluate_e4_quality_gate(
    *,
    source_metadata: SourceMetadata,
    curated_transcript: CuratedTranscript,
    segments: list[StudySegment],
    version_decision: VersionDecision | None = None,
    min_transcript_quality: float = 0.7,
    max_noise_level: float = 0.4,
    min_segment_count: int = 1,
) -> QualityGateResult:
    """Avalia se um artefato curado pode entrar no fluxo E4."""

    if min_segment_count < 1:
        raise ValueError("min_segment_count deve ser >= 1")

    reasons: list[str] = []

    checklist = {
        "curated_status_approved": curated_transcript.curation_status == "approved",
        "transcript_quality_threshold": source_metadata.transcript_quality >= min_transcript_quality,
        "noise_level_threshold": source_metadata.noise_level <= max_noise_level,
        "segment_count_threshold": len(segments) >= min_segment_count,
        "segment_source_consistency": _segments_match_source(segments, curated_transcript.source_media_id),
        "segment_curated_consistency": _segments_match_curated(segments, curated_transcript.curated_transcript_id),
        "version_policy_allows_entry": _version_allows_entry(version_decision),
    }

    if not checklist["curated_status_approved"]:
        reasons.append("curated_transcript deve estar com status approved")

    if not checklist["transcript_quality_threshold"]:
        reasons.append("transcript_quality abaixo do limiar minimo")

    if not checklist["noise_level_threshold"]:
        reasons.append("noise_level acima do limite operacional")

    if not checklist["segment_count_threshold"]:
        reasons.append("quantidade de segmentos insuficiente")

    if not checklist["segment_source_consistency"]:
        reasons.append("segmentos com source_media_id inconsistente")

    if not checklist["segment_curated_consistency"]:
        reasons.append("segmentos com curated_transcript_id inconsistente")

    if not checklist["version_policy_allows_entry"]:
        reasons.append("politica de versionamento bloqueia entrada no fluxo E4")

    status = "approved" if not reasons else "rejected"
    return QualityGateResult(status=status, reasons=tuple(reasons), checklist=checklist)


def _segments_match_source(segments: list[StudySegment], source_media_id: str) -> bool:
    return all(segment.source_media_id == source_media_id for segment in segments)


def _segments_match_curated(segments: list[StudySegment], curated_transcript_id: str) -> bool:
    return all(segment.curated_transcript_id == curated_transcript_id for segment in segments)


def _version_allows_entry(version_decision: VersionDecision | None) -> bool:
    if version_decision is None:
        return True
    return version_decision.action not in {"invalidate", "reprocess"}
