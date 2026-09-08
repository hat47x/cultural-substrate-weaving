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

from validate_research_technical_asset_localization import validate_localization  # noqa: E402

CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json"
)
SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchTechnicalAssetLocalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, contract: dict, suite: dict, fragment: str) -> None:
        errors = validate_localization(contract, suite)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_localization_contract_is_valid(self) -> None:
        self.assertEqual(validate_localization(self.contract, self.suite), [])

    def test_contract_never_authorizes_promotion(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["production_promotion_authorized"] = True
        self.assert_has_error(
            contract,
            self.suite,
            "must not authorize production promotion",
        )

    def test_affinity_english_package_requires_localized_representation(self) -> None:
        suite = copy.deepcopy(self.suite)
        skill = next(item for item in suite["skills"] if item["id"] == "affinity-synthesis")
        files = skill["locale_realizations"]["en-US"]["package_source"]["files"]
        files.remove("references/REPRESENTATION.en.md")
        self.assert_has_error(
            self.contract,
            suite,
            "affinity English package source missing localized runtime asset",
        )

    def test_iterative_english_package_requires_localized_round_template(self) -> None:
        suite = copy.deepcopy(self.suite)
        skill = next(
            item for item in suite["skills"] if item["id"] == "iterative-inquiry-synthesis"
        )
        files = skill["locale_realizations"]["en-US"]["package_source"]["files"]
        files.remove("references/ROUND-TEMPLATE.en.md")
        self.assert_has_error(
            self.contract,
            suite,
            "iterative English package source missing localized runtime asset",
        )

    def test_translated_runtime_asset_cannot_be_marked_not_package_required(self) -> None:
        contract = copy.deepcopy(self.contract)
        representation = next(
            item
            for item in contract["assets"]
            if item["role"] == "representation_grammar"
        )
        representation["english_package_required"] = False
        self.assert_has_error(
            contract,
            self.suite,
            "translated runtime technical asset must be package-required",
        )

    def test_language_neutral_schema_may_be_shared(self) -> None:
        schema = next(
            item
            for item in self.contract["assets"]
            if item["role"] == "machine_readable_schema"
        )
        self.assertEqual(schema["localization_status"], "language-neutral-shared")
        self.assertTrue(schema["english_package_required"])


if __name__ == "__main__":
    unittest.main()
