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
SCRIPTS = ROOT / "research" / "framework-candidates" / "scripts"
TARGET = ROOT / "research" / "framework-candidates" / "trials" / "requirements-review-target-v1.json"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = load_module("audit_trial_pair")
record = load_module("record_trial_response")


class TrialPairAuditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.target = json.loads(TARGET.read_text(encoding="utf-8"))
        # These are synthetic bytes only, not independent review observations.
        self.baseline = "確認する権限の条件は何か。\n".encode("utf-8")
        self.contact = "未検討の条件の組合せはあるか。\n".encode("utf-8")
        self.base_record = record.response_record(
            self.target, self.baseline, phase="unprimed-baseline",
            response_reference="raw/baseline.md",
            method_as_reported="ordinary requirements review",
            exposure_as_reported="reported-none",
        )
        self.contact_record = record.response_record(
            self.target, self.contact, phase="framework-contact",
            response_reference="raw/contact.md",
            method_as_reported="late Ars contact",
            exposure_as_reported="reported-prior-contact",
        )

    def run_audit(self):
        return audit.audit_pair(
            self.target, self.base_record, self.baseline,
            self.contact_record, self.contact,
        )

    def test_trace_complete_is_not_discovery_verdict(self) -> None:
        result = self.run_audit()
        self.assertEqual(result["format"], "csw.precontact-review-pair-audit/v1")
        self.assertEqual(result["status"], "trace-complete")
        self.assertEqual(result["baseline"]["trace_issues"], [])
        self.assertEqual(result["framework_contact"]["trace_issues"], [])
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("確認する権限", serialized)
        self.assertNotIn("未検討の条件", serialized)
        self.assertNotIn('"discovery_score"', serialized)
        self.assertIn("not chronological sealing", result["interpretation_boundary"])

    def test_raw_response_tampering_is_detected(self) -> None:
        self.baseline = b"changed"
        result = self.run_audit()
        self.assertEqual(result["status"], "trace-incomplete")
        self.assertIn("response-bytes-mismatch", result["baseline"]["trace_issues"])

    def test_target_change_and_phase_conflict_are_detected(self) -> None:
        self.target["provided_information"][0] += " 改変"
        self.contact_record["phase"] = "unprimed-baseline"
        result = self.run_audit()
        self.assertEqual(result["status"], "trace-incomplete")
        self.assertIn("target-fingerprint-mismatch", result["baseline"]["trace_issues"])
        self.assertIn("target-fingerprint-mismatch", result["framework_contact"]["trace_issues"])
        self.assertIn("phase-mismatch", result["framework_contact"]["trace_issues"])

    def test_prior_exposure_and_duplicate_response_are_cautions(self) -> None:
        self.base_record["exposure_as_reported"] = "reported-prior-contact"
        self.base_record["raw_response_reference"] = "raw/contact.md"
        self.contact = self.baseline
        self.contact_record["response_sha256"] = self.base_record["response_sha256"]
        result = self.run_audit()
        self.assertEqual(result["status"], "trace-complete")
        self.assertIn("baseline-self-reports-prior-framework-contact", result["review_cautions"])
        self.assertIn("identical-response-bytes", result["review_cautions"])
        self.assertIn("same-raw-response-reference", result["review_cautions"])

    def test_missing_method_and_unknown_exposure_remain_explicit(self) -> None:
        self.base_record["method_as_reported"] = []
        self.base_record["exposure_as_reported"] = "unknown"
        result = self.run_audit()
        self.assertEqual(result["status"], "trace-incomplete")
        self.assertIn("invalid-method-as-reported", result["baseline"]["trace_issues"])
        self.assertIn("baseline-method-not-reported", result["review_cautions"])
        self.assertIn("baseline-prior-exposure-unknown", result["review_cautions"])

    def test_cli_reads_raw_bytes_and_stays_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            base_bytes = base / "baseline.md"
            contact_bytes = base / "contact.md"
            base_record = base / "baseline.json"
            contact_record = base / "contact.json"
            target_path = base / "target.json"
            target_path.write_text(json.dumps(self.target), encoding="utf-8")
            base_bytes.write_bytes(self.baseline)
            contact_bytes.write_bytes(self.contact)
            base_record.write_text(json.dumps(self.base_record), encoding="utf-8")
            contact_record.write_text(json.dumps(self.contact_record), encoding="utf-8")
            args = [
                sys.executable, str(SCRIPTS / "audit_trial_pair.py"),
                "--target", str(target_path),
                "--baseline-record", str(base_record),
                "--baseline-response", str(base_bytes),
                "--contact-record", str(contact_record),
                "--contact-response", str(contact_bytes),
            ]
            output = subprocess.run(args, check=True, capture_output=True, text=True)
            parsed = json.loads(output.stdout)
            self.assertEqual(parsed, self.run_audit())
            self.assertEqual(base_bytes.read_bytes(), self.baseline)
            self.assertEqual(contact_bytes.read_bytes(), self.contact)


if __name__ == "__main__":
    unittest.main()
