from __future__ import annotations

import hashlib
import json
import posixpath
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ADAPTERS = ROOT / "adapters"
DIST = ROOT / "dist"
PLUGINS = ROOT / "plugins"
RELEASE_REPORT_PATHS = (
    "reports/validation-report.json",
    "reports/token-budget.json",
    "reports/living-lab-observation-summary.json",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def _run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"git {' '.join(args)} failed: {exc}") from exc
    return result.stdout.strip()


def git_head(root: Path = ROOT) -> str:
    value = _run_git(root, "rev-parse", "HEAD")
    if not value:
        raise RuntimeError("cannot resolve git HEAD: empty result")
    return value


def git_worktree_changes(root: Path = ROOT) -> str:
    return _run_git(root, "status", "--porcelain")


def manifest():
    return read_json(SRC / "manifest.json")


def locales() -> list[str]:
    return list(manifest()["locales"].keys())


def locale_source(locale: str) -> Path:
    return SRC / locale


def clean_generated() -> None:
    for path in (DIST, PLUGINS, ROOT / ".claude-plugin", ROOT / ".agents"):
        if path.exists():
            shutil.rmtree(path)
    DIST.mkdir(parents=True)
    PLUGINS.mkdir(parents=True)


def replace_router_links(router: str, modules: list[dict], prefix: str = "references/") -> str:
    output = router
    for module in modules:
        output = output.replace(module["source"], prefix + module["skill_reference"])
    return output


def project_reference_links(text: str, modules: list[dict], source_relative: str) -> str:
    """Render source-root pointers and local Markdown links in flat references."""
    names = {module["source"]: module["skill_reference"] for module in modules}
    for module in modules:
        for alias in module.get("aliases", []):
            names[alias] = module["skill_reference"]

    def local_link(match: re.Match) -> str:
        target = match.group(1)
        path, separator, anchor = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_relative), path))
        replacement = names.get(path, names.get(resolved))
        return "](" + (replacement + separator + anchor if replacement else target) + ")"

    output = re.sub(r"\]\(([^)]+)\)", local_link, text)
    pattern = r"(?<![A-Za-z0-9_./-])(" + "|".join(re.escape(name) for name in sorted(names, key=len, reverse=True)) + r")(?=$|[\s`),;.!?\]])"
    return re.sub(pattern, lambda match: names[match.group(1)], output)


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def locale_heading(locale: str) -> str:
    return {
        "ja-JP": "## 参照ファイルを選ぶ",
        "en-US": "## Select reference files",
    }[locale]


def locale_short(locale: str) -> str:
    return {"ja-JP": "ja", "en-US": "en"}[locale]
