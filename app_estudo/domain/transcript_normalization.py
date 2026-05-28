"""Pipeline de normalizacao textual versionada para transcricoes."""

from __future__ import annotations

import re
from dataclasses import dataclass

_CONTRACTION_MAP = {
    "gonna": "going to",
    "wanna": "want to",
    "kinda": "kind of",
    "gotta": "got to",
    "i'm": "i am",
    "it's": "it is",
    "don't": "do not",
    "can't": "cannot",
    "won't": "will not",
    "they're": "they are",
    "we're": "we are",
    "i've": "i have",
    "didn't": "did not",
    "isn't": "is not",
    "that's": "that is",
}
_FILLER_WORDS = {"um", "uh", "erm", "hmm"}

_TIMESTAMP_PATTERN = re.compile(r"\[?\b\d{1,2}:\d{2}(?::\d{2})?(?:[\.,]\d+)?\b\]?")
_NOISE_PATTERN = re.compile(r"\[(?:noise|music|applause|laughter)\]|\((?:noise|music|applause|laughter)\)", re.IGNORECASE)
_SPECIAL_CHAR_PATTERN = re.compile(r"[^\w\s\.,!?':\-]")
_MULTI_SPACE_PATTERN = re.compile(r"\s+")
_SPACE_BEFORE_PUNCT_PATTERN = re.compile(r"\s+([\.,!?;:])")
_DUPLICATE_TOKEN_PATTERN = re.compile(r"\b(\w+)(\s+\1\b)+", re.IGNORECASE)


@dataclass(frozen=True)
class NormalizationResult:
    """Saida normalizada com versao de regra e flags de transformacao."""

    raw_text: str
    normalized_text: str
    normalization_version: str
    transformation_flags: tuple[str, ...]
    incomplete_sentence: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "raw_text": self.raw_text,
            "normalized_text": self.normalized_text,
            "normalization_version": self.normalization_version,
            "transformation_flags": list(self.transformation_flags),
            "incomplete_sentence": self.incomplete_sentence,
        }


def normalize_transcript_text(raw_text: str, normalization_version: str) -> NormalizationResult:
    """Aplica pipeline de normalizacao textual com flags auditaveis."""

    _require_non_empty("raw_text", raw_text)
    _ensure_version_like("normalization_version", normalization_version)

    flags: list[str] = []
    text = raw_text

    text, changed = _remove_timestamps(text)
    if changed:
        flags.append("timestamps_removed")

    text, changed = _expand_contractions(text)
    if changed:
        flags.append("contractions_expanded")

    text, changed = _remove_fillers(text)
    if changed:
        flags.append("fillers_removed")

    text, changed = _remove_noise_markers(text)
    if changed:
        flags.append("noise_markers_removed")

    text, changed = _remove_special_chars(text)
    if changed:
        flags.append("special_chars_removed")

    text, changed = _remove_duplicate_tokens(text)
    if changed:
        flags.append("duplicate_tokens_removed")

    text, changed = _normalize_spaces(text)
    if changed:
        flags.append("whitespace_normalized")

    incomplete_sentence = not text.endswith((".", "!", "?"))
    if incomplete_sentence:
        flags.append("incomplete_sentence_detected")

    return NormalizationResult(
        raw_text=raw_text,
        normalized_text=text,
        normalization_version=normalization_version,
        transformation_flags=tuple(flags),
        incomplete_sentence=incomplete_sentence,
    )


def _remove_timestamps(text: str) -> tuple[str, bool]:
    normalized = _TIMESTAMP_PATTERN.sub(" ", text)
    return normalized, normalized != text


def _expand_contractions(text: str) -> tuple[str, bool]:
    changed = False

    def replace_match(match: re.Match[str]) -> str:
        nonlocal changed
        token = match.group(0)
        replacement = _CONTRACTION_MAP.get(token.lower())
        if replacement is None:
            return token
        changed = True
        return replacement

    pattern = re.compile(r"\b(" + "|".join(map(re.escape, _CONTRACTION_MAP.keys())) + r")\b", re.IGNORECASE)
    normalized = pattern.sub(replace_match, text)
    return normalized, changed


def _remove_fillers(text: str) -> tuple[str, bool]:
    tokens = text.split()
    filtered = [token for token in tokens if token.lower().strip(",.!?:;-") not in _FILLER_WORDS]
    normalized = " ".join(filtered)
    return normalized, normalized != text


def _remove_noise_markers(text: str) -> tuple[str, bool]:
    normalized = _NOISE_PATTERN.sub(" ", text)
    return normalized, normalized != text


def _remove_special_chars(text: str) -> tuple[str, bool]:
    normalized = _SPECIAL_CHAR_PATTERN.sub(" ", text)
    return normalized, normalized != text


def _remove_duplicate_tokens(text: str) -> tuple[str, bool]:
    normalized = _DUPLICATE_TOKEN_PATTERN.sub(r"\1", text)
    return normalized, normalized != text


def _normalize_spaces(text: str) -> tuple[str, bool]:
    normalized = _MULTI_SPACE_PATTERN.sub(" ", text).strip()
    normalized = _SPACE_BEFORE_PUNCT_PATTERN.sub(r"\1", normalized)
    return normalized, normalized != text


def _require_non_empty(field_name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} e obrigatorio")


def _ensure_version_like(field_name: str, value: str) -> None:
    candidate = value.strip().lower()
    if not candidate.startswith("v") or len(candidate) < 2:
        raise ValueError(f"{field_name} deve seguir padrao de versao, ex.: v1")
