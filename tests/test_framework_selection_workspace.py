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
            planned_operations=["condition-chain"],
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
        self.assertEqual(alpha["planned_operations"], ["condition-chain"])
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

    def test_audit_map_compares_planned_and_observed_operations_without_scoring(self) -> None:
        selection = workspace.worksheet_payload(
            FIXTURE,
            "Need another boundary view",
            ["alpha", "beta"],
            "Target baseline",
            "selection://round-audit/framework-choice",
        )
        workspace.update_candidate(
            selection,
            "alpha",
            role="primary",
            planned_operations=["condition-chain"],
        )
        workspace.update_candidate(
            selection,
            "beta",
            role="reflecting",
            planned_operations=["node-perspective"],
        )

        affinity_map = {
            "format": "affinity-map",
            "version": "0.1",
            "cards": [
                {
                    "id": "C001",
                    "text": "Candidate from alpha",
                    "input_status": "framework_generated",
                    "catalytic_trace": {
                        "selection_refs": ["selection://round-audit/framework-choice"],
                        "frameworks": ["alpha"],
                        "operations": ["condition-chain"],
                        "yield_kinds": ["question"],
                        "target_responses": ["weakened"],
                        "target_return_audits": [{"state": "weakened"}],
                    },
                },
                {
                    "id": "C002",
                    "text": "Candidate using a noncanonical framework label",
                    "input_status": "framework_generated",
                    "catalytic_trace": {
                        "selection_refs": ["selection://round-audit/framework-choice"],
                        "frameworks": ["beta-alias"],
                        "operations": ["boundary-probe"],
                        "yield_kinds": ["distinction"],
                    },
                },
                {
                    "id": "C003",
                    "text": "Cross-field result",
                    "input_status": "cross_field_emergent",
                    "cross_field_trace": {
                        "target_refs": ["S001"],
                        "framework_refs": ["C001"],
                    },
                },
                {
                    "id": "C004",
                    "text": "Another selection",
                    "input_status": "framework_generated",
                    "catalytic_trace": {
                        "selection_refs": ["selection://other"],
                        "frameworks": ["beta"],
                        "operations": ["node-perspective"],
                    },
                },
            ],
        }

        payload = workspace.audit_map_payload(selection, affinity_map)
        self.assertEqual([card["id"] for card in payload["linked_cards"]], ["C001", "C002"])
        self.assertEqual(
            payload["planned_operations"],
            ["condition-chain", "node-perspective"],
        )
        self.assertEqual(
            payload["observed_operations"],
            ["condition-chain", "boundary-probe"],
        )
        self.assertEqual(
            payload["planned_not_observed_exact"],
            ["node-perspective"],
        )
        self.assertEqual(
            payload["observed_not_planned_exact"],
            ["boundary-probe"],
        )
        self.assertEqual(payload["cards_by_exact_candidate_id"]["alpha"], ["C001"])
        self.assertEqual(payload["cards_by_exact_candidate_id"]["beta"], [])
        self.assertEqual(
            payload["framework_labels_without_exact_candidate_id_match"],
            ["beta-alias"],
        )
        self.assertEqual(payload["downstream_cross_field_cards"], ["C003"])
        candidate_audits = {
            row["candidate_id"]: row
            for row in payload["candidate_operation_audits"]
        }
        self.assertEqual(
            candidate_audits["alpha"]["observed_operations"],
            ["condition-chain"],
        )
        self.assertEqual(
            candidate_audits["alpha"]["planned_not_observed_exact"],
            [],
        )
        self.assertEqual(candidate_audits["alpha"]["yield_kinds"], ["question"])
        self.assertEqual(
            candidate_audits["alpha"]["target_responses"],
            ["weakened"],
        )
        self.assertEqual(
            candidate_audits["alpha"]["target_return_states"],
            ["weakened"],
        )
        self.assertEqual(
            candidate_audits["beta"]["observed_operations"],
            [],
        )
        self.assertEqual(
            candidate_audits["beta"]["planned_not_observed_exact"],
            ["node-perspective"],
        )
        self.assertEqual(candidate_audits["beta"]["yield_kinds"], [])
        self.assertEqual(candidate_audits["beta"]["target_responses"], [])
        self.assertEqual(candidate_audits["beta"]["target_return_states"], [])
        self.assertNotIn("score", json.dumps(payload))

    def test_candidate_audit_does_not_credit_another_frameworks_operation(self) -> None:
        selection = workspace.worksheet_payload(
            FIXTURE,
            "Separate framework contribution",
            ["alpha", "beta"],
            None,
            "selection://candidate-attribution",
        )
        workspace.update_candidate(
            selection,
            "alpha",
            planned_operations=["condition-chain"],
        )
        workspace.update_candidate(
            selection,
            "beta",
            planned_operations=["node-perspective"],
        )
        affinity_map = {
            "format": "affinity-map",
            "version": "0.1",
            "cards": [
                {
                    "id": "C001",
                    "text": "Beta happened to use alpha's planned operation",
                    "input_status": "framework_generated",
                    "catalytic_trace": {
                        "selection_refs": ["selection://candidate-attribution"],
                        "frameworks": ["beta"],
                        "operations": ["condition-chain"],
                    },
                }
            ],
        }

        payload = workspace.audit_map_payload(selection, affinity_map)
        self.assertEqual(payload["planned_not_observed_exact"], ["node-perspective"])
        self.assertEqual(
            payload["candidate_operation_audits"],
            [
                {
                    "candidate_id": "alpha",
                    "linked_card_ids": [],
                    "planned_operations": ["condition-chain"],
                    "observed_operations": [],
                    "planned_not_observed_exact": ["condition-chain"],
                    "observed_not_planned_exact": [],
                    "yield_kinds": [],
                    "target_responses": [],
                    "target_return_states": [],
                },
                {
                    "candidate_id": "beta",
                    "linked_card_ids": ["C001"],
                    "planned_operations": ["node-perspective"],
                    "observed_operations": ["condition-chain"],
                    "planned_not_observed_exact": ["node-perspective"],
                    "observed_not_planned_exact": ["condition-chain"],
                    "yield_kinds": [],
                    "target_responses": [],
                    "target_return_states": [],
                },
            ],
        )
        self.assertNotIn("score", json.dumps(payload))

    def test_candidate_rejects_operation_not_available_in_inventory(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need another boundary view",
            ["alpha"],
            None,
            "selection://round-ops/framework-choice",
        )
        before = json.dumps(data, sort_keys=True)
        with self.assertRaisesRegex(
            ValueError,
            "planned operation is not available for candidate alpha",
        ):
            workspace.update_candidate(
                data,
                "alpha",
                planned_operations=["node-perspective"],
            )
        self.assertEqual(json.dumps(data, sort_keys=True), before)

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
                "--operation",
                "condition-chain",
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
                shown["candidates"][0]["planned_operations"],
                ["condition-chain"],
            )
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
