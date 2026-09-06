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

from plan_suite_layout import plan_suite  # noqa: E402

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
    skill: dict[str, Any],
    locale: str,
    package_source: dict[str, Any],
    packaging_mode: str,
) -> None:
    realization = skill["locale_realizations"][locale]
    origin = {
        "suite": manifest["suite_id"],
        "skill_id": skill["id"],
        "installable_name": skill["installable_name"],
        "locale": locale,
        "realization_status": realization.get("status"),
        "runtime_source": realization.get("runtime_entry"),
        "method_source": realization.get("method_definition"),
        "package_source": package_source,
        "packaging_mode": packaging_mode,
        "research_only": True,
    }
    (target / "ORIGIN.json").write_text(
        json.dumps(origin, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_explicit_files_preview(
    output_root: Path,
    manifest: dict[str, Any],
    skill: dict[str, Any],
    locale: str,
    package_source: dict[str, Any],
) -> Path:
    package_root = ROOT / str(package_source["root"])
    runtime = (ROOT / skill["locale_realizations"][locale]["runtime_entry"]).resolve()
    target = output_root / locale / skill["installable_name"]
    target.mkdir(parents=True, exist_ok=True)

    for relative in package_source["files"]:
        source = package_root / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        destination_relative = Path("SKILL.md") if source.resolve() == runtime else Path(relative)
        destination = target / destination_relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    write_origin(
        target,
        manifest,
        skill,
        locale,
        package_source,
        "explicit-files-research-preview",
    )
    return target


def build_canonical_manifest_preview(
    output_root: Path,
    manifest: dict[str, Any],
    skill: dict[str, Any],
    locale: str,
    package_source: dict[str, Any],
) -> Path:
    source_manifest = load_json(ROOT / str(package_source["manifest"]))
    locale_root = ROOT / str(package_source["locale_root"])
    runtime = ROOT / skill["locale_realizations"][locale]["runtime_entry"]
    target = output_root / locale / skill["installable_name"]
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
        f"name: {skill['installable_name']}\n"
        f"description: {description}\n"
        "---\n\n"
        + router
    )
    (target / "SKILL.md").write_text(skill_text, encoding="utf-8")

    for module in source_manifest["modules"]:
        source = locale_root / module["source"]
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copyfile(source, references / module["skill_reference"])

    write_origin(
        target,
        manifest,
        skill,
        locale,
        package_source,
        "canonical-manifest-research-preview",
    )
    return target


def build_preview(output_root: Path) -> list[Path]:
    manifest = load_manifest()
    plan = plan_suite(manifest)
    skills_by_id = {
        skill["id"]: skill for skill in manifest["skills"] if isinstance(skill, dict)
    }
    built: list[Path] = []

    for locale, locale_plan in plan["locales"].items():
        for skill_id, realization_plan in locale_plan["skill_realizations"].items():
            if not realization_plan["realized"]:
                raise ValueError(f"cannot preview blocked realization: {skill_id} {locale}")
            package_source = realization_plan.get("package_source")
            if not isinstance(package_source, dict):
                raise ValueError(f"missing package_source: {skill_id} {locale}")
            skill = skills_by_id[skill_id]
            mode = package_source.get("mode")
            if mode == "explicit_files":
                target = build_explicit_files_preview(
                    output_root, manifest, skill, locale, package_source
                )
            elif mode == "canonical_manifest":
                target = build_canonical_manifest_preview(
                    output_root, manifest, skill, locale, package_source
                )
            else:
                raise ValueError(
                    f"unsupported package_source mode {mode!r}: {skill_id} {locale}"
                )
            built.append(target)

    return built


def validate_local_links(output_root: Path, target: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(target.rglob("*.md")):
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


def expected_explicit_destination(
    origin: dict[str, Any],
    source_relative: str,
) -> Path:
    package_source = origin["package_source"]
    package_root = ROOT / str(package_source["root"])
    source = (package_root / source_relative).resolve()
    runtime = (ROOT / str(origin["runtime_source"])).resolve()
    return Path("SKILL.md") if source == runtime else Path(source_relative)


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

        package_source = origin.get("package_source", {})
        if package_source.get("mode") == "explicit_files":
            for source_relative in package_source.get("files", []):
                destination = target / expected_explicit_destination(origin, source_relative)
                if not destination.is_file():
                    errors.append(
                        f"{target.relative_to(output_root)}: declared package source missing: "
                        f"{source_relative}"
                    )

        method_source = origin.get("method_source")
        if method_source and package_source.get("mode") == "explicit_files":
            package_root = ROOT / str(package_source["root"])
            method_path = (ROOT / str(method_source)).resolve()
            method_relative = method_path.relative_to(package_root.resolve())
            if not (target / method_relative).is_file():
                errors.append(
                    f"{target.relative_to(output_root)}: selected locale Method Definition missing"
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
