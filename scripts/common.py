from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ADAPTERS = ROOT / "adapters"
DIST = ROOT / "dist"
PLUGINS = ROOT / "plugins"


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


def git_head(root: Path = ROOT) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot resolve git HEAD: {exc}") from exc
    value = result.stdout.strip()
    if not value:
        raise RuntimeError("cannot resolve git HEAD: empty result")
    return value


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
