from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
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


PACKAGE = load_script("package")
VALIDATOR = load_script("validate_release")


class ReleaseManifestTests(unittest.TestCase):
    VERSION = "9.9.9"
    LOCALES = ["ja-JP", "en-US"]

    def build_valid_release(self, root: Path) -> Path:
        dist = root / "dist"
        source = root / "source"
        source.mkdir(parents=True)
        (source / "payload.txt").write_text("payload\n", encoding="utf-8")

        internal = dist / "ja-JP" / "generated" / "internal.txt"
        internal.parent.mkdir(parents=True)
        internal.write_text("build provenance\n", encoding="utf-8")

        for report in VALIDATOR.REQUIRED_REPORTS:
            path = dist / report
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")

        for relative in VALIDATOR.expected_package_paths(self.VERSION, self.LOCALES):
            PACKAGE.zip_tree(source, dist / relative)

        files = []
        manifest_path = dist / "release-manifest.json"
        for path in sorted(p for p in dist.rglob("*") if p.is_file() and p != manifest_path):
            files.append(
                {
                    "path": path.relative_to(dist).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": VALIDATOR.sha256(path),
                }
            )

        release_assets = ["release-manifest.json"] + sorted(
            path.relative_to(dist).as_posix()
            for root_name in ("packages", "reports")
            for path in (dist / root_name).glob("*")
            if path.is_file()
        )
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": VALIDATOR.MANIFEST_SCHEMA_VERSION,
                    "version": self.VERSION,
                    "locales": self.LOCALES,
                    "files": files,
                    "release_assets": release_assets,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return dist

    def test_valid_release_contract_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dist = self.build_valid_release(Path(temp_dir))
            self.assertEqual(
                VALIDATOR.validate_release(dist, self.VERSION, self.LOCALES),
                [],
            )

            manifest = json.loads((dist / "release-manifest.json").read_text(encoding="utf-8"))
            self.assertNotIn("ja-JP/generated/internal.txt", manifest["release_assets"])
            self.assertIn("ja-JP/generated/internal.txt", {item["path"] for item in manifest["files"]})

    def test_tampered_file_breaks_manifest_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dist = self.build_valid_release(Path(temp_dir))
            target = dist / "reports" / "validation-report.json"
            target.write_text("tampered\n", encoding="utf-8")
            errors = VALIDATOR.validate_release(dist, self.VERSION, self.LOCALES)
            self.assertTrue(any("sha256 mismatch" in error for error in errors), errors)

    def test_missing_package_breaks_package_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dist = self.build_valid_release(Path(temp_dir))
            missing = dist / sorted(VALIDATOR.expected_package_paths(self.VERSION, self.LOCALES))[0]
            missing.unlink()
            errors = VALIDATOR.validate_release(dist, self.VERSION, self.LOCALES)
            self.assertTrue(any("package set mismatch" in error for error in errors), errors)

    def test_unsafe_zip_member_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("../escape.txt", "bad")
            errors: list[str] = []
            VALIDATOR.validate_zip(path, "unsafe.zip", errors)
            self.assertTrue(any("stay inside the release root" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
