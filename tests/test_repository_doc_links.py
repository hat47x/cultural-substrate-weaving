from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "data:")


def repository_docs() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "README.en.md", ROOT / "AGENTS.md"]
    paths.extend(sorted((ROOT / "docs").rglob("*.md")))
    paths.extend(sorted((ROOT / "research").rglob("*.md")))
    paths.append(ROOT / ".living-lab" / "README.md")
    return [path for path in paths if path.is_file()]


def local_link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip().strip("<>")
        if not target or target.startswith("#") or target.startswith(EXTERNAL_PREFIXES):
            continue
        targets.append(target)
    return targets


class RepositoryDocumentationLinkTests(unittest.TestCase):
    def test_local_documentation_links_resolve_inside_repository(self) -> None:
        failures: list[str] = []
        for source in repository_docs():
            text = source.read_text(encoding="utf-8")
            for target in local_link_targets(text):
                path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not path_part:
                    continue
                resolved = (source.parent / path_part).resolve()
                if not resolved.is_relative_to(ROOT.resolve()):
                    failures.append(
                        f"{source.relative_to(ROOT)}: link escapes repository: {target}"
                    )
                    continue
                if not resolved.exists():
                    failures.append(
                        f"{source.relative_to(ROOT)}: missing local target: {target}"
                    )
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
