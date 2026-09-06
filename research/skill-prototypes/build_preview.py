from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUITE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = SUITE_ROOT / "suite-manifest.json"
FRONTMATTER_NAME = re.compile(r"\A---\s*\n.*?^name:\s*([^\n]+)$.*?\n---\s*\n", re.MULTILINE | re.DOTALL)


def load_manifest() -> dict[str, Any]:
    value = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("suite manifest must be a JSON object")
    return value


def frontmatter_name(text: str) -> str | None:
    match = FRONTMATTER_NAME.match(text)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def selected_reference_paths(skill: dict[str, Any], locale: str) -> list[Path]:
    realization = skill["locale_realizations"][locale]
    selected_method = realization.get("method_definition")
    canonical_method = skill.get("method_definition")
    locale_methods = {
        str(item.get("method_definition"))
        for item in skill.get("locale_realizations", {}).values()
        if isinstance(item, dict) and item.get("method_definition")
    }

    selected: list[Path] = []
    if selected_method:
        selected.append(ROOT / str(selected_method))

    for relative in skill.get("references", []):
        relative = str(relative)
        if relative == canonical_method or relative in locale_methods:
            continue
        selected.append(ROOT / relative)

    return selected


def build_preview(output_root: Path) -> list[Path]:
    manifest = load_manifest()
    built: list[Path] = []

    for locale in manifest["locales"]:
        for skill in manifest["skills"]:
            realization = skill["locale_realizations"][locale]
            runtime = ROOT / realization["runtime_entry"]
            target = output_root / locale / skill["installable_name"]
            references = target / "references"
            references.mkdir(parents=True, exist_ok=True)

            shutil.copyfile(runtime, target / "SKILL.md")
            built.append(target)

            for source in selected_reference_paths(skill, locale):
                if not source.is_file():
                    raise FileNotFoundError(source)
                shutil.copyfile(source, references / source.name)

            origin = {
                "suite": manifest["suite_id"],
                "skill_id": skill["id"],
                "installable_name": skill["installable_name"],
                "locale": locale,
                "realization_status": realization.get("status"),
                "runtime_source": realization["runtime_entry"],
                "method_source": realization.get("method_definition"),
                "research_only": True,
            }
            (target / "ORIGIN.json").write_text(
                json.dumps(origin, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    return built


def validate_preview(output_root: Path, built: list[Path]) -> list[str]:
    errors: list[str] = []
    manifest = load_manifest()
    expected_count = len(manifest["locales"]) * len(manifest["skills"])
    if len(built) != expected_count:
        errors.append(f"preview count mismatch: expected {expected_count}, got {len(built)}")

    for target in built:
        skill_path = target / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"missing packaged SKILL.md: {skill_path.relative_to(output_root)}")
            continue

        text = skill_path.read_text(encoding="utf-8")
        name = frontmatter_name(text)
        origin_path = target / "ORIGIN.json"
        if not origin_path.is_file():
            errors.append(f"missing ORIGIN.json: {target.relative_to(output_root)}")
            continue
        origin = json.loads(origin_path.read_text(encoding="utf-8"))
        expected_name = origin["installable_name"]

        if name is not None and name != expected_name:
            errors.append(
                f"{target.relative_to(output_root)}: frontmatter name {name!r} != {expected_name!r}"
            )
        if origin.get("research_only") is not True:
            errors.append(f"{target.relative_to(output_root)}: preview lost research_only marker")

        method_source = origin.get("method_source")
        if method_source:
            expected_method_name = Path(str(method_source)).name
            if not (target / "references" / expected_method_name).is_file():
                errors.append(
                    f"{target.relative_to(output_root)}: selected locale Method Definition missing"
                )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a research-only bilingual sibling-Skill preview.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory. If omitted with --check, a temporary directory is used.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build and validate the preview without claiming release readiness.",
    )
    args = parser.parse_args()

    if args.check and args.output is None:
        with tempfile.TemporaryDirectory(prefix="csw-skill-preview-") as tmp:
            root = Path(tmp)
            built = build_preview(root)
            errors = validate_preview(root, built)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}")
                raise SystemExit(1)
            print(f"Research suite preview check passed ({len(built)} locale/skill packages)")
        return

    output = args.output or (ROOT / "dist" / "research-skill-suite")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    built = build_preview(output)

    if args.check:
        errors = validate_preview(output, built)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)

    print(f"Built research suite preview: {len(built)} locale/skill packages at {output}")


if __name__ == "__main__":
    main()
