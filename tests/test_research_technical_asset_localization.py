from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_technical_asset_localization import (  # noqa: E402
    _file,
    main as technical_localization_main,
    validate_localization,
)

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

    def test_validator_rejects_non_object_authority_roots_without_crashing(self) -> None:
        self.assertEqual(
            validate_localization([], self.suite),
            ["technical localization contract must be an object"],
        )
        self.assertEqual(
            validate_localization(self.contract, []),
            ["research skill suite must be an object"],
        )

    def test_asset_file_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()
            outside = base / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            link = root / "asset.md"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            self.assertIsNone(_file("asset.md", root=root))

    def test_malformed_locale_realization_does_not_crash(self) -> None:
        suite = copy.deepcopy(self.suite)
        skill = next(
            item for item in suite["skills"] if item["id"] == "affinity-synthesis"
        )
        skill["locale_realizations"] = None
        errors = validate_localization(self.contract, suite)
        self.assertTrue(
            any(
                "technical localization package authority is missing realized en-US sibling"
                in error
                for error in errors
            ),
            errors,
        )

    def test_cli_catches_non_object_json_root(self) -> None:
        with patch(
            "validate_research_technical_asset_localization.json.loads",
            side_effect=[[], self.suite],
        ):
            self.assertEqual(technical_localization_main(), 1)

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

    def test_future_non_markdown_package_asset_requires_contract_classification(self) -> None:
        suite = copy.deepcopy(self.suite)
        skill = next(item for item in suite["skills"] if item["id"] == "affinity-synthesis")
        files = skill["locale_realizations"]["en-US"]["package_source"]["files"]
        files.append("references/FUTURE.schema.json")
        self.assert_has_error(
            self.contract,
            suite,
            "English package non-Markdown asset is not classified by technical localization contract",
        )


if __name__ == "__main__":
    unittest.main()
