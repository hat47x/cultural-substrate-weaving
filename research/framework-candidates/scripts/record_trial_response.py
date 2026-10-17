"""Record a raw review response with input and output fingerprints.

Does not perform a review, attest independence, or decide framework efficacy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from precontact_review_packet import fingerprint, visible_target


FORMAT = "csw.precontact-review-observation/v1"
PHASES = ("unprimed-baseline", "framework-contact")
EXPOSURES = ("unknown", "reported-none", "reported-prior-contact")


def response_record(
    target: dict[str, Any],
    raw_response: bytes,
    *,
    phase: str,
    response_reference: str,
    method_as_reported: str,
    exposure_as_reported: str,
) -> dict[str, Any]:
    if phase not in PHASES:
        raise ValueError(f"phase must be one of: {', '.join(PHASES)}")
    if exposure_as_reported not in EXPOSURES:
        raise ValueError(f"exposure_as_reported must be one of: {', '.join(EXPOSURES)}")
    if not isinstance(raw_response, bytes) or not raw_response.strip():
        raise ValueError("raw response must be nonempty UTF-8 bytes")
    try:
        raw_response.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("raw response must be UTF-8 encoded") from exc
    if not isinstance(response_reference, str) or not response_reference.strip():
        raise ValueError("response_reference must identify the stored raw response")
    if not isinstance(method_as_reported, str):
        raise ValueError("method_as_reported must be a string")

    return {
        "format": FORMAT,
        "status": "raw-response-captured-unassessed",
        "phase": phase,
        "target_visible_sha256": fingerprint(visible_target(target)),
        "response_sha256": hashlib.sha256(raw_response).hexdigest(),
        "raw_response_reference": response_reference,
        "method_as_reported": method_as_reported,
        "exposure_as_reported": exposure_as_reported,
        "interpretation_boundary": (
            "Hashes identify bytes, not reviewer independence or task validity. "
            "Reported exposure is not verified. This record does not establish "
            "additional discovery, target-side support, causation, efficacy, "
            "framework activation, or a retention/demotion decision."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="frozen target JSON")
    parser.add_argument("response", type=Path, help="original plain-text response")
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--method-as-reported", default="")
    parser.add_argument("--exposure-as-reported", choices=EXPOSURES, default="unknown")
    parser.add_argument("--output", type=Path, help="where to write a JSON metadata record")
    args = parser.parse_args()

    target = json.loads(args.target.read_text(encoding="utf-8"))
    raw_bytes = args.response.read_bytes()
    payload = response_record(
        target,
        raw_bytes,
        phase=args.phase,
        response_reference=str(args.response),
        method_as_reported=args.method_as_reported,
        exposure_as_reported=args.exposure_as_reported,
    )
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
