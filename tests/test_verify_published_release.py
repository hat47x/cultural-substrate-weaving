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
                    "schema_version": "1",
                    "version": "9.9.9",
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
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return manifest, release_json

    def test_exact_published_asset_set_and_digests_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            self.assertEqual(
                VERIFIER.validate_published_release(manifest, release_json, self.TAG),
                [],
            )

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

            errors = VERIFIER.validate_published_release(manifest, release_json, self.TAG)
            self.assertTrue(any("undeclared assets" in error for error in errors))

    def test_digest_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["assets"][1]["digest"] = f"sha256:{'f' * 64}"
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = VERIFIER.validate_published_release(manifest, release_json, self.TAG)
            self.assertTrue(any("digest mismatch" in error for error in errors))

    def test_missing_asset_and_wrong_tag_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest, release_json = self.build_fixture(Path(tmp))
            data = json.loads(release_json.read_text(encoding="utf-8"))
            data["tag_name"] = "v0.0.0"
            data["assets"] = data["assets"][:1]
            release_json.write_text(json.dumps(data) + "\n", encoding="utf-8")

            errors = VERIFIER.validate_published_release(manifest, release_json, self.TAG)
            self.assertTrue(any("tag mismatch" in error for error in errors))
            self.assertTrue(any("missing manifest-declared assets" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
