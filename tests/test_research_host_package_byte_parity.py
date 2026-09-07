from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_host_package import materialize_host_package  # noqa: E402


def tree_bytes(root: Path, *, excluded_suffixes: tuple[str, ...] = ()) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if any(relative.endswith(suffix) for suffix in excluded_suffixes):
            continue
        result[relative] = path.read_bytes()
    return result


class ResearchHostPackageByteParityTests(unittest.TestCase):
    def test_openai_profiles_share_identical_skill_tree_bytes_in_both_locales(self) -> None:
        for locale in ("ja-JP", "en-US"):
            with self.subTest(locale=locale):
                with tempfile.TemporaryDirectory() as temp_dir:
                    base = Path(temp_dir)
                    interactive = base / "interactive"
                    metered = base / "metered"

                    materialize_host_package(
                        locale=locale,
                        distribution_name="openai_skill",
                        profile="interactive",
                        output_root=interactive,
                        root=ROOT,
                    )
                    materialize_host_package(
                        locale=locale,
                        distribution_name="openai_skill",
                        profile="metered",
                        output_root=metered,
                        root=ROOT,
                    )

                    self.assertEqual(
                        tree_bytes(interactive, excluded_suffixes=("agents/openai.yaml",)),
                        tree_bytes(metered, excluded_suffixes=("agents/openai.yaml",)),
                    )

    def test_openai_metadata_is_byte_identical_to_declared_source_in_both_locales(self) -> None:
        for locale in ("ja-JP", "en-US"):
            for profile in ("interactive", "metered"):
                with self.subTest(locale=locale, profile=profile):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        output = Path(temp_dir) / "package"
                        result = materialize_host_package(
                            locale=locale,
                            distribution_name="openai_skill",
                            profile=profile,
                            output_root=output,
                            root=ROOT,
                        )

                        self.assertEqual(len(result["host_files"]), 3)
                        for host_file in result["host_files"]:
                            self.assertEqual(host_file["action"], "copy")
                            source = ROOT / host_file["source"]
                            packaged = output / host_file["target"]
                            self.assertEqual(packaged.read_bytes(), source.read_bytes())

    def test_claude_and_codex_share_identical_skill_tree_bytes_in_both_locales(self) -> None:
        for locale in ("ja-JP", "en-US"):
            with self.subTest(locale=locale):
                with tempfile.TemporaryDirectory() as temp_dir:
                    base = Path(temp_dir)
                    claude = base / "claude"
                    codex = base / "codex"

                    materialize_host_package(
                        locale=locale,
                        distribution_name="claude_plugin",
                        output_root=claude,
                        root=ROOT,
                    )
                    materialize_host_package(
                        locale=locale,
                        distribution_name="codex_plugin",
                        output_root=codex,
                        root=ROOT,
                    )

                    self.assertEqual(
                        tree_bytes(claude / "skills"),
                        tree_bytes(codex / "skills"),
                    )


if __name__ == "__main__":
    unittest.main()
