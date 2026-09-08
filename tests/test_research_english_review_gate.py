from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_english_review_gate import (  # noqa: E402
    validate_english_review_gate,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
PACKET_RELATIVE = Path(
    "research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-PACKET-2026-09-08.md"
)
TARGETS_RELATIVE = Path(
    "research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-08-v3.json"
)
PREVIOUS_TARGETS_RELATIVE = Path(
    "research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-07-v2.json"
)
LOCALIZATION_RELATIVE = Path(
    "research/skill-prototypes/P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json"
)


class ResearchEnglishReviewGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.targets = json.loads((ROOT / TARGETS_RELATIVE).read_text(encoding="utf-8"))

    def assert_has_error(self, descriptor: dict, fragment: str) -> None:
        errors = validate_english_review_gate(ROOT, descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def prepare_review_root(self, root: Path) -> None:
        for relative in (PACKET_RELATIVE, TARGETS_RELATIVE, LOCALIZATION_RELATIVE):
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        for item in self.targets["targets"]:
            for locale in ("ja", "en"):
                relative = Path(item[locale]["path"])
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    def test_current_gate_is_valid_and_pending(self) -> None:
        self.assertEqual(validate_english_review_gate(ROOT, self.descriptor), [])
        gate = self.descriptor["english_independent_review"]
        self.assertEqual(gate["status"], "pending")
        self.assertEqual(gate["targets"], str(TARGETS_RELATIVE))
        self.assertEqual(gate["packet"], str(PACKET_RELATIVE))
        self.assertEqual(
            gate["technical_asset_localization"], str(LOCALIZATION_RELATIVE)
        )
        self.assertIsNone(gate["completed_review"])
        self.assertFalse(gate["production_promotion_authorized"])

    def test_v3_snapshot_contains_runtime_method_and_direct_technical_assets(self) -> None:
        pairs = {
            (item["research_id"], item["artifact"])
            for item in self.targets["targets"]
        }
        self.assertEqual(
            pairs,
            {
                ("affinity-synthesis", "runtime"),
                ("affinity-synthesis", "method_definition"),
                ("affinity-synthesis", "representation_grammar"),
                ("iterative-inquiry-synthesis", "runtime"),
                ("iterative-inquiry-synthesis", "method_definition"),
                ("iterative-inquiry-synthesis", "round_template"),
            },
        )
        self.assertEqual(
            self.targets["supersedes"],
            str(PREVIOUS_TARGETS_RELATIVE),
        )
        self.assertEqual(
            self.targets["review_source_commit"],
            "6a9118cd71959dcebaf09e64f235d650eb2e1ff8",
        )

    def test_pending_gate_cannot_claim_completed_review(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["completed_review"] = (
            "research/skill-prototypes/reviews/english-review.md"
        )
        self.assert_has_error(
            descriptor,
            "pending English independent review must not declare completed_review",
        )

    def test_review_gate_never_authorizes_production_promotion(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["production_promotion_authorized"] = True
        self.assert_has_error(
            descriptor,
            "must not authorize production promotion by itself",
        )

    def test_completed_gate_requires_separate_review_record(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        gate = descriptor["english_independent_review"]
        gate["status"] = "completed"
        gate["completed_review"] = str(PACKET_RELATIVE)
        self.assert_has_error(
            descriptor,
            "completed review record must be separate from the review packet",
        )

    def test_snapshot_detects_changed_review_target_blob(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_review_root(root)
            changed_relative = Path(self.targets["targets"][0]["en"]["path"])
            changed = root / changed_relative
            changed.write_text(
                changed.read_text(encoding="utf-8") + "\nchanged after snapshot\n",
                encoding="utf-8",
            )
            errors = validate_english_review_gate(root, self.descriptor)
            self.assertTrue(
                any("blob changed since snapshot" in error for error in errors),
                errors,
            )

    def test_gate_requires_current_v3_snapshot(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["targets"] = str(
            PREVIOUS_TARGETS_RELATIVE
        )
        self.assert_has_error(
            descriptor,
            "must reference the canonical v3 review target snapshot",
        )

    def test_gate_requires_localization_contract(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["technical_asset_localization"] = (
            "research/skill-prototypes/other-localization.json"
        )
        self.assert_has_error(
            descriptor,
            "must reference the canonical localization contract",
        )

    def test_completed_gate_accepts_structured_independent_review_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_review_root(root)

            review_relative = Path(
                "research/skill-prototypes/reviews/english-independent-review.md"
            )
            review_path = root / review_relative
            review_path.parent.mkdir(parents=True, exist_ok=True)
            review_path.write_text(
                "reviewer: external-reviewer\n"
                "reviewer relation / independence: independent of the draft author\n"
                "review date: 2026-09-08\n"
                "review scope: sibling runtimes, Method Definitions, and directly referenced technical assets\n"
                "Layer 1:\n"
                "  technical asset parity: pass\n"
                "Layer 2:\n"
                "  technical asset parity: pass\n"
                "Cross-layer ownership:\n"
                "KJ lineage / naming:\n"
                "Promotion recommendation:\n"
                f"Reviewed target snapshot: {TARGETS_RELATIVE}\n"
                "Reviewed commit / blob refs:\n",
                encoding="utf-8",
            )

            descriptor = copy.deepcopy(self.descriptor)
            gate = descriptor["english_independent_review"]
            gate["status"] = "completed"
            gate["completed_review"] = str(review_relative)

            self.assertEqual(validate_english_review_gate(root, descriptor), [])


if __name__ == "__main__":
    unittest.main()
