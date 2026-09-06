from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUITE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = SUITE_ROOT / "suite-manifest.json"
PLANNER_DIR = SUITE_ROOT / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from plan_build_descriptors import plan_build_descriptors  # noqa: E402

FRONTMATTER_NAME = re.compile(
    r"\A---\s*\n.*?^name:\s*([^\n]+)$.*?\n---\s*\n",
    re.MULTILINE | re.DOTALL,
)
LOCAL_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_manifest() -> dict[str, Any]:
    return load_json(MANIFEST_PATH)


def frontmatter_name(text: str) -> str | None:
    match = FRONTMATTER_NAME.match(text)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def write_origin(
    target: Path,
    manifest: dict[str, Any],
    descriptor: dict[str, Any],
    packaging_mode: str,
) -> None:
    origin = {
        "suite": manifest["suite_id"],
        "skill_id": descriptor["skill_id"],
        "installable_name": descriptor["installable_name"],
        "locale": descriptor["locale"],
        "realization_status": descriptor.get("realization_status"),
        "runtime_source": descriptor.get("runtime_source"),
        "method_source": descriptor.get("method_source"),
        "package_reference_sources": descriptor.get("package_reference_sources", []),
        "assembly_mode": descriptor.get("assembly_mode"),
        "source_manifest": descriptor.get("source_manifest"),
        "packaging_mode": packaging_mode,
        "research_only": True,
    }
    (target / "ORIGIN.json").write_text(
        json.dumps(origin, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_router_modules_preview(
    output_root: Path,
    manifest: dict[str, Any],
    descriptor: dict[str, Any],
) -> Path:
    locale = descriptor["locale"]
    source_manifest_value = descriptor.get("source_manifest")
    if not isinstance(source_manifest_value, str):
        raise ValueError(f"{descriptor['skill_id']} {locale} has no source_manifest")
    source_manifest_path = ROOT / source_manifest_value
    source_manifest = load_json(source_manifest_path)

    runtime_value = descriptor.get("runtime_source")
    if not isinstance(runtime_value, str):
        raise ValueError(f"{descriptor['skill_id']} {locale} has no runtime_source")
    runtime = ROOT / runtime_value

    target = output_root / locale / descriptor["installable_name"]
    references = target / "references"
    references.mkdir(parents=True, exist_ok=True)

    router = runtime.read_text(encoding="utf-8")
    for module in source_manifest["modules"]:
        router = router.replace(
            f"({module['source']})",
            f"(references/{module['skill_reference']})",
        )

    description = source_manifest["locales"][locale]["description"].replace("\n", " ").strip()
    skill_text = (
        "---\n"
        f"name: {descriptor['installable_name']}\n"
        f"description: {description}\n"
        "---\n\n"
        + router
    )
    (target / "SKILL.md").write_text(skill_text, encoding="utf-8")

    source_root = ROOT / descriptor["source_root"] / locale
    for module in source_manifest["modules"]:
        source = source_root / module["source"]
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copyfile(source, references / module["skill_reference"])

    write_origin(target, manifest, descriptor, "router-modules-research-preview")
    return target


def build_direct_skill_preview(
    output_root: Path,
    manifest: dict[str, Any],
    descriptor: dict[str, Any],
) -> Path:
    locale = descriptor["locale"]
    runtime_value = descriptor.get("runtime_source")
    if not isinstance(runtime_value, str):
        raise ValueError(f"{descriptor['skill_id']} {locale} has no runtime_source")
    runtime = ROOT / runtime_value

    target = output_root / locale / descriptor["installable_name"]
    references = target / "references"
    references.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(runtime, target / "SKILL.md")

    for relative in descriptor.get("package_reference_sources", []):
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copyfile(source, references / source.name)

    write_origin(target, manifest, descriptor, "direct-skill-research-preview")
    return target


def build_preview(output_root: Path) -> list[Path]:
    manifest = load_manifest()
    descriptor_plan = plan_build_descriptors(manifest)
    built: list[Path] = []

    for locale, locale_plan in descriptor_plan["locales"].items():
        for descriptor in locale_plan["skills"]:
            if descriptor["state"] != "buildable-input":
                raise ValueError(
                    f"cannot preview blocked descriptor: {descriptor['skill_id']} {locale}"
                )

            mode = descriptor.get("assembly_mode")
            if mode == "router_modules":
                target = build_router_modules_preview(output_root, manifest, descriptor)
            elif mode == "direct_skill":
                target = build_direct_skill_preview(output_root, manifest, descriptor)
            else:
                raise ValueError(
                    f"unsupported preview assembly mode {mode!r} for "
                    f"{descriptor['skill_id']} {locale}"
                )
            built.append(target)

    return built


def validate_local_links(output_root: Path, target: Path) -> list[str]:
    errors: list[str] = []
    for path in [target / "SKILL.md", *sorted((target / "references").glob("*.md"))]:
        if not path.is_file():
            continue
        for link in LOCAL_LINK.findall(path.read_text(encoding="utf-8")):
            raw = link.strip()
            if not raw or raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = raw.split("#", 1)[0].strip()
            if not relative:
                continue
            if not (path.parent / relative).exists():
                errors.append(
                    f"{path.relative_to(output_root)}: unresolved local link -> {raw}"
                )
    return errors


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

        if name is None:
            errors.append(f"{target.relative_to(output_root)}: packaged SKILL.md has no name frontmatter")
        elif name != expected_name:
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

        for source in origin.get("package_reference_sources", []):
            expected = target / "references" / Path(str(source)).name
            if not expected.is_file():
                errors.append(
                    f"{target.relative_to(output_root)}: declared package reference missing: {source}"
                )

        errors.extend(validate_local_links(output_root, target))

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a research-only bilingual three-Skill preview."
    )
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
