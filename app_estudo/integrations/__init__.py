"""Integracoes logicas e adaptadores externos do projeto."""

from .ankiconnect_healthcheck import AnkiHealthcheckResult, check_ankiconnect
from .anki_mapping import LogicalAnkiNote, map_to_anki_logical_note
from .ankiconnect_client import AnkiConnectClient, AnkiSyncResult
from .anki_reconciliation import DuplicateGroup, ReconciliationReport, build_duplicate_groups

__all__ = [
	"LogicalAnkiNote",
	"map_to_anki_logical_note",
	"AnkiHealthcheckResult",
	"check_ankiconnect",
	"AnkiConnectClient",
	"AnkiSyncResult",
	"DuplicateGroup",
	"ReconciliationReport",
	"build_duplicate_groups",
]
