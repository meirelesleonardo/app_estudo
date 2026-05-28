"""Extracao de audio de videos YouTube para apoio ao pipeline de listening."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app_estudo.integrations.youtube_ingestion import extract_youtube_video_id


@dataclass(frozen=True)
class YoutubeAudioExtractionResult:
    """Resumo da extracao de audio de um video YouTube."""

    video_id: str
    title: str
    duration_seconds: int
    audio_file_path: str
    source_url: str


def extract_youtube_audio(
    *,
    youtube_url: str,
    output_dir: str | Path = "data/media/audio",
    file_stem: str | None = None,
) -> YoutubeAudioExtractionResult:
    """Extrai audio do YouTube no melhor stream disponivel."""

    video_id = extract_youtube_video_id(youtube_url)

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    stem = file_stem.strip() if file_stem and file_stem.strip() else video_id
    outtmpl = str(target_dir / f"{stem}.%(ext)s")

    yt_dlp = _load_yt_dlp()
    options = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(options) as client:
        info = client.extract_info(youtube_url, download=True)

    audio_path = _resolve_audio_path(info)

    return YoutubeAudioExtractionResult(
        video_id=video_id,
        title=str(info.get("title", "")),
        duration_seconds=int(info.get("duration") or 0),
        audio_file_path=audio_path,
        source_url=youtube_url,
    )


def _resolve_audio_path(info: dict[str, Any]) -> str:
    requested = info.get("requested_downloads")
    if isinstance(requested, list) and requested:
        candidate = requested[0]
        if isinstance(candidate, dict):
            path = candidate.get("filepath")
            if path:
                return str(path)

    filename = info.get("_filename")
    if filename:
        return str(filename)

    raise RuntimeError("Nao foi possivel resolver o caminho do audio extraido")


def _load_yt_dlp() -> Any:
    try:
        import yt_dlp
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Dependencia ausente: instale 'yt-dlp' para extrair audio do YouTube") from exc

    return yt_dlp
