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

CONTRACT_SCRIPT = ROOT / "research" / "framework-candidates" / "scripts" / "framework_corpus_contract.py"
contract_spec = importlib.util.spec_from_file_location("framework_corpus_contract", CONTRACT_SCRIPT)
assert contract_spec is not None and contract_spec.loader is not None
contract = importlib.util.module_from_spec(contract_spec)
contract_spec.loader.exec_module(contract)


TYPOLOGY_FIXTURE = {
    "schema": "csw.efficacy-framework-typology/v1",
    "status": "research-only / provisional classification",
    "date": "2026-10-03",
    "super_families": {
        "SF-A": "condition and relation",
        "SF-B": "viewpoint and node",
    },
    "target_structures": {
        "TS-condition-chain": "an outcome depends on upstream conditions",
        "TS-node-view": "a role changes when viewed through another node",
    },
    "frameworks": [
        {
            "id": "alpha",
            "sf": "SF-A",
            "structure_kind": "conditional chain",
            "ts": ["TS-condition-chain"],
            "tier": "A",
        },
        {
            "id": "beta",
            "sf": "SF-B",
            "structure_kind": "node-conditioned relation",
            "ts": ["TS-node-view"],
            "tier": "B",
        },
    ],
}


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
            "selection_cues": [
                "成立条件と停止条件を見たい",
                "inspect upstream conditions",
            ],
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
            "selection_cues": [
                "別のnodeから全体を見直したい",
                "change viewpoint through a node",
            ],
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
            "selection_cues": [
                "周期の位相ずれを見たい",
                "inspect recurrence offset",
            ],
            "do_not_assume": [],
            "sources": [],
        },
    ],
}


