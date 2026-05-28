"""Persistencia SQLite para artefatos de midia e transcricao."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app_estudo.domain.segmentation import StudySegment
from app_estudo.domain.source_media import SourceMedia, SourceMetadata
from app_estudo.domain.transcript import CuratedTranscript, RawTranscript


class SqliteMediaArtifactStore:
    """Armazena artefatos de E2.S4 com trilha de auditoria em SQLite."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def upsert_source_media(self, source_media: SourceMedia) -> None:
        payload = source_media.to_dict()
        payload_json = _to_json(payload)
        self._execute(
            """
            INSERT INTO source_media (
                source_media_id, source_key, platform, external_id, canonical_url,
                media_type, language, duration_seconds, created_at, captured_at,
                last_seen_at, source_hash, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_media_id) DO UPDATE SET
                source_key=excluded.source_key,
                platform=excluded.platform,
                external_id=excluded.external_id,
                canonical_url=excluded.canonical_url,
                media_type=excluded.media_type,
                language=excluded.language,
                duration_seconds=excluded.duration_seconds,
                created_at=excluded.created_at,
                captured_at=excluded.captured_at,
                last_seen_at=excluded.last_seen_at,
                source_hash=excluded.source_hash,
                payload_json=excluded.payload_json
            """,
            (
                source_media.source_media_id,
                source_media.source_key,
                source_media.platform,
                source_media.external_id,
                source_media.canonical_url,
                source_media.media_type,
                source_media.language,
                source_media.duration_seconds,
                source_media.created_at,
                source_media.captured_at,
                source_media.last_seen_at,
                source_media.source_hash,
                payload_json,
            ),
        )
        self._append_audit_event(
            artifact_type="source_media",
            artifact_id=source_media.source_media_id,
            action="upsert",
            artifact_hash=source_media.source_hash,
            metadata={"source_key": source_media.source_key},
        )

    def upsert_source_metadata(self, source_metadata: SourceMetadata) -> None:
        payload = source_metadata.to_dict()
        payload_json = _to_json(payload)
        derived_hash = _hash_payload(payload)
        self._execute(
            """
            INSERT INTO source_metadata (
                source_metadata_id, source_media_id, subtitle_type,
                transcript_quality, connected_speech_density, noise_level,
                pedagogical_category, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_metadata_id) DO UPDATE SET
                source_media_id=excluded.source_media_id,
                subtitle_type=excluded.subtitle_type,
                transcript_quality=excluded.transcript_quality,
                connected_speech_density=excluded.connected_speech_density,
                noise_level=excluded.noise_level,
                pedagogical_category=excluded.pedagogical_category,
                payload_json=excluded.payload_json
            """,
            (
                source_metadata.source_metadata_id,
                source_metadata.source_media_id,
                source_metadata.subtitle_type,
                source_metadata.transcript_quality,
                source_metadata.connected_speech_density,
                source_metadata.noise_level,
                source_metadata.pedagogical_category,
                payload_json,
            ),
        )
        self._append_audit_event(
            artifact_type="source_metadata",
            artifact_id=source_metadata.source_metadata_id,
            action="upsert",
            artifact_hash=derived_hash,
            metadata={"source_media_id": source_metadata.source_media_id},
        )

    def upsert_raw_transcript(self, raw_transcript: RawTranscript) -> None:
        payload = raw_transcript.to_dict()
        payload_json = _to_json(payload)
        self._execute(
            """
            INSERT INTO raw_transcript (
                raw_transcript_id, source_media_id, provider, locale,
                ingestion_version, content_hash, captured_at, lineage_key,
                payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(raw_transcript_id) DO UPDATE SET
                source_media_id=excluded.source_media_id,
                provider=excluded.provider,
                locale=excluded.locale,
                ingestion_version=excluded.ingestion_version,
                content_hash=excluded.content_hash,
                captured_at=excluded.captured_at,
                lineage_key=excluded.lineage_key,
                payload_json=excluded.payload_json
            """,
            (
                raw_transcript.raw_transcript_id,
                raw_transcript.source_media_id,
                raw_transcript.provider,
                raw_transcript.locale,
                raw_transcript.ingestion_version,
                raw_transcript.content_hash,
                raw_transcript.captured_at,
                raw_transcript.lineage_key,
                payload_json,
            ),
        )
        self._append_audit_event(
            artifact_type="raw_transcript",
            artifact_id=raw_transcript.raw_transcript_id,
            action="upsert",
            artifact_hash=raw_transcript.content_hash,
            metadata={"lineage_key": raw_transcript.lineage_key},
        )

    def upsert_curated_transcript(self, curated_transcript: CuratedTranscript) -> None:
        payload = curated_transcript.to_dict()
        payload_json = _to_json(payload)
        derived_hash = _hash_payload(payload)
        self._execute(
            """
            INSERT INTO curated_transcript (
                curated_transcript_id, source_media_id, raw_transcript_id,
                curation_status, quality_score, curated_version, approved_at,
                lineage_key, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(curated_transcript_id) DO UPDATE SET
                source_media_id=excluded.source_media_id,
                raw_transcript_id=excluded.raw_transcript_id,
                curation_status=excluded.curation_status,
                quality_score=excluded.quality_score,
                curated_version=excluded.curated_version,
                approved_at=excluded.approved_at,
                lineage_key=excluded.lineage_key,
                payload_json=excluded.payload_json
            """,
            (
                curated_transcript.curated_transcript_id,
                curated_transcript.source_media_id,
                curated_transcript.raw_transcript_id,
                curated_transcript.curation_status,
                curated_transcript.quality_score,
                curated_transcript.curated_version,
                curated_transcript.approved_at,
                curated_transcript.lineage_key,
                payload_json,
            ),
        )
        self._append_audit_event(
            artifact_type="curated_transcript",
            artifact_id=curated_transcript.curated_transcript_id,
            action="upsert",
            artifact_hash=derived_hash,
            metadata={"lineage_key": curated_transcript.lineage_key},
        )

    def upsert_study_segments(self, segments: list[StudySegment]) -> None:
        if not segments:
            return

        rows = []
        for segment in segments:
            rows.append(
                (
                    segment.study_segment_id,
                    segment.source_media_id,
                    segment.curated_transcript_id,
                    segment.segment_index,
                    segment.segment_start_ms,
                    segment.segment_end_ms,
                    segment.segment_hash,
                    _to_json(segment.to_dict()),
                )
            )

        with self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO study_segment (
                    study_segment_id, source_media_id, curated_transcript_id,
                    segment_index, segment_start_ms, segment_end_ms,
                    segment_hash, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(study_segment_id) DO UPDATE SET
                    source_media_id=excluded.source_media_id,
                    curated_transcript_id=excluded.curated_transcript_id,
                    segment_index=excluded.segment_index,
                    segment_start_ms=excluded.segment_start_ms,
                    segment_end_ms=excluded.segment_end_ms,
                    segment_hash=excluded.segment_hash,
                    payload_json=excluded.payload_json
                """,
                rows,
            )
            conn.commit()

        for segment in segments:
            self._append_audit_event(
                artifact_type="study_segment",
                artifact_id=segment.study_segment_id,
                action="upsert",
                artifact_hash=segment.segment_hash,
                metadata={
                    "curated_transcript_id": segment.curated_transcript_id,
                    "segment_index": segment.segment_index,
                },
            )

    def get_table_counts(self) -> dict[str, int]:
        tables = [
            "source_media",
            "source_metadata",
            "raw_transcript",
            "curated_transcript",
            "study_segment",
            "audit_event",
        ]
        counts: dict[str, int] = {}
        with self._connect() as conn:
            for table in tables:
                counts[table] = conn.execute(f"SELECT COUNT(1) FROM {table}").fetchone()[0]
        return counts

    def query_audit_events(
        self,
        artifact_type: str | None = None,
        artifact_id: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        query = "SELECT occurred_at, artifact_type, artifact_id, action, artifact_hash, metadata_json FROM audit_event"
        where: list[str] = []
        params: list[Any] = []

        if artifact_type is not None:
            where.append("artifact_type = ?")
            params.append(artifact_type)
        if artifact_id is not None:
            where.append("artifact_id = ?")
            params.append(artifact_id)

        if where:
            query += " WHERE " + " AND ".join(where)

        query += " ORDER BY id ASC"

        if limit is not None and limit >= 0:
            query += " LIMIT ?"
            params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()

        result: list[dict[str, Any]] = []
        for row in rows:
            result.append(
                {
                    "occurred_at": row[0],
                    "artifact_type": row[1],
                    "artifact_id": row[2],
                    "action": row[3],
                    "artifact_hash": row[4],
                    "metadata": json.loads(row[5]),
                }
            )
        return result

    def _append_audit_event(
        self,
        *,
        artifact_type: str,
        artifact_id: str,
        action: str,
        artifact_hash: str,
        metadata: dict[str, Any],
    ) -> None:
        occurred_at = datetime.now(timezone.utc).isoformat()
        self._execute(
            """
            INSERT INTO audit_event (
                occurred_at, artifact_type, artifact_id, action, artifact_hash, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                occurred_at,
                artifact_type,
                artifact_id,
                action,
                artifact_hash,
                _to_json(metadata),
            ),
        )

    def _execute(self, sql: str, params: tuple[Any, ...]) -> None:
        with self._connect() as conn:
            conn.execute(sql, params)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS source_media (
                    source_media_id TEXT PRIMARY KEY,
                    source_key TEXT NOT NULL UNIQUE,
                    platform TEXT NOT NULL,
                    external_id TEXT NOT NULL,
                    canonical_url TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    language TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    captured_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    source_hash TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS source_metadata (
                    source_metadata_id TEXT PRIMARY KEY,
                    source_media_id TEXT NOT NULL,
                    subtitle_type TEXT NOT NULL,
                    transcript_quality REAL NOT NULL,
                    connected_speech_density REAL NOT NULL,
                    noise_level REAL NOT NULL,
                    pedagogical_category TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(source_media_id) REFERENCES source_media(source_media_id)
                );

                CREATE TABLE IF NOT EXISTS raw_transcript (
                    raw_transcript_id TEXT PRIMARY KEY,
                    source_media_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    ingestion_version TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    captured_at TEXT NOT NULL,
                    lineage_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(source_media_id) REFERENCES source_media(source_media_id)
                );

                CREATE TABLE IF NOT EXISTS curated_transcript (
                    curated_transcript_id TEXT PRIMARY KEY,
                    source_media_id TEXT NOT NULL,
                    raw_transcript_id TEXT NOT NULL,
                    curation_status TEXT NOT NULL,
                    quality_score REAL NOT NULL,
                    curated_version TEXT NOT NULL,
                    approved_at TEXT,
                    lineage_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(source_media_id) REFERENCES source_media(source_media_id),
                    FOREIGN KEY(raw_transcript_id) REFERENCES raw_transcript(raw_transcript_id)
                );

                CREATE TABLE IF NOT EXISTS study_segment (
                    study_segment_id TEXT PRIMARY KEY,
                    source_media_id TEXT NOT NULL,
                    curated_transcript_id TEXT NOT NULL,
                    segment_index INTEGER NOT NULL,
                    segment_start_ms INTEGER NOT NULL,
                    segment_end_ms INTEGER NOT NULL,
                    segment_hash TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(source_media_id) REFERENCES source_media(source_media_id),
                    FOREIGN KEY(curated_transcript_id) REFERENCES curated_transcript(curated_transcript_id)
                );

                CREATE TABLE IF NOT EXISTS audit_event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    occurred_at TEXT NOT NULL,
                    artifact_type TEXT NOT NULL,
                    artifact_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    artifact_hash TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                );
                """
            )
            conn.commit()


def _to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, sort_keys=True)


def _hash_payload(payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_to_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
