"""Entidades e estrategia de segmentacao pedagogica."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class StudySegment:
    """Representa um recorte pedagogico derivado de transcript curado."""

    study_segment_id: str
    curated_transcript_id: str
    source_media_id: str
    segment_index: int
    segment_start_ms: int
    segment_end_ms: int
    segment_text: str
    pedagogical_unit: str
    difficulty_band: str
    segment_hash: str

    def __post_init__(self) -> None:
        _require_non_empty("study_segment_id", self.study_segment_id)
        _require_non_empty("curated_transcript_id", self.curated_transcript_id)
        _require_non_empty("source_media_id", self.source_media_id)
        _require_non_empty("segment_text", self.segment_text)
        _require_non_empty("pedagogical_unit", self.pedagogical_unit)
        _require_non_empty("difficulty_band", self.difficulty_band)
        _require_non_empty("segment_hash", self.segment_hash)

        if self.segment_index < 0:
            raise ValueError("segment_index deve ser >= 0")

        if self.segment_start_ms < 0:
            raise ValueError("segment_start_ms deve ser >= 0")

        if self.segment_end_ms <= self.segment_start_ms:
            raise ValueError("segment_end_ms deve ser maior que segment_start_ms")

        duration_ms = self.segment_end_ms - self.segment_start_ms
        if duration_ms < 10000 or duration_ms > 45000:
            raise ValueError("duracao de segmento deve estar entre 10s e 45s")

    def to_dict(self) -> dict[str, object]:
        return {
            "study_segment_id": self.study_segment_id,
            "curated_transcript_id": self.curated_transcript_id,
            "source_media_id": self.source_media_id,
            "segment_index": self.segment_index,
            "segment_start_ms": self.segment_start_ms,
            "segment_end_ms": self.segment_end_ms,
            "segment_text": self.segment_text,
            "pedagogical_unit": self.pedagogical_unit,
            "difficulty_band": self.difficulty_band,
            "segment_hash": self.segment_hash,
        }


def segment_curated_transcript(
    *,
    curated_transcript_id: str,
    source_media_id: str,
    curated_text: str,
    total_duration_seconds: int,
    pedagogical_unit: str,
    difficulty_band: str,
    min_segment_seconds: int = 10,
    max_segment_seconds: int = 45,
    target_segment_seconds: int = 25,
) -> list[StudySegment]:
    """Segmenta transcript curado em recortes pedagogicos deterministas."""

    _require_non_empty("curated_transcript_id", curated_transcript_id)
    _require_non_empty("source_media_id", source_media_id)
    _require_non_empty("curated_text", curated_text)
    _require_non_empty("pedagogical_unit", pedagogical_unit)
    _require_non_empty("difficulty_band", difficulty_band)

    if total_duration_seconds <= 0:
        raise ValueError("total_duration_seconds deve ser maior que zero")

    if not (0 < min_segment_seconds <= target_segment_seconds <= max_segment_seconds):
        raise ValueError("intervalo de segmentacao invalido")

    sentences = _split_sentences(curated_text)
    if not sentences:
        raise ValueError("curated_text deve conter ao menos uma sentenca")

    groups: list[list[str]] = []
    current_group: list[str] = []
    current_chars = 0
    total_chars = sum(len(sentence) for sentence in sentences)
    total_ms = total_duration_seconds * 1000
    target_ms = target_segment_seconds * 1000

    for sentence in sentences:
        projected_chars = current_chars + len(sentence)
        projected_ms = int((projected_chars / total_chars) * total_ms)

        if current_group and projected_ms > target_ms:
            groups.append(current_group)
            current_group = [sentence]
            current_chars = len(sentence)
            continue

        current_group.append(sentence)
        current_chars = projected_chars

    if current_group:
        groups.append(current_group)

    normalized_groups = _rebalance_groups(groups, total_ms, total_chars, min_segment_seconds, max_segment_seconds)

    segments: list[StudySegment] = []
    current_start_ms = 0

    for index, group in enumerate(normalized_groups):
        text = " ".join(group).strip()
        group_chars = sum(len(sentence) for sentence in group)
        if index == len(normalized_groups) - 1:
            end_ms = total_ms
        else:
            duration_ms = int((group_chars / total_chars) * total_ms)
            end_ms = current_start_ms + duration_ms

        end_ms = _clamp_end(end_ms, current_start_ms, min_segment_seconds * 1000, max_segment_seconds * 1000)

        segment_hash = _segment_hash(curated_transcript_id, index, text)
        segment = StudySegment(
            study_segment_id=f"seg-{curated_transcript_id}-{index:03d}",
            curated_transcript_id=curated_transcript_id,
            source_media_id=source_media_id,
            segment_index=index,
            segment_start_ms=current_start_ms,
            segment_end_ms=end_ms,
            segment_text=text,
            pedagogical_unit=pedagogical_unit,
            difficulty_band=difficulty_band,
            segment_hash=segment_hash,
        )
        segments.append(segment)
        current_start_ms = end_ms

    return segments


def _split_sentences(curated_text: str) -> list[str]:
    chunks = [sentence.strip() for sentence in _SENTENCE_SPLIT_PATTERN.split(curated_text.strip()) if sentence.strip()]
    return chunks


def _rebalance_groups(
    groups: list[list[str]],
    total_ms: int,
    total_chars: int,
    min_segment_seconds: int,
    max_segment_seconds: int,
) -> list[list[str]]:
    min_ms = min_segment_seconds * 1000
    max_ms = max_segment_seconds * 1000

    rebalanced: list[list[str]] = []
    buffer_group: list[str] = []

    for group in groups:
        candidate = buffer_group + group
        candidate_chars = sum(len(sentence) for sentence in candidate)
        candidate_ms = int((candidate_chars / total_chars) * total_ms)

        if candidate_ms < min_ms and not rebalanced:
            buffer_group = candidate
            continue

        if candidate_ms > max_ms and buffer_group:
            rebalanced.append(buffer_group)
            buffer_group = group
            continue

        buffer_group = candidate
        if candidate_ms >= min_ms:
            rebalanced.append(buffer_group)
            buffer_group = []

    if buffer_group:
        if rebalanced:
            rebalanced[-1].extend(buffer_group)
        else:
            rebalanced.append(buffer_group)

    return rebalanced


def _segment_hash(curated_transcript_id: str, segment_index: int, segment_text: str) -> str:
    payload = f"{curated_transcript_id}|{segment_index}|{segment_text.strip().lower()}"
    return "sha1:" + hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _clamp_end(end_ms: int, start_ms: int, min_ms: int, max_ms: int) -> int:
    duration = end_ms - start_ms
    if duration < min_ms:
        return start_ms + min_ms
    if duration > max_ms:
        return start_ms + max_ms
    return end_ms


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")
