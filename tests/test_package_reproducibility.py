from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location("package_script", SCRIPTS / "package.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PackageReproducibilityTests(unittest.TestCase):
    def test_zip_tree_ignores_source_mtime_and_normalizes_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            nested = source / "nested"
            nested.mkdir(parents=True)

            plain = source / "plain.txt"
            executable = nested / "run.sh"
            plain.write_text("same content\n", encoding="utf-8")
            executable.write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
            executable.chmod(0o755)

            first = root / "first.zip"
            second = root / "second.zip"
            MODULE.zip_tree(source, first, root_name="bundle")

            os.utime(plain, (1_700_000_000, 1_700_000_000))
            os.utime(executable, (1_800_000_000, 1_800_000_000))
            MODULE.zip_tree(source, second, root_name="bundle")

            self.assertEqual(first.read_bytes(), second.read_bytes())

            with zipfile.ZipFile(first) as archive:
                infos = archive.infolist()
                self.assertEqual(
                    [info.filename for info in infos],
                    ["bundle/nested/run.sh", "bundle/plain.txt"],
                )
                for info in infos:
                    self.assertEqual(info.date_time, MODULE.ZIP_TIMESTAMP)
                    self.assertEqual(info.create_system, 3)

                modes = {info.filename: (info.external_attr >> 16) & 0o777 for info in infos}
                self.assertEqual(modes["bundle/plain.txt"], 0o644)
                self.assertEqual(modes["bundle/nested/run.sh"], 0o755)


if __name__ == "__main__":
    unittest.main()
