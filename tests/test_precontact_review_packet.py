from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research" / "framework-candidates" / "scripts" / "precontact_review_packet.py"
TARGET = ROOT / "research" / "framework-candidates" / "trials" / "requirements-review-target-v1.json"
spec = importlib.util.spec_from_file_location("precontact_review_packet", SCRIPT)
assert spec is not None and spec.loader is not None
packet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packet)


class PrecontactReviewPacketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(TARGET.read_text(encoding="utf-8"))

    def test_neutral_render_excludes_hidden_context_and_method_cues(self) -> None:
        result = packet.render_packet(self.source)
        self.assertIn("最新・古い・欠落", result)
        self.assertIn("最初に自然に選ぶ確認方法", result)
        self.assertIn("入力指紋（SHA-256）", result)
        frozen_packet = (
            ROOT / "research" / "framework-candidates" / "trials" / "reviewer-packet-v1.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(result, frozen_packet)
        for hidden in ("Llull", "llull", "Ars", "ars", "組合せ", "combinatorial", "framework", "internal_research_context"):
            self.assertNotIn(hidden, result)

    def test_fingerprint_only_covers_frozen_reviewer_input(self) -> None:
        original = packet.visible_target(self.source)
        baseline = packet.fingerprint(original)
        revised = copy.deepcopy(self.source)
        revised["internal_research_context"] = "changed secret metadata"
        self.assertEqual(baseline, packet.fingerprint(packet.visible_target(revised)))
        revised["provided_information"][0] += " 追加情報"
        self.assertNotEqual(baseline, packet.fingerprint(packet.visible_target(revised)))

    def test_invalid_input_rejected_without_creating_results(self) -> None:
        for key, value in (("context", ""), ("provided_information", []), ("not_provided", [""])):
            bad = copy.deepcopy(self.source)
            bad[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                packet.render_packet(bad)
        self.assertNotIn("result", packet.render_packet(self.source).lower())

    def test_marshallese_incident_packet_is_target_only(self) -> None:
        path = (
            ROOT / "research" / "framework-candidates" / "trials"
            / "marshallese-observability-target-v1.json"
        )
        source = json.loads(path.read_text(encoding="utf-8"))
        rendered = packet.render_packet(source)
        self.assertIn("O1: queue Q-A", rendered)
        self.assertIn("O7: P-X", rendered)
        self.assertIn("入力指紋（SHA-256）", rendered)
        self.assertNotIn("Marshallese", rendered)
        self.assertNotIn("wave-navigation", rendered)
        self.assertNotIn("internal_research_context", rendered)
        self.assertNotIn("航海", rendered)
        self.assertNotIn("局所的な手掛かり", rendered)
        changed = copy.deepcopy(source)
        changed["internal_research_context"] = "Different internal hypothesis"
        self.assertEqual(rendered, packet.render_packet(changed))
        self.assertNotEqual(
            packet.fingerprint(packet.visible_target(source)),
            packet.fingerprint(packet.visible_target(
                {**source, "context": source["context"] + "追記"}
            )),
        )

    def test_sankhya_dashboard_packet_hides_internal_research_context(self) -> None:
        path = (
            ROOT / "research" / "framework-candidates" / "trials"
            / "sankhya-dashboard-target-v1.json"
        )
        source = json.loads(path.read_text(encoding="utf-8"))
        rendered = packet.render_packet(source)
        self.assertIn("注文成功率", rendered)
        self.assertIn("O3: ダッシュボード", rendered)
        self.assertIn("入力指紋（SHA-256）", rendered)
        self.assertNotIn("Sankhya", rendered)
        self.assertNotIn("サーンキヤ", rendered)
        self.assertNotIn("puruṣa", rendered)
        self.assertNotIn("internal_research_context", rendered)

        revised = copy.deepcopy(source)
        revised["internal_research_context"] = "different private hypothesis"
        self.assertEqual(rendered, packet.render_packet(revised))
        revised["provided_information"][0] += " 追加"
        self.assertNotEqual(rendered, packet.render_packet(revised))

    def test_cli_writes_same_packet_without_private_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "review-request.md"
            subprocess.run(
                [sys.executable, str(SCRIPT), str(TARGET), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(output.read_text(encoding="utf-8"), packet.render_packet(self.source))


if __name__ == "__main__":
    unittest.main()
