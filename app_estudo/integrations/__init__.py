"""Integracoes logicas e adaptadores externos do projeto."""

from .ankiconnect_healthcheck import AnkiHealthcheckResult, check_ankiconnect
from .anki_mapping import LogicalAnkiNote, map_to_anki_logical_note
from .ankiconnect_client import AnkiConnectClient, AnkiSyncResult
from .anki_reconciliation import DuplicateGroup, ReconciliationReport, build_duplicate_groups
from .item_history import ItemHistoryEvent, JsonlItemHistoryStore, new_event
from .pilot_validation import validate_pilot_notes
from .pilot_backfill import plan_backfill_updates

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
	"ItemHistoryEvent",
	"JsonlItemHistoryStore",
	"new_event",
	"validate_pilot_notes",
	"plan_backfill_updates",
]
