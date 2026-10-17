from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "research" / "framework-candidates" / "scripts"
TARGET = ROOT / "research" / "framework-candidates" / "trials" / "requirements-review-target-v1.json"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("record_trial_response", SCRIPTS / "record_trial_response.py")
assert spec is not None and spec.loader is not None
record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(record)


class RecordTrialResponseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.target = json.loads(TARGET.read_text(encoding="utf-8"))
        self.response = "権限と更新競合を確認します。\n"

    def make_record(self, **changes: str) -> dict:
        options = {
            "phase": "unprimed-baseline",
            "response_reference": "raw-round-1.md",
            "method_as_reported": "requirements review",
            "exposure_as_reported": "unknown",
        }
        options.update(changes)
        return record.response_record(self.target, self.response, **options)

    def test_records_hashes_not_text_or_automatic_verdict(self) -> None:
        output = self.make_record()
        self.assertEqual(output["format"], "csw.precontact-review-observation/v1")
        self.assertEqual(output["status"], "raw-response-captured-unassessed")
        self.assertEqual(
            output["response_sha256"],
            hashlib.sha256(self.response.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(len(output["target_visible_sha256"]), 64)
        self.assertEqual(output["raw_response_reference"], "raw-round-1.md")
        encoded = json.dumps(output, ensure_ascii=False)
        self.assertNotIn("権限と更新競合", encoded)
        self.assertNotIn("discovery_score", encoded)
        self.assertNotIn("approved", encoded)

    def test_metadata_is_not_exposed_in_target_hash(self) -> None:
        original = self.make_record()["target_visible_sha256"]
        changed = copy.deepcopy(self.target)
        changed["internal_research_context"] = "private metadata changed"
        self.target = changed
        self.assertEqual(original, self.make_record()["target_visible_sha256"])
        changed["provided_information"][0] += " 追加"
        self.assertNotEqual(original, self.make_record()["target_visible_sha256"])

    def test_exposure_is_self_report_only(self) -> None:
        output = self.make_record(exposure_as_reported="reported-none")
        self.assertEqual(output["exposure_as_reported"], "reported-none")
        self.assertIn("not verified", output["interpretation_boundary"])

    def test_invalid_record_is_rejected(self) -> None:
        for kwargs in (
            {"phase": "not-an-arm"},
            {"exposure_as_reported": "verified-independent"},
            {"response_reference": " "},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.make_record(**kwargs)
        with self.assertRaises(ValueError):
            record.response_record(
                self.target, " ", phase="unprimed-baseline",
                response_reference="x", method_as_reported="",
                exposure_as_reported="unknown",
            )

    def test_cli_preserves_raw_file_and_reports_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            response_path = Path(tmp) / "response.md"
            output_path = Path(tmp) / "record.json"
            response_path.write_text(self.response, encoding="utf-8")
            subprocess.run(
                [
                    sys.executable, str(SCRIPTS / "record_trial_response.py"),
                    str(TARGET), str(response_path), "--phase", "unprimed-baseline",
                    "--method-as-reported", "ordinary requirements review",
                    "--output", str(output_path),
                ],
                check=True, capture_output=True, text=True,
            )
            output = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(output["phase"], "unprimed-baseline")
            self.assertEqual(output["method_as_reported"], "ordinary requirements review")
            self.assertEqual(output["response_sha256"], hashlib.sha256(self.response.encode()).hexdigest())
            self.assertEqual(response_path.read_text(encoding="utf-8"), self.response)


if __name__ == "__main__":
    unittest.main()
