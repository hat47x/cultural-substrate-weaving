"""Audit trial input/response provenance without judging cognitive discovery.

Compare a baseline record and framework-contact record against exact response bytes.
This tool does not establish reviewer independence, chronological order or efficacy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from precontact_review_packet import fingerprint, visible_target
from record_trial_response import EXPOSURES, FORMAT as RECORD_FORMAT


FORMAT = "csw.precontact-review-pair-audit/v1"
EXPECTED_STATUS = "raw-response-captured-unassessed"


def _inspect(
    target_sha256: str,
    record: dict[str, Any],
    raw: bytes,
    expected_phase: str,
) -> dict[str, Any]:
    issues: list[str] = []
    if record.get("format") != RECORD_FORMAT:
        issues.append("unexpected-record-format")
    if record.get("status") != EXPECTED_STATUS:
        issues.append("unexpected-record-status")
    if record.get("phase") != expected_phase:
        issues.append("phase-mismatch")
    if record.get("target_visible_sha256") != target_sha256:
        issues.append("target-fingerprint-mismatch")
    raw_hash = hashlib.sha256(raw).hexdigest()
    if record.get("response_sha256") != raw_hash:
        issues.append("response-bytes-mismatch")
    try:
        if not raw.strip():
            issues.append("empty-response")
        raw.decode("utf-8")
    except UnicodeDecodeError:
        issues.append("non-utf8-response")
    if not isinstance(record.get("raw_response_reference"), str) or not record[
        "raw_response_reference"
    ].strip():
        issues.append("missing-response-reference")
    if not isinstance(record.get("method_as_reported"), str):
        issues.append("invalid-method-as-reported")
    if record.get("exposure_as_reported") not in EXPOSURES:
        issues.append("invalid-exposure-as-reported")

    return {
        "phase": expected_phase,
        "recorded_phase": record.get("phase"),
        "response_sha256": raw_hash,
        "reported_method": record.get("method_as_reported"),
        "reported_exposure": record.get("exposure_as_reported"),
        "trace_issues": issues,
    }


def audit_pair(
    target: dict[str, Any],
    baseline_record: dict[str, Any],
    baseline_response: bytes,
    contact_record: dict[str, Any],
    contact_response: bytes,
) -> dict[str, Any]:
    target_sha256 = fingerprint(visible_target(target))
    baseline = _inspect(
        target_sha256, baseline_record, baseline_response, "unprimed-baseline"
    )
    contact = _inspect(
        target_sha256, contact_record, contact_response, "framework-contact"
    )

    cautions: list[str] = []
    if baseline["reported_exposure"] == "reported-prior-contact":
        cautions.append("baseline-self-reports-prior-framework-contact")
    if baseline["reported_exposure"] == "unknown":
        cautions.append("baseline-prior-exposure-unknown")
    if not (baseline["reported_method"] or "").strip():
        cautions.append("baseline-method-not-reported")
    if not (contact["reported_method"] or "").strip():
        cautions.append("contact-method-not-reported")
    if baseline["response_sha256"] == contact["response_sha256"]:
        cautions.append("identical-response-bytes")
    if (
        baseline_record.get("raw_response_reference")
        == contact_record.get("raw_response_reference")
    ):
        cautions.append("same-raw-response-reference")

    # Provenance completeness is not a proxy for experimental independence.
    trace_complete = not baseline["trace_issues"] and not contact["trace_issues"]
    return {
        "format": FORMAT,
        "status": "trace-complete" if trace_complete else "trace-incomplete",
        "target_visible_sha256": target_sha256,
        "baseline": baseline,
        "framework_contact": contact,
        "review_cautions": cautions,
        "interpretation_boundary": (
            "Complete hashes and phase labels establish limited record consistency, "
            "not chronological sealing, blind assignment, independent reviewers, "
            "new questions, target support, benefit, or a framework retention decision. "
            "No semantic equivalence or discovery score is calculated. "
            "Unreported exposure is not evidence of no prior contact."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--baseline-record", type=Path, required=True)
    parser.add_argument("--baseline-response", type=Path, required=True)
    parser.add_argument("--contact-record", type=Path, required=True)
    parser.add_argument("--contact-response", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit_pair(
        json.loads(args.target.read_text(encoding="utf-8")),
        json.loads(args.baseline_record.read_text(encoding="utf-8")),
        args.baseline_response.read_bytes(),
        json.loads(args.contact_record.read_text(encoding="utf-8")),
        args.contact_response.read_bytes(),
    )
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
