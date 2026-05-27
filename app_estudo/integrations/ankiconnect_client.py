"""Cliente base para sincronizacao com AnkiConnect."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from urllib import error, request

from .anki_mapping import LogicalAnkiNote
from .ankiconnect_healthcheck import DEFAULT_ANKI_ENDPOINT

_ANKI_API_VERSION = 6
_REQUIRED_FIELDS = {
    "source_id",
    "source_type",
    "title",
    "transcript_excerpt",
    "target_expression",
    "explanation_ptbr",
    "listening_context",
    "level",
    "accent",
    "audio_reference",
    "created_from_stage",
}
_MODEL_FIELDS = [
    "source_id",
    "source_type",
    "title",
    "transcript_excerpt",
    "target_expression",
    "explanation_ptbr",
    "listening_context",
    "level",
    "accent",
    "tags_context",
    "audio_reference",
    "created_from_stage",
    "logical_key",
    "evaluation_score",
    "evaluation_classification",
]


class AnkiConnectError(Exception):
    """Erro base de integracao com AnkiConnect."""


class AnkiConnectConnectivityError(AnkiConnectError):
    """Falha de conectividade com endpoint do AnkiConnect."""


class AnkiConnectRemoteError(AnkiConnectError):
    """Erro remoto retornado pelo AnkiConnect."""


class AnkiConnectValidationError(AnkiConnectError):
    """Erro de validacao antes de enviar dados ao AnkiConnect."""


@dataclass(frozen=True)
class AnkiSyncResult:
    """Resultado logico de uma tentativa de sincronizacao."""

    state: str
    action: str
    note_id: int | None
    error_type: str | None
    error_message: str | None


class AnkiConnectClient:
    """Cliente de baixo nivel para operacoes basicas com AnkiConnect."""

    def __init__(
        self,
        endpoint: str = DEFAULT_ANKI_ENDPOINT,
        timeout: float = 3.0,
        model_name: str = "Basic",
    ) -> None:
        self.endpoint = endpoint
        self.timeout = timeout
        self.model_name = model_name

    def version(self) -> int:
        result = self._invoke("version", {})
        if not isinstance(result, int):
            raise AnkiConnectRemoteError("Resposta de version invalida")
        return result

    def sync_logical_note(self, note: LogicalAnkiNote) -> AnkiSyncResult:
        try:
            self._validate_note(note)
            self._ensure_model_exists()
            self._ensure_deck_exists(note.deck_name)
        except AnkiConnectValidationError as exc:
            return AnkiSyncResult(
                state="blocked",
                action="validation",
                note_id=None,
                error_type="validation",
                error_message=str(exc),
            )
        except AnkiConnectConnectivityError as exc:
            return AnkiSyncResult(
                state="pending",
                action="setup_check",
                note_id=None,
                error_type="connectivity",
                error_message=str(exc),
            )
        except AnkiConnectRemoteError as exc:
            return AnkiSyncResult(
                state="blocked",
                action="setup_check",
                note_id=None,
                error_type="remote",
                error_message=str(exc),
            )

        try:
            existing_note_ids = self.find_notes_by_source_id(str(note.fields["source_id"]))
        except AnkiConnectConnectivityError as exc:
            return AnkiSyncResult(
                state="pending",
                action="lookup",
                note_id=None,
                error_type="connectivity",
                error_message=str(exc),
            )
        except AnkiConnectRemoteError as exc:
            return AnkiSyncResult(
                state="blocked",
                action="lookup",
                note_id=None,
                error_type="remote",
                error_message=str(exc),
            )

        if len(existing_note_ids) > 1:
            return AnkiSyncResult(
                state="conflict",
                action="lookup",
                note_id=None,
                error_type="conflict",
                error_message="Mais de uma nota encontrada para o mesmo source_id",
            )

        if len(existing_note_ids) == 1:
            note_id = existing_note_ids[0]
            return self._update_existing_note(note_id, note)

        return self._create_new_note(note)

    def find_notes_by_source_id(self, source_id: str) -> list[int]:
        escaped = source_id.replace('"', r'\"')
        result = self._invoke("findNotes", {"query": f'"source_id:{escaped}"'})

        if not isinstance(result, list) or not all(isinstance(item, int) for item in result):
            raise AnkiConnectRemoteError("findNotes retornou formato invalido")

        return result

    def _create_new_note(self, note: LogicalAnkiNote) -> AnkiSyncResult:
        try:
            note_id = self._add_note(note)
            return AnkiSyncResult(
                state="synced",
                action="created",
                note_id=note_id,
                error_type=None,
                error_message=None,
            )
        except AnkiConnectConnectivityError as exc:
            return AnkiSyncResult(
                state="pending",
                action="created",
                note_id=None,
                error_type="connectivity",
                error_message=str(exc),
            )
        except AnkiConnectRemoteError as exc:
            message = str(exc).lower()
            state = "conflict" if "duplicate" in message else "blocked"
            error_type = "conflict" if state == "conflict" else "remote"
            return AnkiSyncResult(
                state=state,
                action="created",
                note_id=None,
                error_type=error_type,
                error_message=str(exc),
            )

    def _update_existing_note(self, note_id: int, note: LogicalAnkiNote) -> AnkiSyncResult:
        try:
            self._update_note_fields(note_id, note)
            self._add_tags(note_id, note.tags)
            return AnkiSyncResult(
                state="updated",
                action="updated",
                note_id=note_id,
                error_type=None,
                error_message=None,
            )
        except AnkiConnectConnectivityError as exc:
            return AnkiSyncResult(
                state="pending",
                action="updated",
                note_id=note_id,
                error_type="connectivity",
                error_message=str(exc),
            )
        except AnkiConnectRemoteError as exc:
            return AnkiSyncResult(
                state="blocked",
                action="updated",
                note_id=note_id,
                error_type="remote",
                error_message=str(exc),
            )

    def _add_note(self, note: LogicalAnkiNote) -> int:
        result = self._invoke("addNote", {"note": self._build_anki_note_payload(note)})
        if not isinstance(result, int):
            raise AnkiConnectRemoteError("addNote nao retornou id de nota")
        return result

    def _update_note_fields(self, note_id: int, note: LogicalAnkiNote) -> None:
        payload = {
            "note": {
                "id": note_id,
                "fields": self._serialize_fields(note.fields),
            }
        }
        self._invoke("updateNoteFields", payload)

    def _add_tags(self, note_id: int, tags: tuple[str, ...]) -> None:
        if not tags:
            return
        self._invoke(
            "addTags",
            {
                "notes": [note_id],
                "tags": " ".join(tags),
            },
        )

    def _build_anki_note_payload(self, note: LogicalAnkiNote) -> dict[str, object]:
        payload: dict[str, object] = {
            "deckName": note.deck_name,
            "modelName": self.model_name,
            "fields": self._serialize_fields(note.fields),
            "tags": list(note.tags),
        }

        audio = self._build_audio(note)
        if audio:
            payload["audio"] = audio

        return payload

    def _ensure_model_exists(self) -> None:
        model_names = self._invoke("modelNames", {})
        if not isinstance(model_names, list):
            raise AnkiConnectRemoteError("modelNames retornou formato invalido")

        if self.model_name in model_names:
            return

        self._invoke(
            "createModel",
            {
                "modelName": self.model_name,
                "inOrderFields": _MODEL_FIELDS,
                "css": ".card { font-family: arial; font-size: 20px; }",
                "isCloze": False,
                "cardTemplates": [
                    {
                        "Name": "Card 1",
                        "Front": "{{target_expression}}",
                        "Back": "{{FrontSide}}<hr id=answer>{{explanation_ptbr}}<br><br>{{transcript_excerpt}}",
                    }
                ],
            },
        )

    def _ensure_deck_exists(self, deck_name: str) -> None:
        if not deck_name.strip():
            raise AnkiConnectValidationError("deck_name e obrigatorio")

        # createDeck e idempotente no AnkiConnect: cria se nao existir e nao falha se ja existir.
        self._invoke("createDeck", {"deck": deck_name})

    def _build_audio(self, note: LogicalAnkiNote) -> list[dict[str, object]]:
        reference = note.media.get("reference_path_or_url")
        if not isinstance(reference, str) or not reference.strip():
            return []

        source_id = str(note.fields.get("source_id", "audio"))
        filename = f"{_safe_filename(source_id)}.mp3"
        fields = ["audio_reference"]

        if reference.startswith("http://") or reference.startswith("https://"):
            return [{"url": reference, "filename": filename, "fields": fields}]

        return [{"path": reference, "filename": filename, "fields": fields}]

    def _serialize_fields(self, fields: dict[str, object]) -> dict[str, str]:
        serialized: dict[str, str] = {}
        for key, value in fields.items():
            if isinstance(value, (dict, list, tuple)):
                serialized[key] = json.dumps(value, ensure_ascii=True)
            elif value is None:
                serialized[key] = ""
            else:
                serialized[key] = str(value)
        return serialized

    def _validate_note(self, note: LogicalAnkiNote) -> None:
        if not note.deck_name.strip():
            raise AnkiConnectValidationError("deck_name e obrigatorio")

        missing_fields = sorted(_REQUIRED_FIELDS - set(note.fields.keys()))
        if missing_fields:
            raise AnkiConnectValidationError(
                "Campos obrigatorios ausentes em note.fields: " + ", ".join(missing_fields)
            )

        if not note.note_unique_id.strip():
            raise AnkiConnectValidationError("note_unique_id e obrigatorio")

    def _invoke(self, action: str, params: dict[str, object]) -> object:
        payload = {
            "action": action,
            "version": _ANKI_API_VERSION,
            "params": params,
        }

        req = request.Request(
            self.endpoint,
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except (error.URLError, TimeoutError) as exc:
            raise AnkiConnectConnectivityError(str(exc)) from exc
        except json.JSONDecodeError as exc:
            raise AnkiConnectRemoteError("Resposta JSON invalida do AnkiConnect") from exc

        remote_error = body.get("error")
        if remote_error is not None:
            raise AnkiConnectRemoteError(str(remote_error))

        if "result" not in body:
            raise AnkiConnectRemoteError("Resposta sem campo result")

        return body["result"]


def _safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", value)
