from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_lineage import LineageGraph  # noqa: E402


FIXTURE = {
    "format": "affinity-map",
    "version": "0.1",
    "sources": [
        {"id": "S01", "ref": "source A"},
        {"id": "S02", "ref": "source B"},
    ],
    "cards": [
        {"id": "C001", "text": "main card", "source_refs": ["S01"]},
        {"id": "C002", "text": "group member", "source_refs": ["S02"]},
    ],
    "groups": [
        {"id": "G01", "label": "primary group", "members": ["C002"]},
    ],
    "resonances": [
        {
            "id": "X01",
            "from": "C001",
            "to": "G01",
            "note": "C001 resonates with G01 without becoming its member",
            "display_label": "secondary resonance",
        }
    ],
    "narratives": [
        {
            "id": "N01",
            "text": "A narrative unit that explicitly keeps X01 in its basis.",
            "basis": ["X01"],
        }
    ],
}


class ResearchAffinityLineageProjectionTests(unittest.TestCase):
    def graph(self, focus: str, *, detail: str = "cards") -> LineageGraph:
        graph = LineageGraph(FIXTURE, detail)
        graph.walk(focus)
        return graph

    def test_secondary_resonance_is_a_known_lineage_artifact(self) -> None:
        graph = self.graph("X01")
        self.assertEqual(graph.kind("X01"), "resonances")
        self.assertIn("X01", graph.nodes)
        self.assertEqual(graph.nodes["X01"][1], "resonances")

    def test_secondary_resonance_traces_both_endpoints_without_membership_claim(self) -> None:
        graph = self.graph("X01")
        self.assertIn(("C001", "X01", "secondary resonance source"), graph.edges)
        self.assertIn(("G01", "X01", "resonance target / not membership"), graph.edges)
        self.assertNotIn(("C001", "G01", "membership"), graph.edges)

    def test_narrative_basis_can_trace_through_secondary_resonance(self) -> None:
        graph = self.graph("N01")
        self.assertIn(("X01", "N01", "narrative basis"), graph.edges)
        self.assertIn(("C001", "X01", "secondary resonance source"), graph.edges)
        self.assertIn(("G01", "X01", "resonance target / not membership"), graph.edges)
        self.assertIn(("S01", "C001", "source → card"), graph.edges)
        self.assertIn(("C002", "G01", "membership"), graph.edges)
        self.assertIn(("S02", "C002", "source → card"), graph.edges)

    def test_mermaid_keeps_not_membership_label_visible(self) -> None:
        output = self.graph("X01").mermaid()
        self.assertIn("X01", output)
        self.assertIn("secondary resonance source", output)
        self.assertIn("resonance target / not membership", output)


if __name__ == "__main__":
    unittest.main()
