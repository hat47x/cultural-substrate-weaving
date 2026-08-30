from __future__ import annotations

import json
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from common import DIST, locales, sha256, version

MANIFEST_SCHEMA_VERSION = "1"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
PACKAGE_KINDS = (
    "openai-interactive",
    "openai-metered",
    "claude-plugin",
    "chatgpt-gpt",
    "m365-copilot",
    "canonical-docs",
)
REQUIRED_REPORTS = {
    "reports/validation-report.json",
    "reports/token-budget.json",
    "reports/living-lab-observation-summary.json",
}


def expected_package_paths(expected_version: str, expected_locales: list[str]) -> set[str]:
    return {
        f"packages/cultural-substrate-weaving-{kind}-{locale}-v{expected_version}.zip"
        for locale in expected_locales
        for kind in PACKAGE_KINDS
    }


def _safe_relative_path(value: Any, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty string")
        return None
    if "\\" in value:
        errors.append(f"{label} must use POSIX separators: {value}")
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} must stay inside the release root: {value}")
        return None
    return value


def validate_zip(path: Path, label: str, errors: list[str]) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if not infos:
                errors.append(f"empty release ZIP: {label}")
                return
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                errors.append(f"duplicate members in release ZIP: {label}")
            for info in infos:
                name = _safe_relative_path(info.filename, f"{label} member", errors)
                if name is None:
                    continue
                if name.endswith("/"):
                    errors.append(f"release ZIP should contain files, not directory entries: {label} -> {name}")
                if info.date_time != ZIP_TIMESTAMP:
                    errors.append(f"non-reproducible ZIP timestamp: {label} -> {name}: {info.date_time}")
                if info.create_system != 3:
                    errors.append(f"release ZIP member is not normalized as Unix metadata: {label} -> {name}")
                raw_mode = (info.external_attr >> 16) & 0xFFFF
                if not stat.S_ISREG(raw_mode):
                    errors.append(f"release ZIP member is not a regular file: {label} -> {name}")
                if stat.S_IMODE(raw_mode) not in {0o644, 0o755}:
                    errors.append(
                        f"unexpected release ZIP permissions: {label} -> {name}: {oct(stat.S_IMODE(raw_mode))}"
                    )
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"invalid release ZIP {label}: {exc}")


def validate_release(
    dist: Path,
    expected_version: str,
    expected_locales: list[str],
) -> list[str]:
    errors: list[str] = []
    manifest_path = dist / "release-manifest.json"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read release manifest: {exc}"]

    if not isinstance(data, dict):
        return ["release manifest must be a JSON object"]
    if data.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        errors.append(
            f"release manifest schema_version mismatch: {data.get('schema_version')} != {MANIFEST_SCHEMA_VERSION}"
        )
    if data.get("version") != expected_version:
        errors.append(f"release manifest version mismatch: {data.get('version')} != {expected_version}")
    if data.get("locales") != expected_locales:
        errors.append(f"release manifest locales mismatch: {data.get('locales')} != {expected_locales}")

    raw_files = data.get("files")
    if not isinstance(raw_files, list):
        errors.append("release manifest files must be an array")
        raw_files = []

    entries: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_files):
        if not isinstance(raw, dict):
            errors.append(f"release manifest files[{index}] must be an object")
            continue
        path_value = _safe_relative_path(raw.get("path"), f"release manifest files[{index}].path", errors)
        if path_value is None:
            continue
        if path_value == "release-manifest.json":
            errors.append("release manifest must not hash itself in files")
        if path_value in entries:
            errors.append(f"duplicate release manifest file entry: {path_value}")
            continue
        entries[path_value] = raw

    actual_files = {
        path.relative_to(dist).as_posix()
        for path in dist.rglob("*")
        if path.is_file() and path != manifest_path
    }
    manifest_files = set(entries)
    if manifest_files != actual_files:
        missing = sorted(actual_files - manifest_files)
        stale = sorted(manifest_files - actual_files)
        if missing:
            errors.append(f"release manifest omits build files: {missing}")
        if stale:
            errors.append(f"release manifest references missing build files: {stale}")

    for relative, entry in entries.items():
        path = dist / relative
        if not path.is_file():
            continue
        if entry.get("bytes") != path.stat().st_size:
            errors.append(f"release manifest byte count mismatch: {relative}")
        if entry.get("sha256") != sha256(path):
            errors.append(f"release manifest sha256 mismatch: {relative}")

    raw_assets = data.get("release_assets")
    if not isinstance(raw_assets, list):
        errors.append("release manifest release_assets must be an array")
        raw_assets = []
    release_assets: list[str] = []
    for index, value in enumerate(raw_assets):
        path_value = _safe_relative_path(value, f"release_assets[{index}]", errors)
        if path_value is not None:
            release_assets.append(path_value)
    if len(release_assets) != len(set(release_assets)):
        errors.append("release_assets must not contain duplicates")

    actual_release_assets = {"release-manifest.json"}
    for root_name in ("packages", "reports"):
        root = dist / root_name
        if root.exists():
            actual_release_assets.update(
                path.relative_to(dist).as_posix()
                for path in root.glob("*")
                if path.is_file()
            )
    if set(release_assets) != actual_release_assets:
        errors.append(
            "release_assets do not match the files published by the release workflow: "
            f"manifest={sorted(set(release_assets))}, actual={sorted(actual_release_assets)}"
        )

    expected_packages = expected_package_paths(expected_version, expected_locales)
    actual_packages = {
        path.relative_to(dist).as_posix()
        for path in (dist / "packages").glob("*.zip")
        if path.is_file()
    } if (dist / "packages").exists() else set()
    if actual_packages != expected_packages:
        errors.append(
            f"release package set mismatch: expected={sorted(expected_packages)}, actual={sorted(actual_packages)}"
        )

    if not REQUIRED_REPORTS.issubset(actual_release_assets):
        errors.append(
            f"required release reports missing: {sorted(REQUIRED_REPORTS - actual_release_assets)}"
        )

    for relative in sorted(actual_packages):
        validate_zip(dist / relative, relative, errors)

    return errors


def main() -> int:
    errors = validate_release(DIST, version(), locales())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Release manifest and packages validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
