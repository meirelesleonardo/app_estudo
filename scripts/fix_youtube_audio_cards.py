#!/usr/bin/env python3
"""Corrige audio de cards YouTube ja criados no Anki."""

from __future__ import annotations

import argparse
import base64
import json
import time
from pathlib import Path
import re
import sys
from urllib import error, request

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app_estudo.integrations.youtube_audio_extraction import extract_youtube_audio

ENDPOINT = "http://127.0.0.1:8765"
MODEL_NAME = "AppEstudoListening"

_SOURCE_ID_RE = re.compile(r"^src-yt-([^:]+):")


def invoke(
    action: str,
    params: dict | None = None,
    *,
    timeout_seconds: float = 120.0,
    retries: int = 3,
    retry_delay_seconds: float = 1.5,
) -> object:
    if params is None:
        params = {}

    payload = {
        "action": action,
        "version": 6,
        "params": params,
    }

    req = request.Request(
        ENDPOINT,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with request.urlopen(req, timeout=timeout_seconds) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            break
        except (TimeoutError, error.URLError) as exc:
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep(retry_delay_seconds)
    else:  # pragma: no cover
        raise RuntimeError(f"Falha ao invocar AnkiConnect: {last_error}")

    if body.get("error") is not None:
        raise RuntimeError(str(body["error"]))

    return body.get("result")


def extract_video_id(source_id: str) -> str | None:
    match = _SOURCE_ID_RE.match(source_id.strip())
    if not match:
        return None
    return match.group(1)


def ensure_model_template_has_audio(model_name: str, apply: bool) -> dict[str, object]:
    templates = invoke("modelTemplates", {"modelName": model_name})
    if not isinstance(templates, dict):
        raise RuntimeError("modelTemplates retornou formato invalido")

    changed_templates = 0
    updated_templates: dict[str, dict[str, str]] = {}

    for template_name, template_payload in templates.items():
        if not isinstance(template_payload, dict):
            continue

        front = str(template_payload.get("Front", ""))
        back = str(template_payload.get("Back", ""))

        if "{{audio_reference}}" in front or "{{audio_reference}}" in back:
            updated_templates[template_name] = {
                "Front": front,
                "Back": back,
            }
            continue

        new_front = "{{audio_reference}}<br><br>" + front
        updated_templates[template_name] = {
            "Front": new_front,
            "Back": back,
        }
        changed_templates += 1

    if apply and changed_templates > 0:
        invoke(
            "updateModelTemplates",
            {
                "model": {
                    "name": model_name,
                    "templates": updated_templates,
                }
            },
        )

    return {
        "model_name": model_name,
        "templates_total": len(updated_templates),
        "templates_changed": changed_templates,
        "apply": apply,
    }


def load_notes_from_deck(deck_name: str) -> list[dict[str, object]]:
    cards = invoke("findCards", {"query": f"deck:{deck_name}"})
    if not isinstance(cards, list) or not all(isinstance(card_id, int) for card_id in cards):
        raise RuntimeError("findCards retornou formato invalido")

    cards_info = invoke("cardsInfo", {"cards": cards}) if cards else []
    if not isinstance(cards_info, list):
        raise RuntimeError("cardsInfo retornou formato invalido")

    note_ids = sorted(
        {
            card.get("note")
            for card in cards_info
            if isinstance(card, dict) and isinstance(card.get("note"), int)
        }
    )

    notes_info = invoke("notesInfo", {"notes": note_ids}) if note_ids else []
    if not isinstance(notes_info, list):
        raise RuntimeError("notesInfo retornou formato invalido")

    return notes_info


def main() -> int:
    parser = argparse.ArgumentParser(description="Corrige audio de cards YouTube no Anki")
    parser.add_argument("--deck", default="Ingles::Listening::B1")
    parser.add_argument("--model-name", default=MODEL_NAME)
    parser.add_argument("--audio-output-dir", default="data/media/audio")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    template_report = ensure_model_template_has_audio(args.model_name, apply=args.apply)

    notes = load_notes_from_deck(args.deck)

    youtube_notes: list[dict[str, object]] = []
    video_id_by_note_id: dict[int, str] = {}

    for note in notes:
        note_id = note.get("noteId")
        if not isinstance(note_id, int):
            continue

        fields = note.get("fields")
        if not isinstance(fields, dict):
            continue

        source_raw = fields.get("source_id")
        if not isinstance(source_raw, dict):
            continue

        source_id = str(source_raw.get("value", "")).strip()
        video_id = extract_video_id(source_id)
        if video_id is None:
            continue

        youtube_notes.append(note)
        video_id_by_note_id[note_id] = video_id

    unique_video_ids = sorted(set(video_id_by_note_id.values()))

    extracted_audio: dict[str, dict[str, str]] = {}
    for video_id in unique_video_ids:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        if args.apply:
            result = extract_youtube_audio(
                youtube_url=youtube_url,
                output_dir=args.audio_output_dir,
                file_stem=video_id,
            )
            extracted_audio[video_id] = {
                "audio_file_path": result.audio_file_path,
                "audio_filename": Path(result.audio_file_path).name,
            }
        else:
            extracted_audio[video_id] = {
                "audio_file_path": str(Path(args.audio_output_dir) / f"{video_id}.m4a"),
                "audio_filename": f"{video_id}.m4a",
            }

    stored_media = 0
    updated_notes = 0

    if args.apply:
        for video_id, payload in extracted_audio.items():
            audio_path = Path(payload["audio_file_path"])
            audio_filename = payload["audio_filename"]

            file_bytes = audio_path.read_bytes()
            invoke(
                "storeMediaFile",
                {
                    "filename": audio_filename,
                    "data": base64.b64encode(file_bytes).decode("ascii"),
                },
                timeout_seconds=300.0,
                retries=4,
                retry_delay_seconds=2.0,
            )
            stored_media += 1

        for note in youtube_notes:
            note_id = note.get("noteId")
            if not isinstance(note_id, int):
                continue

            video_id = video_id_by_note_id[note_id]
            audio_filename = extracted_audio[video_id]["audio_filename"]

            invoke(
                "updateNoteFields",
                {
                    "note": {
                        "id": note_id,
                        "fields": {
                            "audio_reference": f"[sound:{audio_filename}]",
                        },
                    }
                },
            )
            invoke(
                "removeTags",
                {
                    "notes": [note_id],
                    "tags": "status:pending_audio_reference",
                },
            )
            invoke(
                "addTags",
                {
                    "notes": [note_id],
                    "tags": "status:audio_ready origem:youtube",
                },
            )
            updated_notes += 1

    print(
        json.dumps(
            {
                "deck": args.deck,
                "model": template_report,
                "youtube_notes_found": len(youtube_notes),
                "unique_videos_found": len(unique_video_ids),
                "stored_media": stored_media,
                "updated_notes": updated_notes,
                "apply": args.apply,
            },
            ensure_ascii=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
