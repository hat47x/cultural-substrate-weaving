from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
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
    def run_tool(
        self,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            check=check,
            text=True,
            capture_output=True,
        )

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

    def test_workspace_mutations_preserve_explicit_reasoning(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need another way to inspect boundaries",
            ["alpha", "beta"],
            "Target baseline",
            "selection://round-04/framework-choice",
        )

        workspace.update_candidate(
            data,
            "alpha",
            role="primary",
            job="test upstream conditions",
            difference="condition-chain rather than node perspective",
            return_questions=["What condition would stop the pattern?"],
        )
        workspace.update_candidate(
            data,
            "beta",
            role="reflecting",
            job="disturb the primary view through node perspective",
            revisit_if="the target has no meaningful node-dependent role change",
        )
        workspace.update_cross_framework(
            data,
            primary_job="expose establishment conditions",
            second_job="re-identify parts through a different node",
            disturb="the primary framework's fixed condition chain",
            confusions=["do not collapse dependency into whole/part reciprocity"],
            pushbacks=["target material may reject the proposed node boundary"],
        )
        workspace.add_exit_record(
            data,
            "question",
            "Which target-side condition is actually necessary?",
        )
        workspace.add_exit_record(
            data,
            "residual",
            "The node boundary remains unresolved.",
        )

        alpha, beta = data["candidates"]
        self.assertEqual(alpha["role"], "primary")
        self.assertEqual(alpha["intended_cognitive_job"], "test upstream conditions")
        self.assertEqual(
            alpha["target_return_questions"],
            ["What condition would stop the pattern?"],
        )
        self.assertEqual(beta["role"], "reflecting")
        self.assertEqual(
            data["cross_framework_notes"]["what_the_second_framework_should_disturb"],
            "the primary framework's fixed condition chain",
        )
        self.assertEqual(
            data["exit_record"]["questions_created"],
            ["Which target-side condition is actually necessary?"],
        )
        self.assertEqual(
            data["exit_record"]["residuals_created"],
            ["The node boundary remains unresolved."],
        )
        self.assertNotIn("score", json.dumps(data))

    def test_workspace_round_trip_is_atomic_and_refuses_overwrite_on_creation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selection.json"
            data = workspace.worksheet_payload(
                FIXTURE,
                "Need a second relation principle",
                ["alpha"],
                None,
                "selection://round-05/framework-choice",
            )
            workspace.save_workspace(path, data)
            loaded = workspace.load_workspace(path)
            self.assertEqual(loaded["workspace_ref"], "selection://round-05/framework-choice")
            self.assertEqual(loaded["candidates"][0]["role"], "unassigned")

    def test_cli_round_trip_updates_saved_selection_reasoning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / "inventory.json"
            selection = Path(tmp) / "selection.json"
            inventory.write_text(json.dumps(FIXTURE), encoding="utf-8")

            self.run_tool(
                "worksheet",
                str(inventory),
                "--need",
                "Need another way to inspect boundaries",
                "--candidate",
                "alpha",
                "--candidate",
                "beta",
                "--baseline",
                "Target baseline",
                "--ref",
                "selection://round-06/framework-choice",
                "--output",
                str(selection),
            )
            self.run_tool(
                "set-candidate",
                str(selection),
                "alpha",
                "--role",
                "primary",
                "--job",
                "test upstream conditions",
                "--return-question",
                "What condition would stop the pattern?",
            )
            self.run_tool(
                "set-cross-framework",
                str(selection),
                "--primary-job",
                "expose establishment conditions",
                "--second-job",
                "re-identify parts through a node",
                "--disturb",
                "fixed one-way condition chain",
            )
            self.run_tool(
                "record-exit",
                str(selection),
                "--kind",
                "residual",
                "The node boundary remains unresolved.",
            )

            shown = json.loads(
                self.run_tool("show", str(selection)).stdout
            )
            self.assertEqual(
                shown["workspace_ref"],
                "selection://round-06/framework-choice",
            )
            self.assertEqual(shown["candidates"][0]["role"], "primary")
            self.assertEqual(
                shown["candidates"][0]["target_return_questions"],
                ["What condition would stop the pattern?"],
            )
            self.assertEqual(
                shown["cross_framework_notes"]["primary_framework_job"],
                "expose establishment conditions",
            )
            self.assertEqual(
                shown["exit_record"]["residuals_created"],
                ["The node boundary remains unresolved."],
            )

            overwrite = self.run_tool(
                "worksheet",
                str(inventory),
                "--need",
                "Another need",
                "--candidate",
                "alpha",
                "--output",
                str(selection),
                check=False,
            )
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertIn("refusing to overwrite existing workspace", overwrite.stderr)

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
