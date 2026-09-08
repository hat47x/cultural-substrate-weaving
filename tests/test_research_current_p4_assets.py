from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_current_p4_assets import (  # noqa: E402
    current_p4_authority_paths,
    validate_current_p4_assets,
)

MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
DESCRIPTOR_PATH = (
    ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


class ResearchCurrentP4AssetsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(
        self,
        manifest: dict,
        descriptor: dict,
        fragment: str,
        *,
        root: Path = ROOT,
    ) -> None:
        errors = validate_current_p4_assets(root, manifest, descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_descriptor_authorities_are_registered(self) -> None:
        self.assertEqual(validate_current_p4_assets(ROOT, self.manifest, self.descriptor), [])
        assets = set(self.manifest["suite_research_assets"])
        for relative in current_p4_authority_paths(self.descriptor):
            self.assertIn(relative, assets)

    def test_current_complete_checkout_binding_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        binding = self.descriptor["complete_checkout_validation"]["binding_contract"]
        manifest["suite_research_assets"].remove(binding)
        self.assert_has_error(manifest, self.descriptor, "not registered", root=ROOT)

    def test_current_complete_checkout_status_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        evidence = self.descriptor["complete_checkout_validation"]["evidence"]
        manifest["suite_research_assets"].remove(evidence)
        self.assert_has_error(manifest, self.descriptor, "not registered", root=ROOT)

    def test_current_english_review_packet_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        packet = self.descriptor["english_independent_review"]["packet"]
        manifest["suite_research_assets"].remove(packet)
        self.assert_has_error(manifest, self.descriptor, "not registered", root=ROOT)

    def test_current_english_review_targets_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        targets = self.descriptor["english_independent_review"]["targets"]
        manifest["suite_research_assets"].remove(targets)
        self.assert_has_error(manifest, self.descriptor, "not registered", root=ROOT)

    def test_descriptor_authority_path_must_be_safe(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["targets"] = "../outside.json"
        self.assert_has_error(manifest=self.manifest, descriptor=descriptor, fragment="unsafe")

    def test_descriptor_authority_file_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = copy.deepcopy(self.manifest)
            descriptor = copy.deepcopy(self.descriptor)
            missing = "research/skill-prototypes/missing-current-authority.md"
            descriptor["complete_checkout_validation"]["evidence"] = missing
            manifest["suite_research_assets"].append(missing)
            self.assert_has_error(manifest, descriptor, "file is missing", root=root)


if __name__ == "__main__":
    unittest.main()
