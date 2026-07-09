"""Testes para o fluxo de importacao de cards da trilha IA."""

from __future__ import annotations

import importlib
import io
import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

import scripts.import_concurso_cards_to_anki as imp_mod

IA_MODEL = imp_mod.IA_MODEL
IA_SUBDECKS = imp_mod.IA_SUBDECKS


def _mock_response(payload: object) -> io.BytesIO:
    body = json.dumps({"result": payload, "error": None}).encode("utf-8")
    return io.BytesIO(body)


def _csv_line(card_id: str, front: str, back: str, deck: str = "", tags: str = "") -> str:
    return f"{card_id},{front},{back},{deck},{tags}\n"


class EnsureIaModelTests(unittest.TestCase):
    """Criacao idempotente do modelo AppEstudoIA."""

    @patch("urllib.request.urlopen")
    def test_creates_model_when_not_exists(self, mock_urlopen: MagicMock) -> None:
        model_names_resp = _mock_response(["Basic", "AppEstudoConcurso"])
        create_resp = _mock_response({"modelName": IA_MODEL})
        mock_urlopen.side_effect = [model_names_resp, create_resp]

        imp_mod.ensure_ia_model("http://localhost:8765")

        self.assertEqual(mock_urlopen.call_count, 2)
        create_call = json.loads(mock_urlopen.call_args_list[1][0][0].data)
        self.assertEqual(create_call["action"], "createModel")
        self.assertEqual(create_call["params"]["modelName"], IA_MODEL)
        self.assertIn("CardID", create_call["params"]["inOrderFields"])

    @patch("urllib.request.urlopen")
    def test_skips_creation_when_model_already_exists(self, mock_urlopen: MagicMock) -> None:
        model_names_resp = _mock_response(["Basic", IA_MODEL, "AppEstudoConcurso"])
        mock_urlopen.side_effect = [model_names_resp]

        imp_mod.ensure_ia_model("http://localhost:8765")

        mock_urlopen.assert_called_once()


