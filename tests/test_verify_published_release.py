from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERIFIER = load_script("verify_published_release")
VALIDATION_NOTE = "**Validation status / 検証状況**\n\nRequired disclosure."


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PublishedReleaseVerificationTests(unittest.TestCase):
    TAG = "v9.9.9"

    def build_fixture(self, root: Path) -> tuple[Path, Path]:
        dist = root / "dist"
        report = dist / "reports" / "validation-report.json"
        report.parent.mkdir(parents=True)
        report.write_text('{"ok": true}\n', encoding="utf-8")

        report_bytes = report.read_bytes()
        manifest = dist / "release-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": "2",
                    "version": "9.9.9",
                    "source_commit": "1" * 40,
                    "locales": ["ja-JP", "en-US"],
                    "files": [
                        {
                            "path": "reports/validation-report.json",
                            "bytes": len(report_bytes),
                            "sha256": sha256_bytes(report_bytes),
                        }
                    ],
                    "release_assets": [
                        "release-manifest.json",
                        "reports/validation-report.json",
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        release_json = root / "release.json"
        release_json.write_text(
            json.dumps(
                {
                    "tag_name": self.TAG,
                    "draft": False,
                    "prerelease": False,
                    "body": VALIDATION_NOTE + "\n\n## What's Changed\n\n- Example change.",
                    "assets": [
                        {
                            "name": "release-manifest.json",
                            "state": "uploaded",
                            "size": manifest.stat().st_size,
                            "digest": f"sha256:{VERIFIER.file_sha256(manifest)}",
                        },
                        {
                            "name": "validation-report.json",
                            "state": "uploaded",
                            "size": len(report_bytes),
                            "digest": f"sha256:{sha256_bytes(report_bytes)}",
                        },
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return manifest, release_json

    def validate(self, manifest: Path, release_json: Path, tag: str | None = None) -> list[str]:
        return VERIFIER.validate_published_release(
            manifest,
            release_json,
            tag or self.TAG,
            VALIDATION_NOTE,
        )

    def test_exact_published_asset_set_digests_and_disclosure_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            self.assertEqual(self.validate(manifest, release_json), [])

    def test_extra_published_asset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["assets"].append(
                {
                    "name": "manual-extra.txt",
                    "state": "uploaded",
                    "size": 1,
                    "digest": f"sha256:{'0' * 64}",
                }
            )
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("undeclared assets" in error for error in errors))

    def test_digest_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["assets"][1]["digest"] = f"sha256:{'f' * 64}"
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("digest mismatch" in error for error in errors))

    def test_missing_asset_and_wrong_tag_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["tag_name"] = "v0.0.0"
            data["assets"] = data["assets"][:1]
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("tag mismatch" in error for error in errors))
            self.assertTrue(any("missing manifest-declared assets" in error for error in errors))

    def test_same_wrong_tag_cannot_bypass_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            wrong_tag = "v9.9.8"
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["tag_name"] = wrong_tag
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json, wrong_tag)
            self.assertTrue(any("release tag mismatch" in error for error in errors))

    def test_missing_validation_disclosure_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["body"] = "## What's Changed\n\n- Example change."
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("missing the required validation disclosure" in error for error in errors))

    def test_draft_release_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["draft"] = True
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("must not be a draft" in error for error in errors))

    def test_prerelease_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["prerelease"] = True
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = self.validate(manifest, release_json)
            self.assertTrue(any("must not be a prerelease" in error for error in errors))

    def test_validation_note_line_endings_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["body"] = data["body"].replace("\n", "\r\n")
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            self.assertEqual(self.validate(manifest, release_json), [])


if __name__ == "__main__":
    unittest.main()
