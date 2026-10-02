from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research" / "framework-candidates" / "scripts" / "framework_selection_workspace.py"
spec = importlib.util.spec_from_file_location("framework_selection_workspace", SCRIPT)
assert spec is not None and spec.loader is not None
workspace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workspace)


FIXTURE = {
    "schema": "csw.framework-candidate-inventory/v1",
    "status": "research-only",
    "candidates": [
        {
            "id": "alpha",
            "names": ["Alpha"],
            "readiness": "adopted",
            "structural_primitives": ["chain", "threshold"],
            "cognitive_operations": ["condition-chain", "boundary-probe"],
            "useful_for": ["finding upstream conditions"],
            "do_not_assume": ["condition is cause"],
            "sources": [{"kind": "primary-text", "title": "A"}],
            "runtime_path": "src/ja-JP/frameworks/alpha.md",
        },
        {
            "id": "beta",
            "names": ["Beta"],
            "readiness": "profile-ready",
            "structural_primitives": ["node", "threshold"],
            "cognitive_operations": ["boundary-probe", "node-perspective"],
            "useful_for": ["changing viewpoint through a node"],
            "do_not_assume": ["node is essence"],
            "sources": [{"kind": "scholarly-reference", "title": "B"}],
            "profile_path": "research/framework-candidates/profiles/beta.md",
        },
        {
            "id": "gamma",
            "names": ["Gamma"],
            "readiness": "sourced-candidate",
            "structural_primitives": ["cycle"],
            "cognitive_operations": ["phase-offset"],
            "useful_for": ["finding recurrence offset"],
            "do_not_assume": [],
            "sources": [],
        },
    ],
}


class FrameworkSelectionWorkspaceTest(unittest.TestCase):
    def test_shortlist_preserves_inventory_order_without_score(self) -> None:
        payload = workspace.shortlist_payload(FIXTURE, "threshold", "primitive", None)
        self.assertEqual(
            [row["candidate"]["id"] for row in payload["candidates"]],
            ["alpha", "beta"],
        )
        self.assertNotIn("score", json.dumps(payload))

    def test_shortlist_filters_readiness_without_ranking(self) -> None:
        payload = workspace.shortlist_payload(
            FIXTURE, "boundary", "operation", ["profile-ready"]
        )
        self.assertEqual(
            [row["candidate"]["id"] for row in payload["candidates"]],
            ["beta"],
        )

    def test_contrast_exposes_exact_overlap_and_unique_operations(self) -> None:
        payload = workspace.contrast_payload(FIXTURE, ["alpha", "beta"])
        alpha, beta = payload["candidates"]
        self.assertEqual(alpha["exact_common_operations"], ["boundary-probe"])
        self.assertEqual(alpha["exact_unique_operations"], ["condition-chain"])
        self.assertEqual(beta["exact_unique_operations"], ["node-perspective"])

    def test_worksheet_leaves_selection_judgment_unassigned(self) -> None:
        payload = workspace.worksheet_payload(
            FIXTURE,
            "Need another way to inspect boundaries",
            ["alpha", "beta"],
            "Target-side baseline before framework contact",
            "selection://round-03/framework-choice",
        )
        self.assertEqual(
            payload["workspace_ref"],
            "selection://round-03/framework-choice",
        )
        self.assertEqual(payload["candidates"][0]["role"], "unassigned")
        self.assertEqual(payload["cross_framework_notes"]["primary_framework_job"], "")
        self.assertEqual(payload["exit_record"]["questions_created"], [])
        self.assertIn("does not choose a framework", payload["interpretation_boundary"])

    def test_inventory_rejects_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            data = dict(FIXTURE)
            data["candidates"] = [FIXTURE["candidates"][0], FIXTURE["candidates"][0]]
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate candidate id"):
                workspace.load_inventory(path)


if __name__ == "__main__":
    unittest.main()