class EnsureIaDeckHierarchyTests(unittest.TestCase):
    """Criacao idempotente da arvore de subdecks IA."""

    @patch("urllib.request.urlopen")
    def test_creates_all_subdecks(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = [_mock_response(None) for _ in range(len(IA_SUBDECKS))]

        imp_mod.ensure_ia_deck_hierarchy("http://localhost:8765")

        self.assertEqual(mock_urlopen.call_count, len(IA_SUBDECKS))
        for i, deck_name in enumerate(IA_SUBDECKS):
            call_data = json.loads(mock_urlopen.call_args_list[i][0][0].data)
            self.assertEqual(call_data["action"], "createDeck")
            self.assertEqual(call_data["params"]["deck"], deck_name)


class FindByCardIdTests(unittest.TestCase):
    """Busca de notas existentes por card_id no deck destino."""

    @patch("urllib.request.urlopen")
    def test_returns_empty_when_no_notes_found(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response([])

        result = imp_mod.find_by_card_id("http://localhost:8765", "IA::01 - Fundamentos", "CARD-IA-001")

        self.assertEqual(result, [])

    @patch("urllib.request.urlopen")
    def test_returns_note_ids_when_found(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response([101])

        result = imp_mod.find_by_card_id("http://localhost:8765", "IA::01 - Fundamentos", "CARD-IA-001")

        self.assertEqual(result, [101])

    @patch("urllib.request.urlopen")
    def test_filters_non_integer_results(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response([101, "invalid", 102])

        result = imp_mod.find_by_card_id("http://localhost:8765", "IA::01 - Fundamentos", "CARD-IA-001")

        self.assertEqual(result, [101, 102])


class ImportIaCardsTests(unittest.TestCase):
    """Importacao completa de cards IA a partir de CSV.

    Estratégia de teste: mockar funções de alto nível
    (ensure_ia_model, ensure_ia_deck_hierarchy, invoke) para
    evitar complexidade de contagem de chamadas no side_effect.
    """

    def setUp(self) -> None:
        self.csv_path = Path("/tmp/test_ia_cards.csv")
        self._create_csv()

    def _create_csv(self) -> None:
        lines = [
            "card_id,front,back,deck,tags\n",
            _csv_line("CARD-IA-001", "O que e LLM?", "Resposta LLM", "IA::01 - Fundamentos", "ia llm"),
            _csv_line("CARD-IA-002", "O que e Prompt?", "Resposta Prompt", "IA::01 - Fundamentos", "ia prompt"),
            _csv_line("", "Sem ID", "Ignorado", "IA::01 - Fundamentos", ""),
        ]
        self.csv_path.write_text("".join(lines), encoding="utf-8")

    def tearDown(self) -> None:
        if self.csv_path.exists():
            self.csv_path.unlink()

    @patch.object(imp_mod, "ensure_ia_model")
    @patch.object(imp_mod, "ensure_ia_deck_hierarchy")
    @patch.object(imp_mod, "invoke")
    def test_imports_new_cards(
        self,
        mock_invoke: MagicMock,
        mock_decks: MagicMock,
        mock_model: MagicMock,
    ) -> None:
        mock_invoke.side_effect = [
            [], 101,    # findNotes + addNote (CARD-IA-001)
            [], 102,    # findNotes + addNote (CARD-IA-002)
        ]

        report = imp_mod.import_ia_cards(
            endpoint="http://localhost:8765",
            csv_path=self.csv_path,
            allow_duplicate=False,
        )

        self.assertEqual(report["mode"], "ia")
        self.assertEqual(report["created"], 2)
        self.assertEqual(report["skipped"], 1)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["model_name"], IA_MODEL)
        mock_model.assert_called_once()
        mock_decks.assert_called_once()

    @patch.object(imp_mod, "ensure_ia_model")
    @patch.object(imp_mod, "ensure_ia_deck_hierarchy")
    @patch.object(imp_mod, "invoke")
    def test_skips_duplicate_card_ids(
        self,
        mock_invoke: MagicMock,
        mock_decks: MagicMock,
        mock_model: MagicMock,
    ) -> None:
        mock_invoke.side_effect = [
            [101],      # findNotes: CARD-IA-001 ja existe (duplicado)
            [], 102,    # findNotes + addNote (CARD-IA-002)
        ]

        report = imp_mod.import_ia_cards(
            endpoint="http://localhost:8765",
            csv_path=self.csv_path,
            allow_duplicate=False,
        )

        self.assertEqual(report["created"], 1)
        self.assertEqual(report["skipped"], 2)
        self.assertEqual(report["created_by_deck"], {"IA::01 - Fundamentos": 1})
        self.assertEqual(report["skipped_by_deck"], {"IA::01 - Fundamentos": 1})

    @patch.object(imp_mod, "ensure_ia_model")
    @patch.object(imp_mod, "ensure_ia_deck_hierarchy")
    @patch.object(imp_mod, "invoke")
    def test_allow_duplicate_ignores_existing_cards(
        self,
        mock_invoke: MagicMock,
        mock_decks: MagicMock,
        mock_model: MagicMock,
    ) -> None:
        mock_invoke.side_effect = [
            101,        # addNote (CARD-IA-001, sem findNotes)
            102,        # addNote (CARD-IA-002, sem findNotes)
        ]

        report = imp_mod.import_ia_cards(
            endpoint="http://localhost:8765",
            csv_path=self.csv_path,
            allow_duplicate=True,
        )

        self.assertEqual(report["created"], 2)
        self.assertEqual(report["skipped"], 1)

    @patch.object(imp_mod, "ensure_ia_model")
    @patch.object(imp_mod, "ensure_ia_deck_hierarchy")
    @patch.object(imp_mod, "invoke")
    def test_reports_errors_on_failure(
        self,
        mock_invoke: MagicMock,
        mock_decks: MagicMock,
        mock_model: MagicMock,
    ) -> None:
        mock_invoke.side_effect = [
            [],                                            # findNotes (CARD-IA-001)
            RuntimeError("Falha na criacao da nota"),       # addNote falha (CARD-IA-001)
            [], 102,                                       # findNotes + addNote (CARD-IA-002)
        ]

        report = imp_mod.import_ia_cards(
            endpoint="http://localhost:8765",
            csv_path=self.csv_path,
            allow_duplicate=False,
        )

        self.assertEqual(report["errors"], [{"card_id": "CARD-IA-001", "error": "Falha na criacao da nota"}])

    @patch.object(imp_mod, "ensure_ia_model")
    @patch.object(imp_mod, "ensure_ia_deck_hierarchy")
    @patch.object(imp_mod, "invoke")
    def test_all_fields_in_note_payload(
        self,
        mock_invoke: MagicMock,
        mock_decks: MagicMock,
        mock_model: MagicMock,
    ) -> None:
        mock_invoke.side_effect = [
            [], 101,    # findNotes + addNote (CARD-IA-001)
            [], 102,    # findNotes + addNote (CARD-IA-002)
        ]

        imp_mod.import_ia_cards(
            endpoint="http://localhost:8765",
            csv_path=self.csv_path,
            allow_duplicate=False,
        )

        # Segunda chamada = addNote do CARD-IA-001 (primeira addNote)
        add_calls = [
            c for c in mock_invoke.call_args_list
            if c.args[1] == "addNote"
        ]
        self.assertEqual(len(add_calls), 2)
        note = add_calls[0].args[2]["note"]
        self.assertEqual(note["deckName"], "IA::01 - Fundamentos")
        self.assertEqual(note["modelName"], IA_MODEL)
        self.assertEqual(note["fields"]["CardID"], "CARD-IA-001")
        self.assertEqual(note["fields"]["Front"], "O que e LLM?")
        self.assertEqual(note["fields"]["Back"], "Resposta LLM")
        self.assertEqual(note["tags"], ["ia", "llm"])
        self.assertEqual(note["options"]["allowDuplicate"], False)

        # Verifica segundo card
        note2 = add_calls[1].args[2]["note"]
        self.assertEqual(note2["fields"]["CardID"], "CARD-IA-002")
        self.assertEqual(note2["fields"]["Front"], "O que e Prompt?")


class InvokeTests(unittest.TestCase):
    """Chamadas de baixo nivel ao AnkiConnect."""

    @patch("urllib.request.urlopen")
    def test_raises_runtime_error_on_connectivity_failure(self, mock_urlopen: MagicMock) -> None:
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Conexao recusada")

        with self.assertRaises(RuntimeError) as ctx:
            imp_mod.invoke("http://localhost:8765", "version", {})

        self.assertIn("Falha de conectividade", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_raises_runtime_error_on_anki_error(self, mock_urlopen: MagicMock) -> None:
        body = json.dumps({"result": None, "error": "deck not found"}).encode("utf-8")
        mock_urlopen.return_value = io.BytesIO(body)

        with self.assertRaises(RuntimeError) as ctx:
            imp_mod.invoke("http://localhost:8765", "createDeck", {"deck": "X"})

        self.assertIn("deck not found", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_returns_result_on_success(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.return_value = _mock_response(42)

        result = imp_mod.invoke("http://localhost:8765", "version", {})

        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
