from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_research_adapter_metadata as adapter_validator
from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402

SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"


class ResearchAdapterMetadataDistributionAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    def test_declared_future_locale_bundle_distribution_is_validated(self) -> None:
        suite = copy.deepcopy(self.suite)
        metadata = copy.deepcopy(self.metadata)

        suite["distribution_prototypes"]["future_plugin"] = copy.deepcopy(
            suite["distribution_prototypes"]["claude_plugin"]
        )
        metadata["distributions"]["future_plugin"] = copy.deepcopy(
            metadata["distributions"]["claude_plugin"]
        )
        metadata["distributions"]["future_plugin"]["locales"]["en-US"][
            "prototype_source"
        ] = "research/skill-prototypes/DOES-NOT-EXIST.json"

        original_loader = adapter_validator._load_json

        def load_fixture_suite(path, field, errors):
            if path == SUITE_PATH:
                return suite
            return original_loader(path, field, errors)

        with patch.object(adapter_validator, "_load_json", side_effect=load_fixture_suite):
            errors = validate_adapter_metadata(ROOT, metadata)

        self.assertTrue(
            any(
                "future_plugin prototype metadata source is missing" in error
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
