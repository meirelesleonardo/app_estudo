#!/usr/bin/env python3
"""Ingestao em lote de videos YouTube com sincronizacao de cards no Anki."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app_estudo.integrations import (
    AnkiConnectClient,
    SqliteMediaArtifactStore,
    YoutubeTranscriptPayload,
    ingest_youtube_video_and_sync_anki,
)


def _load_batch(batch_file: Path) -> list[dict[str, object]]:
    payload = json.loads(batch_file.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Arquivo de lote deve conter uma lista JSON")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingestao em lote YouTube -> Anki")
    parser.add_argument("--batch-file", default="docs/english/YOUTUBE_STARTER_BATCH.json")
    parser.add_argument("--db-path", default="data/audit/media_artifacts.db")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8765")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--model-name", default="AppEstudoListening")
    parser.add_argument("--languages", default="en")
    parser.add_argument(
        "--extract-audio",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Extrai audio do YouTube para anexar nos cards (padrao: desabilitado; TTS cuida do audio)",
    )
    parser.add_argument("--audio-output-dir", default="data/media/audio")
    parser.add_argument("--min-segment-seconds", type=int, default=10)
    parser.add_argument("--max-segment-seconds", type=int, default=45)
    parser.add_argument("--target-segment-seconds", type=int, default=25)
    args = parser.parse_args()

    batch_file = Path(args.batch_file)
    records = _load_batch(batch_file)

    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    store = SqliteMediaArtifactStore(db_path)
    client = AnkiConnectClient(
        endpoint=args.endpoint,
        timeout=args.timeout,
        model_name=args.model_name,
    )

    preferred_languages = tuple(lang.strip() for lang in args.languages.split(",") if lang.strip())

    summaries: list[dict[str, object]] = []
    for index, record in enumerate(records):
        url = str(record.get("url", "")).strip()
        title = str(record.get("title", "")).strip()
        level = str(record.get("level", "B1")).strip().upper()
        accent = str(record.get("accent", "mixed")).strip().lower()
        phenomenon = str(record.get("phenomenon", "connected_speech")).strip().lower()

        if not url or not title:
            summaries.append(
                {
                    "index": index,
                    "status": "skipped",
                    "reason": "url/title ausentes",
                }
            )
            continue

        transcript_payload = None
        manual_raw_text = str(record.get("raw_text", "")).strip()
        if manual_raw_text:
            duration_seconds = int(record.get("duration_seconds", 60))
            raw_timestamps_value = record.get("raw_timestamps", [])
            raw_timestamps: tuple[str, ...]
            if isinstance(raw_timestamps_value, list):
                raw_timestamps = tuple(str(item) for item in raw_timestamps_value)
            else:
                raw_timestamps = tuple()

            transcript_payload = YoutubeTranscriptPayload(
                title=title,
                duration_seconds=duration_seconds,
                raw_text=manual_raw_text,
                raw_timestamps=raw_timestamps,
                locale=str(record.get("locale", "en")),
                provider=str(record.get("provider", "manual_batch_input")),
            )

        try:
            summary = ingest_youtube_video_and_sync_anki(
                youtube_url=url,
                title=title,
                store=store,
                anki_client=client,
                preferred_languages=preferred_languages,
                level=level,
                accent=accent,
                phenomenon=phenomenon,
                extract_audio_enabled=args.extract_audio,
                audio_output_dir=args.audio_output_dir,
                transcript_payload=transcript_payload,
                min_segment_seconds=args.min_segment_seconds,
                max_segment_seconds=args.max_segment_seconds,
                target_segment_seconds=args.target_segment_seconds,
            )
            summaries.append(
                {
                    "index": index,
                    "url": url,
                    "title": title,
                    "level": level,
                    "quality_gate_status": summary.quality_gate_status,
                    "attempted_notes": summary.attempted_notes,
                    "synced_notes": summary.synced_notes,
                    "updated_notes": summary.updated_notes,
                    "pending_notes": summary.pending_notes,
                    "conflict_notes": summary.conflict_notes,
                    "blocked_notes": summary.blocked_notes,
                    "ingestion_mode": "manual_payload" if transcript_payload is not None else "youtube_provider",
                }
            )
        except Exception as exc:
            summaries.append(
                {
                    "index": index,
                    "url": url,
                    "title": title,
                    "level": level,
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "ingestion_mode": "manual_payload" if transcript_payload is not None else "youtube_provider",
                }
            )

    totals = {
        "videos": len(records),
        "attempted_notes": sum(int(item.get("attempted_notes", 0)) for item in summaries),
        "synced_notes": sum(int(item.get("synced_notes", 0)) for item in summaries),
        "updated_notes": sum(int(item.get("updated_notes", 0)) for item in summaries),
        "pending_notes": sum(int(item.get("pending_notes", 0)) for item in summaries),
        "conflict_notes": sum(int(item.get("conflict_notes", 0)) for item in summaries),
        "blocked_notes": sum(int(item.get("blocked_notes", 0)) for item in summaries),
    }

    print(
        json.dumps(
            {
                "batch_file": str(batch_file),
                "sqlite_path": str(db_path),
                "model_name": args.model_name,
                "summaries": summaries,
                "totals": totals,
            },
            ensure_ascii=True,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
