from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research/skill-prototypes/affinity-synthesis/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_mermaid import render_group_map  # noqa: E402


class ResearchAffinityMermaidProjectionTests(unittest.TestCase):
    def base_map(self) -> dict:
        return {
            "format": "affinity-map",
            "version": "0.1",
            "cards": [
                {"id": "C01", "text": "カード1"},
                {"id": "C02", "text": "カード2"},
            ],
            "groups": [
                {"id": "G01", "label": "島1", "members": ["C01"]},
                {"id": "G02", "label": "島2", "members": ["C02"]},
            ],
            "relations": [],
            "questions": [],
        }

    def test_candidate_relation_is_routed_through_question_node(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "この二つに関係があるか",
                "candidate_relation_between": ["G01", "G02"],
            }
        ]

        rendered = render_group_map(data)

        self.assertIn('G01 -.->|"candidate endpoint / not asserted relation"| Q01', rendered)
        self.assertIn('G02 -.->|"candidate endpoint / not asserted relation"| Q01', rendered)
        self.assertNotIn("G01 -.-> G02", rendered)
        self.assertNotIn("G02 -.-> G01", rendered)
        self.assertNotIn("G01 --> G02", rendered)
        self.assertNotIn("G02 --> G01", rendered)

    def test_card_candidate_endpoint_is_declared_with_text(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "cardと島の間に線があるか",
                "candidate_relation_between": ["C01", "G02"],
            }
        ]

        rendered = render_group_map(data)

        self.assertIn('C01["C01｜カード1"]', rendered)
        self.assertIn('C01 -.->|"candidate endpoint / not asserted relation"| Q01', rendered)

    def test_explicit_relation_card_endpoint_is_declared_with_text(self) -> None:
        data = self.base_map()
        data["relations"] = [
            {
                "id": "R01",
                "from": "C01",
                "to": "G02",
                "direction": "directed",
                "predicate": "具体が島2を制約する",
            }
        ]

        rendered = render_group_map(data)

        self.assertIn('C01["C01｜カード1"]', rendered)
        self.assertIn('C01 -->|"R01｜具体が島2を制約する"| G02', rendered)

    def test_candidate_endpoint_and_question_provenance_share_one_edge(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "関係候補",
                "arises_from": ["G01"],
                "candidate_relation_between": ["G01", "G02"],
            }
        ]

        rendered = render_group_map(data)

        combined = (
            'G01 -.->|"candidate endpoint + question provenance / not asserted relation"| Q01'
        )
        self.assertIn(combined, rendered)
        self.assertEqual(rendered.count("G01 -.->"), 1)
        self.assertIn('G02 -.->|"candidate endpoint / not asserted relation"| Q01', rendered)

    def test_plain_question_provenance_stays_distinct_from_relation_candidate(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "島1から生じた問い",
                "arises_from": ["G01"],
            }
        ]

        rendered = render_group_map(data)

        self.assertIn(
            'G01 -.->|"question provenance / not asserted relation"| Q01',
            rendered,
        )
        self.assertNotIn("candidate endpoint", rendered)


if __name__ == "__main__":
    unittest.main()
