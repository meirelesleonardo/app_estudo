"""Matriz de avaliacao de listening com score ponderado."""

from __future__ import annotations

from dataclasses import dataclass

from .study_item import CuratedStudyItem

CRITERION_WEIGHTS: dict[str, int] = {
    "audio_clarity": 20,
    "speech_speed": 15,
    "connected_speech_presence": 20,
    "subtitle_transcript_quality": 20,
    "context_naturalness": 15,
    "pedagogical_reusability": 10,
}


@dataclass(frozen=True)
class ListeningEvaluation:
    """Representa o resultado da avaliacao de listening de um item."""

    item_logical_key: str
    score_final: float
    classification: str
    criteria_scores: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "item_logical_key": self.item_logical_key,
            "score_final": self.score_final,
            "classification": self.classification,
            "criteria_scores": dict(self.criteria_scores),
            "weights": dict(CRITERION_WEIGHTS),
        }


def evaluate_listening_item(
    item: CuratedStudyItem, criteria_scores: dict[str, float]
) -> ListeningEvaluation:
    """Aplica a matriz de listening ao item e retorna score + classificacao."""

    _validate_criteria(criteria_scores)

    weighted_sum = 0.0
    for criterion, weight in CRITERION_WEIGHTS.items():
        weighted_sum += criteria_scores[criterion] * weight

    score_final = round(weighted_sum / 100, 2)
    classification = _classify_score(score_final)

    return ListeningEvaluation(
        item_logical_key=item.logical_key,
        score_final=score_final,
        classification=classification,
        criteria_scores=dict(criteria_scores),
    )


def _validate_criteria(criteria_scores: dict[str, float]) -> None:
    if set(criteria_scores.keys()) != set(CRITERION_WEIGHTS.keys()):
        missing = sorted(set(CRITERION_WEIGHTS.keys()) - set(criteria_scores.keys()))
        extra = sorted(set(criteria_scores.keys()) - set(CRITERION_WEIGHTS.keys()))
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        raise ValueError("criteria_scores invalido: " + ", ".join(details))

    for criterion, value in criteria_scores.items():
        if value < 0 or value > 5:
            raise ValueError(
                f"nota invalida para {criterion!r}: {value}. Use valores entre 0 e 5"
            )


def _classify_score(score_final: float) -> str:
    if score_final >= 4.0:
        return "recommended"
    if score_final >= 3.0:
        return "recommended_with_reservations"
    return "not_recommended"
