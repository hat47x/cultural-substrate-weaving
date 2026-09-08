from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research/skill-prototypes/affinity-synthesis/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_spatial_svg import render  # noqa: E402


class ResearchAffinitySpatialProjectionTests(unittest.TestCase):
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
            "layout": {
                "projection": "spatial-map",
                "positions": {
                    "G01": {"x": 0.2, "y": 0.35},
                    "G02": {"x": 0.75, "y": 0.35},
                    "Q01": {"x": 0.5, "y": 0.72},
                    "C01": {"x": 0.2, "y": 0.72},
                },
            },
        }

    def test_group_candidate_relation_uses_q_audit_links_without_solid_relation(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "二つの島に接続があるか",
                "candidate_relation_between": ["G01", "G02"],
            }
        ]

        svg = render(data)

        self.assertEqual(svg.count("candidate endpoint / not asserted relation"), 2)
        self.assertNotIn("marker-end=\"url(#arrow)\"", svg)
        self.assertIn("candidate endpoints are never connected directly", svg)

    def test_candidate_card_with_position_is_rendered_as_compact_endpoint(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "cardと島に接続があるか",
                "candidate_relation_between": ["C01", "G02"],
            }
        ]

        svg = render(data)

        self.assertIn(">C01</text>", svg)
        self.assertIn(">カード1</text>", svg)
        self.assertEqual(svg.count("candidate endpoint / not asserted relation"), 2)

    def test_candidate_card_without_position_is_omitted_not_given_invented_geometry(self) -> None:
        data = self.base_map()
        data["layout"]["positions"].pop("C01")
        data["questions"] = [
            {
                "id": "Q01",
                "text": "cardと島に接続があるか",
                "candidate_relation_between": ["C01", "G02"],
            }
        ]

        svg = render(data)

        self.assertNotIn(">C01</text>", svg)
        self.assertEqual(svg.count("candidate endpoint / not asserted relation"), 1)
        self.assertIn(">G02</text>", svg)

    def test_candidate_and_provenance_share_one_audit_link(self) -> None:
        data = self.base_map()
        data["questions"] = [
            {
                "id": "Q01",
                "text": "接続候補",
                "arises_from": ["G01"],
                "candidate_relation_between": ["G01", "G02"],
            }
        ]

        svg = render(data)

        self.assertEqual(
            svg.count("candidate endpoint + question provenance / not asserted relation"),
            1,
        )
        self.assertEqual(svg.count("candidate endpoint / not asserted relation"), 1)
        self.assertEqual(svg.count('stroke-dasharray="7 6"'), 2)

    def test_explicit_relation_card_endpoint_with_position_gets_solid_relation(self) -> None:
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

        svg = render(data)

        self.assertIn(">C01</text>", svg)
        self.assertIn("R01｜具体が島2を制約する", svg)
        self.assertIn('marker-end="url(#arrow)"', svg)


if __name__ == "__main__":
    unittest.main()
