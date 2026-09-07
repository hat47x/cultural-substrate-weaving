from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_translation_refresh_state import (  # noqa: E402
    validate_translation_refresh_state,
)

STATUS_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"
)
MANIFEST_PATH = ROOT / "i18n" / "translation-manifest.json"


class ResearchTranslationRefreshStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def errors(self, status: dict | None = None, manifest: dict | None = None) -> list[str]:
        return validate_translation_refresh_state(
            ROOT,
            self.status if status is None else status,
            self.manifest if manifest is None else manifest,
        )

    def assert_has_error(self, status: dict, fragment: str) -> None:
        errors = self.errors(status=status)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_pending_refresh_state_is_valid(self) -> None:
        self.assertEqual(self.errors(), [])
        self.assertEqual(
            set(self.status["scope_files"]),
            set(self.status["expected_stale_files"]),
        )

    def test_pending_scope_cannot_hide_a_stale_file(self) -> None:
        status = copy.deepcopy(self.status)
        status["expected_stale_files"].remove("governance/evaluation.md")
        self.assert_has_error(status, "must mark the complete semantic-edit scope stale")
        self.assert_has_error(status, "undeclared stale files")

    def test_pending_scope_cannot_claim_an_unchanged_file_is_stale(self) -> None:
        status = copy.deepcopy(self.status)
        extra = "core/activation.md"
        status["scope_files"].append(extra)
        status["expected_stale_files"].append(extra)
        status["english_markers"][extra] = ["#"]
        self.assert_has_error(status, "already synchronized or did not change")

    def test_english_marker_must_exist_in_translated_file(self) -> None:
        status = copy.deepcopy(self.status)
        status["english_markers"]["ROUTER.md"].append(
            "THIS MARKER MUST NOT EXIST IN THE RUNTIME"
        )
        self.assert_has_error(status, "English translation missing declared tension marker")

    def test_semantic_scope_keeps_english_markers_after_refresh(self) -> None:
        status = copy.deepcopy(self.status)
        status["english_markers"].pop("ROUTER.md")
        self.assert_has_error(status, "english_markers must cover exactly scope_files")

    def test_pending_state_cannot_authorize_production(self) -> None:
        status = copy.deepcopy(self.status)
        status["production_promotion_authorized"] = True
        self.assert_has_error(status, "must not authorize production promotion")

    def test_synchronized_state_cannot_keep_expected_stale_files(self) -> None:
        status = copy.deepcopy(self.status)
        status["status"] = "synchronized"
        self.assert_has_error(status, "must have no expected_stale_files")

    def test_refresh_command_cannot_be_replaced_by_manual_hash_edit(self) -> None:
        status = copy.deepcopy(self.status)
        status["refresh_command"] = "edit i18n/translation-manifest.json by hand"
        self.assert_has_error(status, "refresh command must remain make update-en-hashes")

    def test_synchronization_command_is_explicit(self) -> None:
        status = copy.deepcopy(self.status)
        status["synchronization_command"] = "edit status JSON manually"
        self.assert_has_error(status, "translation synchronization command has drifted")


if __name__ == "__main__":
    unittest.main()
