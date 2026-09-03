from __future__ import annotations

import json
import re
from pathlib import Path

from common import ADAPTERS, DIST, ROOT, locales, manifest

LOCAL_METHOD_REFERENCE = re.compile(r"(?:^|[\s(])(?:core|methods|governance|domains)/")
LOCAL_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)[^)]+\)")

REQUIRED_INSTRUCTION_MARKERS = {
    "ja-JP": (
        "Microsoft 365限定プロファイル",
        "意味の一体性を守る必要があるときは結合",
        "委ねられた範囲を、勝手に広げず",
        "target_supported",
        "観測、測定、利用者判断、AI解釈を混ぜない",
    ),
    "en-US": (
        "Microsoft 365 limited profile",
        "Join material when semantic unity must be preserved",
        "Do not expand the scope entrusted by the user",
        "target_supported",
        "Separate observation, measurement, user judgment, and AI interpretation",
    ),
}

README_MARKERS = {
    "ja-JP": (
        "instructions.txt",
        "method-reference/",
        "Knowledge",
        "続きを実行させるためのファイルではありません",
    ),
    "en-US": (
        "instructions.txt",
        "method-reference/",
        "Knowledge",
        "Do not upload these files",
    ),
}


def validate_m365_profile(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    config = manifest() if root == ROOT else json.loads((root / "src/manifest.json").read_text(encoding="utf-8"))
    expected_reference_files = set(config["knowledge_groups"])

    for locale in locales() if root == ROOT else config["locales"]:
        adapter_root = root / "adapters" / "microsoft-copilot" / locale
        generated_root = root / "dist" / locale / "microsoft-copilot"
        source_path = adapter_root / "instructions.md"
        old_prefix = adapter_root / "instructions-prefix.md"
        package_readme_source = adapter_root / "package-readme.txt"

        if old_prefix.exists():
            errors.append(f"{locale}: obsolete Microsoft instructions-prefix.md still exists")

        if not source_path.is_file():
            errors.append(f"{locale}: Microsoft self-contained instructions.md is missing")
            continue

        instructions = source_path.read_text(encoding="utf-8").rstrip()
        if len(instructions) > 8000:
            errors.append(
                f"{locale}: Microsoft self-contained instructions exceed 8000 characters: {len(instructions)}"
            )

        if LOCAL_METHOD_REFERENCE.search(instructions):
            errors.append(f"{locale}: Microsoft instructions contain a local method-module path")
        if LOCAL_MARKDOWN_LINK.search(instructions):
            errors.append(f"{locale}: Microsoft instructions contain a local Markdown dependency")

        for marker in REQUIRED_INSTRUCTION_MARKERS[locale]:
            if marker not in instructions:
                errors.append(f"{locale}: Microsoft instructions missing required marker: {marker}")

        if not package_readme_source.is_file():
            errors.append(f"{locale}: Microsoft package-readme.txt is missing")
        else:
            readme_source = package_readme_source.read_text(encoding="utf-8")
            for marker in README_MARKERS[locale]:
                if marker not in readme_source:
                    errors.append(f"{locale}: Microsoft package README missing marker: {marker}")

        agent_path = generated_root / "agent-project" / "appPackage" / "declarativeAgent.json"
        instructions_path = generated_root / "instructions.txt"
        generated_readme = generated_root / "README.txt"
        method_reference = generated_root / "method-reference"
        old_knowledge = generated_root / "knowledge"

        if not agent_path.is_file():
            errors.append(f"{locale}: generated Microsoft declarativeAgent.json is missing")
        else:
            agent = json.loads(agent_path.read_text(encoding="utf-8"))
            if agent.get("instructions") != instructions:
                errors.append(f"{locale}: generated Microsoft instructions differ from adapter source")

        if not instructions_path.is_file():
            errors.append(f"{locale}: generated Microsoft instructions.txt is missing")
        elif instructions_path.read_text(encoding="utf-8") != instructions + "\n":
            errors.append(f"{locale}: generated Microsoft instructions.txt differs from adapter source")

        if old_knowledge.exists():
            errors.append(f"{locale}: generated Microsoft package still exposes method modules as knowledge/")

        if not method_reference.is_dir():
            errors.append(f"{locale}: generated Microsoft method-reference/ is missing")
        else:
            actual_reference_files = {
                path.name for path in method_reference.glob("*.md") if path.is_file()
            }
            if actual_reference_files != expected_reference_files:
                errors.append(
                    f"{locale}: Microsoft method-reference set mismatch: "
                    f"expected={sorted(expected_reference_files)}, actual={sorted(actual_reference_files)}"
                )

        if not generated_readme.is_file():
            errors.append(f"{locale}: generated Microsoft README.txt is missing")
        elif package_readme_source.is_file() and generated_readme.read_bytes() != package_readme_source.read_bytes():
            errors.append(f"{locale}: generated Microsoft README.txt differs from adapter source")

    return errors


def main() -> None:
    errors = validate_m365_profile()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Microsoft 365 limited-profile validation passed")


if __name__ == "__main__":
    main()