class FrameworkCorpusContractTest(unittest.TestCase):
    def test_repository_inventory_satisfies_readiness_contract(self) -> None:
        inventory_path = ROOT / "research" / "framework-candidates" / "cognitive-operation-inventory.json"
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(contract.validate_inventory(ROOT, data), [])

    def test_profile_ready_requires_examples_cues_and_debinding(self) -> None:
        row = {
            "id": "candidate",
            "readiness": "profile-ready",
            "names": ["Candidate"],
            "structural_primitives": ["structure"],
            "cognitive_operations": ["probe"],
            "useful_for": ["opening a distinction"],
            "do_not_assume": ["framework result is target fact"],
            "sources": [
                {"kind": "primary", "title": "A", "url": "https://example.com/a"},
                {"kind": "scholarly", "title": "B", "url": "https://example.com/b"},
            ],
            "profile_path": "missing-profile.md",
        }
        errors = contract.validate_candidate(ROOT, row)
        joined = "\n".join(errors)
        self.assertIn("profile-ready requires an existing profile_path", joined)
        self.assertIn("profile-ready requires at least two selection_cues", joined)
        self.assertIn("profile-ready requires worked_example_paths", joined)
        self.assertIn("profile-ready requires negative_example_paths", joined)

    def test_profile_ready_candidates_are_recallable_when_explicitly_requested(self) -> None:
        inventory = workspace.load_inventory(
            ROOT / "research" / "framework-candidates" / "cognitive-operation-inventory.json"
        )
        rows = [
            row for row in workspace.candidates(inventory)
            if row.get("readiness") == "profile-ready"
        ]
        self.assertGreater(len(rows), 0)
        for row in rows:
            cue = row["selection_cues"][0]
            payload = workspace.recall_payload(
                inventory,
                cue,
                ["profile-ready"],
            )
            recalled = [
                item["candidate"]["id"]
                for item in payload["candidates"]
            ]
            self.assertIn(row["id"], recalled, row["id"])


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

    def test_registry_inspect_exposes_provenance_without_authority(self) -> None:
        fixture = json.loads(json.dumps(FIXTURE))
        fixture["candidates"][1]["worked_example_paths"] = [
            "research/framework-candidates/worked-examples/beta.md"
        ]
        fixture["candidates"][1]["negative_example_paths"] = [
            "research/framework-candidates/worked-examples/beta-negative.md"
        ]
        fixture["candidates"][1]["adoption_hold"] = "research-only until boundary review"

        payload = workspace.registry_entry_payload(fixture, "beta")

        self.assertEqual(payload["format"], "csw.framework-registry-entry/v0")
        self.assertEqual(payload["candidate"]["id"], "beta")
        self.assertEqual(payload["registry"]["readiness"], "profile-ready")
        self.assertFalse(payload["registry"]["runtime_enabled"])
        self.assertEqual(
            payload["registry"]["adoption_hold"],
            "research-only until boundary review",
        )
        self.assertEqual(
            payload["registry"]["sources"],
            [{"kind": "scholarly-reference", "title": "B", "url": None}],
        )
        self.assertEqual(
            payload["registry"]["artifacts"]["profile_path"],
            "research/framework-candidates/profiles/beta.md",
        )
        self.assertEqual(
            payload["target_return_material"]["worked_example_paths"],
            ["research/framework-candidates/worked-examples/beta.md"],
        )
        self.assertIn(
            "node is essence",
            payload["authority_boundary"]["do_not_assume"],
        )
        encoded = json.dumps(payload)
        self.assertNotIn('"score"', encoded)
        self.assertNotIn('"rank"', encoded)
        self.assertNotIn('"recommendation"', encoded)

    def test_cli_registry_inspect_keeps_adopted_status_separate_from_fit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / "inventory.json"
            inventory.write_text(json.dumps(FIXTURE), encoding="utf-8")
            payload = json.loads(
                self.run_tool(
                    "inspect",
                    str(inventory),
                    "alpha",
                ).stdout
            )
            self.assertTrue(payload["registry"]["runtime_enabled"])
            self.assertEqual(payload["candidate"]["readiness"], "adopted")
            self.assertIn(
                "not framework fit",
                payload["registry"]["interpretation"],
            )
            self.assertNotIn("score", json.dumps(payload))

    def test_target_structure_lookup_uses_exact_mapping_without_ranking(self) -> None:
        payload = workspace.target_structure_candidates_payload(
            TYPOLOGY_FIXTURE,
            FIXTURE,
            ["TS-condition-chain"],
        )
        structure = payload["target_structures"][0]
        self.assertEqual(structure["id"], "TS-condition-chain")
        self.assertEqual(
            [row["candidate"]["id"] for row in structure["mapped_candidates"]],
            ["alpha"],
        )
        self.assertEqual(
            structure["mapped_candidates"][0]["mapping"]["super_family"],
            "SF-A",
        )
        encoded = json.dumps(payload).casefold()
        self.assertNotIn('"score"', encoded)
        self.assertNotIn('"rank"', encoded)
        self.assertNotIn('"recommendation"', encoded)
        self.assertIn("no semantic classification", payload["interpretation_boundary"])

    def test_target_structure_lookup_requires_exact_known_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown target structure"):
            workspace.target_structure_candidates_payload(
                TYPOLOGY_FIXTURE,
                FIXTURE,
                ["conditions"],
            )

    def test_typology_rejects_unknown_target_structure_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "typology.json"
            broken = json.loads(json.dumps(TYPOLOGY_FIXTURE))
            broken["frameworks"][0]["ts"] = ["TS-missing"]
            path.write_text(json.dumps(broken), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown target structure"):
                workspace.load_typology(path)

    def test_cli_structure_lookup_preserves_inventory_order_without_routing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / "inventory.json"
            typology = Path(tmp) / "typology.json"
            inventory.write_text(json.dumps(FIXTURE), encoding="utf-8")
            typology.write_text(json.dumps(TYPOLOGY_FIXTURE), encoding="utf-8")
            payload = json.loads(
                self.run_tool(
                    "structure-lookup",
                    str(typology),
                    str(inventory),
                    "TS-condition-chain",
                ).stdout
            )
            self.assertEqual(
                payload["target_structures"][0]["mapped_candidates"][0]["candidate"]["id"],
                "alpha",
            )
            self.assertIn("not a ranking", payload["candidate_order_note"])

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

    def test_recall_uses_explicit_cues_and_defaults_to_adopted(self) -> None:
        payload = workspace.recall_payload(
            FIXTURE,
            "この対象の成立条件と停止条件を見たい",
        )
        self.assertEqual(
            [row["candidate"]["id"] for row in payload["candidates"]],
            ["alpha"],
        )
        self.assertEqual(payload["readiness"], ["adopted"])
        self.assertNotIn("score", json.dumps(payload))
        self.assertIn("not ranking", payload["interpretation_boundary"])

    def test_recall_can_include_explicit_non_adopted_readiness(self) -> None:
        payload = workspace.recall_payload(
            FIXTURE,
            "別のnodeから全体を見直したい",
            ["profile-ready"],
        )
        self.assertEqual(
            [row["candidate"]["id"] for row in payload["candidates"]],
            ["beta"],
        )

    def test_recall_normalizes_width_spacing_and_punctuation_without_semantics(self) -> None:
        fixture = json.loads(json.dumps(FIXTURE))
        fixture["candidates"][0]["selection_cues"].append(
            "center / periphery"
        )
        payload = workspace.recall_payload(
            fixture,
            "CENTER・PERIPHERYを見直したい",
        )
        self.assertEqual(
            [row["candidate"]["id"] for row in payload["candidates"]],
            ["alpha"],
        )

    def test_cli_recall_returns_adopted_candidate_without_ranking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / "inventory.json"
            inventory.write_text(json.dumps(FIXTURE), encoding="utf-8")
            payload = json.loads(
                self.run_tool(
                    "recall",
                    str(inventory),
                    "--need",
                    "この対象の成立条件と停止条件を見たい",
                ).stdout
            )
            self.assertEqual(
                [row["candidate"]["id"] for row in payload["candidates"]],
                ["alpha"],
            )
            self.assertNotIn("score", json.dumps(payload))

    def test_real_inventory_adopted_candidates_have_selection_cues(self) -> None:
        inventory = workspace.load_inventory(
            ROOT / "research" / "framework-candidates" / "cognitive-operation-inventory.json"
        )
        adopted = [
            row for row in workspace.candidates(inventory)
            if row.get("readiness") == "adopted"
        ]
        self.assertGreater(len(adopted), 0)
        for row in adopted:
            cues = row.get("selection_cues")
            self.assertIsInstance(cues, list, row["id"])
            self.assertGreaterEqual(len(cues), 2, row["id"])
            self.assertTrue(all(str(cue).strip() for cue in cues), row["id"])
            runtime_path = row.get("runtime_path")
            self.assertTrue(runtime_path, row["id"])
            self.assertTrue((ROOT / runtime_path).is_file(), row["id"])

    def test_real_inventory_each_adopted_candidate_is_recallable_by_own_cue(self) -> None:
        inventory = workspace.load_inventory(
            ROOT / "research" / "framework-candidates" / "cognitive-operation-inventory.json"
        )
        adopted = [
            row for row in workspace.candidates(inventory)
            if row.get("readiness") == "adopted"
        ]
        for row in adopted:
            cue = row["selection_cues"][0]
            payload = workspace.recall_payload(inventory, cue)
            recalled_ids = [
                item["candidate"]["id"]
                for item in payload["candidates"]
            ]
            self.assertIn(row["id"], recalled_ids, row["id"])

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
        self.assertEqual(payload["target_structure_hypotheses"], [])
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

    def test_target_structure_hypothesis_is_separate_from_framework_choice(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need another way to inspect conditions",
            ["alpha", "beta"],
            "Target baseline",
            "selection://target-structure-hypothesis",
        )
        workspace.set_target_structure_hypothesis(
            data,
            TYPOLOGY_FIXTURE,
            "TS-condition-chain",
            basis="The target shows an unresolved upstream dependency.",
        )

        self.assertEqual(
            data["target_structure_hypotheses"],
            [{
                "id": "TS-condition-chain",
                "definition": "an outcome depends on upstream conditions",
                "basis": "The target shows an unresolved upstream dependency.",
                "source_typology": {
                    "schema": "csw.efficacy-framework-typology/v1",
                    "date": "2026-10-03",
                    "status": "research-only / provisional classification",
                },
            }],
        )
        self.assertEqual(
            [row["role"] for row in data["candidates"]],
            ["unassigned", "unassigned"],
        )
        review = workspace.review_payload(data)
        self.assertEqual(
            review["target_structure_hypotheses"][0]["id"],
            "TS-condition-chain",
        )
        self.assertEqual(
            review["target_structure_hypotheses"][0]["source_typology"]["date"],
            "2026-10-03",
        )
        self.assertNotIn("score", json.dumps(review))

    def test_non_force_guardrails_externalize_contact_stop_and_survival(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need another way to inspect boundaries",
            ["alpha"],
            "Target-side baseline before framework contact",
            "selection://round-guardrail/framework-choice",
        )

        workspace.update_non_force_guardrail(
            data,
            "alpha",
            contact_if="The target leaves an unresolved establishment-condition gap.",
            stop_if="The target material has no distinct upstream condition to inspect.",
            survive_if=(
                "A de-bound question still points to a concrete target-side "
                "condition or falsifier."
            ),
        )

        alpha = data["candidates"][0]
        self.assertEqual(
            alpha["non_force_guardrails"]["contact_if"],
            "The target leaves an unresolved establishment-condition gap.",
        )
        self.assertEqual(
            alpha["non_force_guardrails"]["stop_if"],
            "The target material has no distinct upstream condition to inspect.",
        )
        self.assertIn(
            "concrete target-side",
            alpha["non_force_guardrails"]["survive_if"],
        )

        review = workspace.review_payload(data)
        self.assertEqual(review["candidates"][0]["unfilled_guardrails"], [])
        self.assertNotIn("score", json.dumps(review))
        self.assertNotIn("rank", json.dumps(review))

    def test_consideration_axes_keep_routing_dimensions_separate(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need a genuinely different boundary view",
            ["alpha", "beta"],
            "Target baseline before framework contact",
            "selection://round-consider/framework-choice",
        )

        workspace.update_consideration(
            data,
            "alpha",
            target_connection="The target already exposes an upstream condition question.",
            structural_difference="Adds a chain view rather than a node perspective.",
            redundancy_or_overlap="Boundary-probe overlaps beta; condition-chain does not.",
            target_return_feasibility="Can return as a necessary-condition question.",
            misuse_or_authority_risk="Do not treat a condition-chain as causation.",
            domain_constraint="Caller requires source-visible justification.",
        )
        workspace.update_non_activation(
            data,
            reason="The target-side baseline may already expose the missing distinction.",
            baseline_note="Try the ordinary target-side question before framework contact.",
            revisit_if="Activate only if the baseline cannot generate a concrete check.",
        )

        alpha = data["candidates"][0]
        self.assertEqual(
            alpha["consideration_axes"]["structural_difference"],
            "Adds a chain view rather than a node perspective.",
        )
        self.assertEqual(
            data["no_framework_option"]["reason"],
            "The target-side baseline may already expose the missing distinction.",
        )
        self.assertNotIn("score", data["candidates"][0])
        self.assertNotIn("rank", data["candidates"][0])
        self.assertNotIn("ranking", data["candidates"][0])

    def test_review_surfaces_unfilled_axes_without_scoring_or_forcing_activation(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need another way to inspect boundaries",
            ["alpha"],
            None,
            "selection://round-review/framework-choice",
        )
        workspace.update_consideration(
            data,
            "alpha",
            target_connection="There is a concrete boundary question.",
            misuse_or_authority_risk="Do not convert framework fit into target fact.",
        )

        payload = workspace.review_payload(data)
        row = payload["candidates"][0]
        self.assertEqual(row["candidate_id"], "alpha")
        self.assertIn("structural_difference", row["unfilled_axes"])
        self.assertNotIn("target_connection", row["unfilled_axes"])
        self.assertEqual(
            payload["no_framework_unfilled"],
            ["reason", "baseline_note", "what_would_change_this"],
        )
        self.assertIn("not failures", payload["interpretation_boundary"])
        self.assertNotIn("score", payload["candidates"][0])
        self.assertNotIn("rank", payload["candidates"][0])
        self.assertNotIn("ranking", payload["candidates"][0])

    def test_old_workspace_is_hydrated_without_losing_selection_reasoning(self) -> None:
        data = workspace.worksheet_payload(
            FIXTURE,
            "Need a second relation principle",
            ["alpha"],
            "Target baseline",
            "selection://legacy/framework-choice",
        )
        del data["candidates"][0]["consideration_axes"]
        del data["no_framework_option"]
        del data["target_structure_hypotheses"]

        workspace.ensure_consideration_fields(data)

        self.assertEqual(
            set(data["candidates"][0]["consideration_axes"]),
            set(workspace.CONSIDERATION_FIELDS),
        )
        self.assertEqual(
            data["candidates"][0]["non_force_guardrails"],
            {"contact_if": "", "stop_if": "", "survive_if": ""},
        )
        self.assertEqual(
            data["no_framework_option"],
            {"reason": "", "baseline_note": "", "what_would_change_this": ""},
        )
        self.assertEqual(data["target_structure_hypotheses"], [])
        self.assertEqual(
            data["workspace_ref"],
            "selection://legacy/framework-choice",
        )

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
        workspace.update_non_force_guardrail(
            selection,
            "alpha",
            contact_if="Open only while an establishment-condition gap remains.",
            stop_if="Stop if the target no longer exposes an upstream condition.",
            survive_if="Keep only a de-bound target-checkable condition question.",
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
        guardrail_contexts = {
            row["candidate_id"]: row
            for row in payload["candidate_guardrail_contexts"]
        }
        self.assertEqual(
            guardrail_contexts["alpha"]["guardrails"]["stop_if"],
            "Stop if the target no longer exposes an upstream condition.",
        )
        self.assertEqual(
            guardrail_contexts["alpha"]["target_responses"],
            ["weakened"],
        )
        self.assertEqual(
            guardrail_contexts["alpha"]["target_return_states"],
            ["weakened"],
        )
        self.assertEqual(
            guardrail_contexts["beta"]["target_return_states"],
            [],
        )
        self.assertNotIn("pass", json.dumps(guardrail_contexts).casefold())
        self.assertNotIn("fail", json.dumps(guardrail_contexts).casefold())
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

    def test_living_lab_audit_joins_selection_contact_and_artifact_provenance(self) -> None:
        selection = workspace.worksheet_payload(
            FIXTURE,
            "Need another boundary view",
            ["alpha", "beta"],
            "Target baseline",
            "selection://living-lab-audit/framework-choice",
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
        workspace.update_non_force_guardrail(
            selection,
            "alpha",
            contact_if="Open only while a concrete condition gap remains.",
            stop_if="Stop if the target exposes no distinct upstream condition.",
            survive_if="Keep only a de-bound target-checkable question.",
        )

        round_record = {
            "schema_version": "0.2",
            "round_id": "round-living-lab-audit-001",
            "activation_scope": "exploratory_use",
            "framework_contacts": [
                {
                    "framework": "alpha",
                    "depth": "preview",
                    "use": "exploration",
                    "selection_ref": "selection://living-lab-audit/framework-choice",
                    "operations": ["condition-chain"],
                },
                {
                    "framework": "beta",
                    "depth": "preview",
                    "use": "exploration",
                    "selection_ref": "selection://other/framework-choice",
                    "operations": ["node-perspective"],
                },
            ],
            "catalytic_deltas": [
                {
                    "delta_ref": "delta:alpha-condition-question",
                    "kind": "question",
                    "statement": "Which upstream condition actually survives target return?",
                    "framework_refs": ["alpha"],
                    "pre_contact_relation": {
                        "state": "reframed_existing",
                        "source_type": "mixed",
                        "evidence_refs": ["artifact:baseline-alpha"],
                    },
                    "selection_refs": [
                        "selection://living-lab-audit/framework-choice"
                    ],
                    "operation_refs": ["condition-chain"],
                    "artifact_refs": ["artifact:alpha-1"],
                    "target_return": {
                        "state": "target_supported",
                        "source_type": "external",
                        "evidence_refs": ["artifact:target-delta-1"],
                    },
                    "user_disposition": {
                        "state": "adopted",
                        "source_ref": "chat:user-delta-1",
                    },
                },
                {
                    "delta_ref": "delta:beta-other-selection",
                    "kind": "relation-or-transition",
                    "statement": "This belongs to another selection workspace.",
                    "framework_refs": ["beta"],
                    "selection_refs": ["selection://other/framework-choice"],
                    "operation_refs": ["node-perspective"],
                    "target_return": {
                        "state": "target_supported",
                        "source_type": "external",
                        "evidence_refs": ["artifact:target-delta-2"],
                    },
                },
            ],
            "artifact_traces": [
                {
                    "artifact_ref": "artifact:alpha-1",
                    "origin": "framework_generated",
                    "framework_refs": ["alpha"],
                    "selection_refs": [
                        "selection://living-lab-audit/framework-choice"
                    ],
                    "operation_refs": ["condition-chain"],
                    "target_return": {
                        "state": "target_weakened",
                        "source_type": "mixed",
                        "evidence_refs": ["artifact:target-1"],
                    },
                    "user_disposition": {
                        "state": "modified",
                        "source_ref": "chat:user-1",
                    },
                },
                {
                    "artifact_ref": "artifact:beta-other-selection",
                    "origin": "framework_generated",
                    "framework_refs": ["beta"],
                    "selection_refs": ["selection://other/framework-choice"],
                    "operation_refs": ["node-perspective"],
                    "target_return": {
                        "state": "target_supported",
                        "source_type": "external",
                        "evidence_refs": ["artifact:target-2"],
                    },
                    "user_disposition": {
                        "state": "adopted",
                        "source_ref": "chat:user-2",
                    },
                },
            ],
        }

        payload = workspace.audit_living_lab_payload(selection, round_record)

        self.assertEqual(payload["round_id"], "round-living-lab-audit-001")
        self.assertEqual(
            [contact["framework"] for contact in payload["linked_contacts"]],
            ["alpha"],
        )
        self.assertEqual(
            [delta["delta_ref"] for delta in payload["linked_deltas"]],
            ["delta:alpha-condition-question"],
        )
        self.assertEqual(
            [trace["artifact_ref"] for trace in payload["linked_artifacts"]],
            ["artifact:alpha-1"],
        )
        self.assertEqual(payload["contacted_operations"], ["condition-chain"])
        self.assertEqual(payload["delta_operations"], ["condition-chain"])
        self.assertEqual(payload["delta_kinds"], ["question"])
        self.assertEqual(
            payload["delta_pre_contact_states"],
            ["reframed_existing"],
        )
        self.assertEqual(
            payload["delta_target_return_states"],
            ["target_supported"],
        )
        self.assertEqual(payload["delta_user_dispositions"], ["adopted"])
        self.assertEqual(payload["artifact_operations"], ["condition-chain"])
        self.assertEqual(payload["target_return_states"], ["target_weakened"])
        self.assertEqual(payload["user_dispositions"], ["modified"])
        self.assertEqual(
            payload["planned_not_contacted_exact"],
            ["node-perspective"],
        )
        self.assertEqual(payload["contacted_not_delta_traced_exact"], [])
        self.assertEqual(payload["delta_not_contacted_exact"], [])
        self.assertEqual(payload["delta_not_artifact_traced_exact"], [])
        self.assertEqual(payload["artifact_not_delta_traced_exact"], [])

        audits = {
            row["candidate_id"]: row
            for row in payload["candidate_audits"]
        }
        self.assertEqual(
            audits["alpha"]["linked_delta_refs"],
            ["delta:alpha-condition-question"],
        )
        self.assertEqual(audits["alpha"]["delta_kinds"], ["question"])
        self.assertEqual(
            audits["alpha"]["delta_pre_contact_states"],
            ["reframed_existing"],
        )
        self.assertEqual(
            audits["alpha"]["delta_target_return_states"],
            ["target_supported"],
        )
        self.assertEqual(
            audits["alpha"]["delta_operations"],
            ["condition-chain"],
        )
        self.assertEqual(audits["alpha"]["delta_user_dispositions"], ["adopted"])
        self.assertEqual(audits["alpha"]["contacted_not_delta_traced_exact"], [])
        self.assertEqual(audits["alpha"]["delta_not_contacted_exact"], [])
        self.assertEqual(audits["alpha"]["delta_not_artifact_traced_exact"], [])
        self.assertEqual(audits["alpha"]["artifact_not_delta_traced_exact"], [])
        self.assertEqual(
            audits["alpha"]["linked_artifact_refs"],
            ["artifact:alpha-1"],
        )
        self.assertEqual(
            audits["alpha"]["guardrails"]["stop_if"],
            "Stop if the target exposes no distinct upstream condition.",
        )
        self.assertEqual(
            audits["alpha"]["target_return_states"],
            ["target_weakened"],
        )
        self.assertEqual(audits["alpha"]["user_dispositions"], ["modified"])
        self.assertEqual(audits["beta"]["linked_artifact_refs"], [])
        self.assertEqual(audits["beta"]["target_return_states"], [])

        encoded = json.dumps(payload).casefold()
        self.assertNotIn('"score"', encoded)
        self.assertNotIn('"rank"', encoded)
        self.assertNotIn('"recommendation"', encoded)

    def test_living_lab_audit_cli_uses_exact_workspace_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            selection_path = Path(tmp) / "selection.json"
            round_path = Path(tmp) / "round.json"
            selection = workspace.worksheet_payload(
                FIXTURE,
                "Need another boundary view",
                ["alpha"],
                "Target baseline",
                "selection://cli-living-lab/framework-choice",
            )
            workspace.update_candidate(
                selection,
                "alpha",
                planned_operations=["condition-chain"],
            )
            workspace.save_workspace(selection_path, selection)
            round_path.write_text(
                json.dumps({
                    "schema_version": "0.2",
                    "round_id": "round-cli-living-lab-001",
                    "activation_scope": "limited_use",
                    "framework_contacts": [{
                        "framework": "alpha",
                        "depth": "preview",
                        "use": "exploration",
                        "selection_ref": "selection://cli-living-lab/framework-choice",
                        "operations": ["condition-chain"],
                    }],
                    "catalytic_deltas": [{
                        "delta_ref": "delta:cli-alpha-question",
                        "kind": "question",
                        "statement": "Which condition remains after return?",
                        "framework_refs": ["alpha"],
                        "selection_refs": [
                            "selection://cli-living-lab/framework-choice"
                        ],
                        "operation_refs": ["condition-chain"],
                        "target_return": {
                            "state": "unresolved",
                            "source_type": "ai",
                            "evidence_refs": ["artifact:target-cli"],
                        },
                    }],
                    "artifact_traces": [{
                        "artifact_ref": "artifact:cli-alpha-1",
                        "origin": "framework_generated",
                        "framework_refs": ["alpha"],
                        "selection_refs": [
                            "selection://cli-living-lab/framework-choice"
                        ],
                        "operation_refs": ["condition-chain"],
                        "target_return": {
                            "state": "unresolved",
                            "source_type": "ai",
                            "evidence_refs": ["artifact:target-cli"],
                        },
                    }],
                }),
                encoding="utf-8",
            )

            payload = json.loads(
                self.run_tool(
                    "audit-living-lab",
                    str(selection_path),
                    str(round_path),
                ).stdout
            )
            self.assertEqual(
                payload["workspace_ref"],
                "selection://cli-living-lab/framework-choice",
            )
            self.assertEqual(
                payload["linked_deltas"][0]["delta_ref"],
                "delta:cli-alpha-question",
            )
            self.assertEqual(
                payload["linked_artifacts"][0]["artifact_ref"],
                "artifact:cli-alpha-1",
            )
            self.assertEqual(payload["target_return_states"], ["unresolved"])

    def test_living_lab_loader_rejects_invalid_catalytic_delta_container(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            round_path = Path(tmp) / "round.json"
            round_path.write_text(
                json.dumps({
                    "schema_version": "0.2",
                    "round_id": "round-invalid-deltas",
                    "framework_contacts": [],
                    "catalytic_deltas": ["not-an-object"],
                    "artifact_traces": [],
                }),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError,
                "catalytic_deltas must be an array of objects",
            ):
                workspace.load_living_lab_round(round_path)

    def test_living_lab_loader_rejects_unknown_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            round_path = Path(tmp) / "round.json"
            round_path.write_text(
                json.dumps({
                    "schema_version": "9.9",
                    "round_id": "round-unknown-schema",
                    "framework_contacts": [],
                    "artifact_traces": [],
                }),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unsupported Living Lab"):
                workspace.load_living_lab_round(round_path)

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
            typology = Path(tmp) / "typology.json"
            selection = Path(tmp) / "selection.json"
            inventory.write_text(json.dumps(FIXTURE), encoding="utf-8")
            typology.write_text(json.dumps(TYPOLOGY_FIXTURE), encoding="utf-8")

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
                "set-target-structure",
                str(selection),
                str(typology),
                "TS-condition-chain",
                "--basis",
                "The target shows an unresolved upstream dependency.",
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
                "set-consideration",
                str(selection),
                "alpha",
                "--target-connection",
                "A concrete target-side condition question exists.",
                "--structural-difference",
                "Condition-chain differs from node perspective.",
                "--target-return",
                "Return as a necessary-condition check.",
                "--misuse-risk",
                "Do not equate condition with cause.",
            )
            self.run_tool(
                "set-guardrail",
                str(selection),
                "alpha",
                "--contact-if",
                "Open only if a concrete condition gap remains.",
                "--stop-if",
                "Stop if the target has no distinct upstream condition.",
                "--survive-if",
                "Carry forward only a de-bound target-checkable question.",
            )
            self.run_tool(
                "set-non-activation",
                str(selection),
                "--reason",
                "Baseline may already be sufficient.",
                "--revisit-if",
                "Activate if baseline fails to produce a concrete check.",
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
                shown["target_structure_hypotheses"][0]["id"],
                "TS-condition-chain",
            )
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
                shown["candidates"][0]["consideration_axes"]["target_connection"],
                "A concrete target-side condition question exists.",
            )
            self.assertEqual(
                shown["candidates"][0]["non_force_guardrails"]["stop_if"],
                "Stop if the target has no distinct upstream condition.",
            )
            self.assertEqual(
                shown["no_framework_option"]["reason"],
                "Baseline may already be sufficient.",
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
