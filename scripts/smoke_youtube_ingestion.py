#!/usr/bin/env python3
"""Smoke test de ingestao YouTube para o pipeline E2.S4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app_estudo.integrations import (
    SqliteMediaArtifactStore,
    extract_youtube_audio,
    ingest_first_youtube_video_from_source,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa smoke test de ingestao YouTube")
    parser.add_argument("--url", required=True, help="URL completa do video YouTube")
    parser.add_argument("--title", required=True, help="Titulo do video para metadados locais")
    parser.add_argument(
        "--db-path",
        default="data/audit/media_artifacts.db",
        help="Caminho do SQLite de artefatos (padrao: data/audit/media_artifacts.db)",
    )
    parser.add_argument(
        "--languages",
        default="en",
        help="Idiomas preferenciais separados por virgula (padrao: en)",
    )
    parser.add_argument(
        "--extract-audio",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Extrai audio do video para uso em listening (padrao: desabilitado; TTS cuida do audio)",
    )
    parser.add_argument(
        "--audio-output-dir",
        default="data/media/audio",
        help="Diretorio para salvar audio extraido (padrao: data/media/audio)",
    )
    args = parser.parse_args()

    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    store = SqliteMediaArtifactStore(db_path)
    preferred_languages = tuple(lang.strip() for lang in args.languages.split(",") if lang.strip())

    result = ingest_first_youtube_video_from_source(
        youtube_url=args.url,
        title=args.title,
        store=store,
        preferred_languages=preferred_languages,
    )

    audio_result = None
    if args.extract_audio:
        audio_result = extract_youtube_audio(
            youtube_url=args.url,
            output_dir=args.audio_output_dir,
        )

    print(
        json.dumps(
            {
                "source_media_id": result.source_media_id,
                "raw_transcript_id": result.raw_transcript_id,
                "curated_transcript_id": result.curated_transcript_id,
                "study_segments_created": result.study_segments_created,
                "quality_gate_status": result.quality_gate_status,
                "sqlite_path": str(db_path),
                "audio": {
                    "video_id": audio_result.video_id,
                    "title": audio_result.title,
                    "duration_seconds": audio_result.duration_seconds,
                    "audio_file_path": audio_result.audio_file_path,
                }
                if audio_result is not None
                else None,
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
