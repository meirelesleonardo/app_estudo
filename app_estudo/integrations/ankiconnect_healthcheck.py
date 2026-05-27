"""Healthcheck local para validar disponibilidade do AnkiConnect."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib import error, request

DEFAULT_ANKI_ENDPOINT = "http://127.0.0.1:8765"


@dataclass(frozen=True)
class AnkiHealthcheckResult:
    ok: bool
    endpoint: str
    version: int | None
    error_message: str | None


def check_ankiconnect(endpoint: str = DEFAULT_ANKI_ENDPOINT, timeout: float = 2.0) -> AnkiHealthcheckResult:
    """Executa ping version no AnkiConnect e retorna resultado estruturado."""

    payload = {
        "action": "version",
        "version": 6,
        "params": {},
    }

    req = request.Request(
        endpoint,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return AnkiHealthcheckResult(
            ok=False,
            endpoint=endpoint,
            version=None,
            error_message=str(exc),
        )

    if body.get("error") is not None:
        return AnkiHealthcheckResult(
            ok=False,
            endpoint=endpoint,
            version=None,
            error_message=str(body.get("error")),
        )

    version = body.get("result")
    if not isinstance(version, int):
        return AnkiHealthcheckResult(
            ok=False,
            endpoint=endpoint,
            version=None,
            error_message="Resposta sem campo result inteiro",
        )

    return AnkiHealthcheckResult(
        ok=True,
        endpoint=endpoint,
        version=version,
        error_message=None,
    )
