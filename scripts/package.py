from __future__ import annotations

import json
import zipfile
from pathlib import Path

from common import DIST, ROOT, locale_short, locales, manifest, sha256, version, write_text


def zip_tree(source: Path, target: Path, root_name: str | None = None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            relative = path.relative_to(source)
            arcname = Path(root_name) / relative if root_name else relative
            archive.write(path, arcname=str(arcname))


def main() -> None:
    config = manifest()
    packages = DIST / "packages"
    packages.mkdir(parents=True, exist_ok=True)
    v = version()

    for locale in locales():
        suffix = locale
        targets = [
            (DIST / locale / "openai-skill/interactive",
             packages / f"cultural-substrate-weaving-openai-interactive-{suffix}-v{v}.zip", None),
            (DIST / locale / "openai-skill/metered",
             packages / f"cultural-substrate-weaving-openai-metered-{suffix}-v{v}.zip", None),
            (DIST / locale / "claude-plugin",
             packages / f"cultural-substrate-weaving-claude-plugin-{suffix}-v{v}.zip", None),
            (DIST / locale / "chatgpt-gpt",
             packages / f"cultural-substrate-weaving-chatgpt-gpt-{suffix}-v{v}.zip",
             f"cultural-substrate-weaving-gpt-{locale_short(locale)}"),
            (DIST / locale / "microsoft-copilot",
             packages / f"cultural-substrate-weaving-m365-copilot-{suffix}-v{v}.zip",
             f"cultural-substrate-weaving-m365-{locale_short(locale)}"),
            (DIST / locale / "canonical-docs",
             packages / f"cultural-substrate-weaving-canonical-docs-{suffix}-v{v}.zip",
             f"cultural-substrate-weaving-{locale_short(locale)}"),
        ]
        for source, target, root_name in targets:
            zip_tree(source, target, root_name)
            print(target)

    files = []
    for path in sorted(p for p in DIST.rglob("*") if p.is_file() and p.name != "release-manifest.json"):
        files.append({
            "path": str(path.relative_to(DIST)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    write_text(
        DIST / "release-manifest.json",
        json.dumps({"version": v, "locales": locales(), "files": files}, ensure_ascii=False, indent=2) + "\n",
    )


if __name__ == "__main__":
    main()
