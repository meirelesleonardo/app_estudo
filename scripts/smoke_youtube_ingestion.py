#!/usr/bin/env python3
"""Smoke test de ingestao YouTube para o pipeline E2.S4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app_estudo.integrations import SqliteMediaArtifactStore, ingest_first_youtube_video_from_source


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

    print(
        json.dumps(
            {
                "source_media_id": result.source_media_id,
                "raw_transcript_id": result.raw_transcript_id,
                "curated_transcript_id": result.curated_transcript_id,
                "study_segments_created": result.study_segments_created,
                "quality_gate_status": result.quality_gate_status,
                "sqlite_path": str(db_path),
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
