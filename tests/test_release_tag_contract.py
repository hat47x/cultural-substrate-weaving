from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_release_tag import (  # noqa: E402
    read_manifest_version,
    validate_release_tag,
    validate_tag_against_version,
)


class ReleaseTagContractTests(unittest.TestCase):
    def test_tag_matches_version(self) -> None:
        self.assertEqual(validate_tag_against_version("v0.5.0", "0.5.0"), [])

    def test_wrong_tag_is_rejected(self) -> None:
        errors = validate_tag_against_version("v0.5.1", "0.5.0")
        self.assertTrue(any("release tag mismatch" in error for error in errors))

    def test_malformed_tag_is_rejected(self) -> None:
        errors = validate_tag_against_version("0.5.0", "0.5.0")
        self.assertTrue(any("release tag must be vX.Y.Z" in error for error in errors))

    def test_manifest_version_mismatch_is_rejected(self) -> None:
        errors = validate_release_tag("v0.5.0", "0.5.0", "0.4.0")
        self.assertTrue(any("release manifest version mismatch" in error for error in errors))

    def test_correct_tag_version_and_manifest_pass(self) -> None:
        self.assertEqual(validate_release_tag("v0.5.0", "0.5.0", "0.5.0"), [])

    def test_reads_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            path.write_text(json.dumps({"version": "0.5.0"}) + "\n", encoding="utf-8")
            self.assertEqual(read_manifest_version(path), "0.5.0")

    def test_missing_manifest_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            path.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_manifest_version(path)


if __name__ == "__main__":
    unittest.main()
