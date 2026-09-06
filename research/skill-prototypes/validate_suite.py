from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUITE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = SUITE_ROOT / "suite-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def read_frontmatter_name(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "name":
            return value.strip().strip('"\'')
    return None


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_runtime_entry(
    sid: str,
    label: str,
    runtime_value: Any,
    installable: str,
    errors: list[str],
) -> None:
    if not isinstance(runtime_value, str) or not runtime_value:
        errors.append(f"{sid}: {label} runtime_entry missing")
        return

    runtime = ROOT / runtime_value
    if not runtime.is_file():
        errors.append(f"{sid}: {label} runtime_entry does not exist: {runtime_value}")
        return

    frontmatter_name = read_frontmatter_name(runtime)
    if frontmatter_name is not None and frontmatter_name != installable:
        errors.append(
            f"{sid}: {label} runtime frontmatter name {frontmatter_name!r} "
            f"!= installable_name {installable!r}"
        )


def validate_method_definition(
    sid: str,
    label: str,
    method_value: Any,
    errors: list[str],
) -> None:
    if method_value is None:
        return
    if not isinstance(method_value, str) or not method_value:
        errors.append(f"{sid}: {label} method_definition must be a path or null")
        return
    if not (ROOT / method_value).is_file():
        errors.append(f"{sid}: {label} method_definition missing: {method_value}")


def validate(manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if manifest.get("schema") != "csw.research-skill-suite/v1":
        errors.append("unexpected suite schema")
    if manifest.get("status") != "research-only":
        warnings.append("suite is no longer marked research-only")

    locale_config = manifest.get("locales")
    if not isinstance(locale_config, dict) or not locale_config:
        errors.append("suite locales are missing")
        expected_locales: set[str] = set()
    else:
        expected_locales = {str(locale) for locale in locale_config}

    canonical_locale = str(manifest.get("canonical_locale", ""))
    if not canonical_locale:
        errors.append("canonical_locale missing")
    elif expected_locales and canonical_locale not in expected_locales:
        errors.append(f"canonical_locale is not declared in locales: {canonical_locale}")

    skills = [item for item in as_list(manifest.get("skills")) if isinstance(item, dict)]
    if not skills:
        errors.append("manifest has no skills")
        return errors, warnings

    ids = [str(item.get("id", "")).strip() for item in skills]
    names = [str(item.get("installable_name", "")).strip() for item in skills]

    for value, label in ((ids, "skill id"), (names, "installable name")):
        empty = [index for index, item in enumerate(value) if not item]
        if empty:
            errors.append(f"empty {label} at indexes: {empty}")
        duplicates = sorted({item for item in value if item and value.count(item) > 1})
        if duplicates:
            errors.append(f"duplicate {label}(s): {', '.join(duplicates)}")

    known_ids = {item for item in ids if item}

    for skill in skills:
        sid = str(skill.get("id", "<missing>"))
        installable = str(skill.get("installable_name", ""))

        source_root_value = skill.get("source_root")
        if not isinstance(source_root_value, str) or not source_root_value:
            errors.append(f"{sid}: source_root missing")
        else:
            source_root = ROOT / source_root_value
            if not source_root.is_dir():
                errors.append(f"{sid}: source_root does not exist: {source_root_value}")

        runtime_value = skill.get("runtime_entry")
        validate_runtime_entry(sid, "canonical", runtime_value, installable, errors)

        method_value = skill.get("method_definition")
        validate_method_definition(sid, "canonical", method_value, errors)

        realizations = skill.get("locale_realizations")
        if not isinstance(realizations, dict) or not realizations:
            errors.append(f"{sid}: locale_realizations missing")
        else:
            actual_locales = {str(locale) for locale in realizations}
            missing_locales = sorted(expected_locales - actual_locales)
            extra_locales = sorted(actual_locales - expected_locales)
            if missing_locales:
                errors.append(
                    f"{sid}: locale_realizations missing locale(s): {', '.join(missing_locales)}"
                )
            if extra_locales:
                errors.append(
                    f"{sid}: locale_realizations contain undeclared locale(s): {', '.join(extra_locales)}"
                )

            for locale, realization in realizations.items():
                label = f"locale {locale}"
                if not isinstance(realization, dict):
                    errors.append(f"{sid}: {label} realization must be an object")
                    continue
                if not str(realization.get("status", "")).strip():
                    errors.append(f"{sid}: {label} realization status missing")
                validate_runtime_entry(
                    sid,
                    label,
                    realization.get("runtime_entry"),
                    installable,
                    errors,
                )
                validate_method_definition(
                    sid,
                    label,
                    realization.get("method_definition"),
                    errors,
                )

            canonical_realization = realizations.get(canonical_locale)
            if isinstance(canonical_realization, dict):
                if canonical_realization.get("runtime_entry") != runtime_value:
                    errors.append(
                        f"{sid}: top-level runtime_entry must match canonical locale realization"
                    )
                if canonical_realization.get("method_definition") != method_value:
                    errors.append(
                        f"{sid}: top-level method_definition must match canonical locale realization"
                    )

        for section in ("references", "evidence", "evals", "checks"):
            declared = skill.get(section, [])
            if not isinstance(declared, list):
                errors.append(f"{sid}: {section} must be an array")
                continue
            for relative in declared:
                if not isinstance(relative, str) or not relative:
                    errors.append(f"{sid}: invalid {section} entry: {relative!r}")
                    continue
                if not (ROOT / relative).is_file():
                    errors.append(f"{sid}: declared {section} file missing: {relative}")

        delegation = skill.get("delegation", {})
        if isinstance(delegation, dict) and delegation.get("hard_dependency") is True:
            errors.append(f"{sid}: public research contract must not assume hard dependency")

    distributions = manifest.get("distribution_prototypes", {})
    if not isinstance(distributions, dict):
        errors.append("distribution_prototypes must be an object")
    else:
        for surface, config in distributions.items():
            if not isinstance(config, dict):
                errors.append(f"distribution {surface} must be an object")
                continue
            for field in ("contains",):
                if field in config:
                    refs = config[field]
                    if not isinstance(refs, list):
                        errors.append(f"distribution {surface}.{field} must be an array")
                        continue
                    unknown = sorted(str(ref) for ref in refs if str(ref) not in known_ids)
                    if unknown:
                        errors.append(
                            f"distribution {surface}.{field} references unknown skills: "
                            + ", ".join(unknown)
                        )
            primary = config.get("primary")
            if primary is not None and str(primary) not in known_ids:
                errors.append(
                    f"distribution {surface}.primary references unknown skill: {primary}"
                )

    gates = manifest.get("promotion_gates")
    if not isinstance(gates, list) or not gates:
        warnings.append("promotion_gates are missing or empty")

    return errors, warnings


def main() -> None:
    try:
        manifest = load_json(MANIFEST_PATH)
        errors, warnings = validate(manifest)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        raise SystemExit(1)

    print(f"Research skill suite validation passed ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
