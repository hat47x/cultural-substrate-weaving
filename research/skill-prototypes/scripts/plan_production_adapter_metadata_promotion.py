#!/usr/bin/env python3
"""Plan research adapter metadata promotion into future production sources.

Read-only research planner. It does not write production adapter metadata.
OpenAI sibling metadata is copied to the descriptor-declared production path
without content rewriting; locale-bundle prototypes contribute reviewed wording
only while the existing production locale/plugin identity remains authoritative.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "skill-prototypes"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402
from validate_research_production_suite_descriptor import (  # noqa: E402
    validate_production_suite_descriptor,
)

PLAN_SCHEMA = "csw.production-adapter-metadata-promotion-plan/v1"
ADAPTER_PLAN_SCHEMA = "csw.research-adapter-metadata-plan/v1"
CANONICAL_SUITE_MANIFEST = "research/skill-prototypes/suite-manifest.json"
BUNDLE_PROMOTION_STATE = "planned-locale-catalog-wording-update"
RESEARCH_BUNDLE_ROOT = PurePosixPath("research/skill-prototypes/adapters/claude-codex")
PRODUCTION_ADAPTER_ROOT = PurePosixPath("adapters")
PRODUCTION_BUNDLE_CATALOG = PurePosixPath("adapters/claude-code/locales.json")


def _safe_repo_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def _path_under(value: str, root: PurePosixPath) -> bool:
    if not _safe_repo_path(value):
        return False
    path = PurePosixPath(value)
    return path.parts[: len(root.parts)] == root.parts


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _assert_public_identity_safe(
    text: str,
    *,
    research_id: str,
    production_name: str,
    label: str,
) -> None:
    """Reject host-visible text that would expose a renamed research identity."""

    if research_id == production_name:
        return
    if research_id in text:
        raise ValueError(
            f"{label} retains renamed research identity {research_id!r}; "
            f"public promotion target is {production_name!r}"
        )


def _bundle_drop_fields(prototype: dict) -> list[str]:
    """Return prototype-only fields that must not enter the host locale catalog."""

    host_visible_or_preserved = {"plugin_name", "display", "description"}
    return [field for field in prototype if field not in host_visible_or_preserved]


def _descriptor_by_id(descriptor: dict) -> dict[str, dict]:
    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        return {}
    return {
        item["research_id"]: item
        for item in skills
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }


def _openai_profile_names(adapter_plan: dict) -> tuple[str, ...]:
    profiles = adapter_plan["distributions"]["openai_skill"]["profiles"]
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError("OpenAI adapter metadata plan must declare profiles")
    return tuple(profiles)


def _bundle_distribution_names(adapter_plan: dict) -> tuple[str, ...]:
    names = tuple(
        name
        for name, config in adapter_plan.get("distributions", {}).items()
        if isinstance(config, dict) and config.get("scope") == "locale_bundle"
    )
    if not names:
        raise ValueError("adapter metadata plan must declare at least one locale_bundle distribution")
    return names


def _assert_adapter_plan_distribution_modes(adapter_plan: dict) -> None:
    if adapter_plan.get("schema") != ADAPTER_PLAN_SCHEMA:
        raise ValueError(
            f"adapter metadata plan schema must remain {ADAPTER_PLAN_SCHEMA}"
        )
    if adapter_plan.get("suite_manifest") != CANONICAL_SUITE_MANIFEST:
        raise ValueError(
            "adapter metadata suite_manifest must remain canonical: "
            f"{adapter_plan.get('suite_manifest')!r} != {CANONICAL_SUITE_MANIFEST!r}"
        )

    distributions = adapter_plan.get("distributions")
    if not isinstance(distributions, dict):
        raise ValueError("adapter metadata plan must declare distributions")

    openai = distributions.get("openai_skill")
    if not isinstance(openai, dict) or openai.get("scope") != "per_skill_per_profile":
        raise ValueError(
            "OpenAI adapter metadata scope must remain per_skill_per_profile"
        )

    bundle_names = set(_bundle_distribution_names(adapter_plan))
    required_bundle_names = {"claude_plugin", "codex_plugin"}
    missing = sorted(required_bundle_names - bundle_names)
    if missing:
        raise ValueError(
            "adapter metadata plan is missing required locale_bundle distributions: "
            f"{missing}"
        )
    for name in bundle_names:
        config = distributions.get(name)
        if not isinstance(config, dict) or config.get("source_mode") != "locale_catalog":
            raise ValueError(
                f"locale_bundle distribution {name} must use source_mode=locale_catalog"
            )


def _bundle_catalog_source(adapter_plan: dict) -> str:
    distributions = adapter_plan["distributions"]
    names = _bundle_distribution_names(adapter_plan)
    sources = {
        distributions[name].get("source")
        for name in names
        if isinstance(distributions.get(name), dict)
    }
    if len(sources) != 1:
        raise ValueError(f"locale_bundle distributions must share one production catalog: {sources!r}")
    source = next(iter(sources))
    if not isinstance(source, str) or not _safe_repo_path(source):
        raise ValueError(f"locale_bundle production catalog path is invalid: {source!r}")
    if not _path_under(source, PRODUCTION_ADAPTER_ROOT):
        raise ValueError(
            "locale_bundle production catalog is outside production adapter source class: "
            f"{source!r}"
        )
    if source != PRODUCTION_BUNDLE_CATALOG.as_posix():
        raise ValueError(
            "locale_bundle production catalog must remain canonical: "
            f"{source!r} != {PRODUCTION_BUNDLE_CATALOG.as_posix()!r}"
        )
    return source


def _assert_locale_catalog_snapshot(
    root: Path,
    source: str,
    locale_catalog: dict,
) -> None:
    if not isinstance(locale_catalog, dict):
        raise ValueError("production locale catalog must be an object")
    try:
        canonical = json.loads((root / source).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(
            f"production locale catalog could not be read from {source!r}: {exc}"
        ) from exc
    if locale_catalog != canonical:
        raise ValueError(
            "locale catalog snapshot must match canonical production catalog source"
        )


def _assert_descriptor_adapter_metadata_authority(
    descriptor_by_id: dict[str, dict],
    *,
    bundle_catalog_source: str,
) -> None:
    """Keep planner inputs bound to descriptor-owned production metadata topology."""

    for research_id, descriptor_skill in descriptor_by_id.items():
        production_name = descriptor_skill.get("proposed_installable_name")
        adapter_metadata = descriptor_skill.get("adapter_metadata")
        if not isinstance(adapter_metadata, dict):
            raise ValueError(
                f"production descriptor adapter_metadata missing for {research_id}"
            )

        openai_meta = adapter_metadata.get("openai_skill")
        if not isinstance(openai_meta, dict):
            raise ValueError(
                f"production descriptor OpenAI adapter metadata missing for {research_id}"
            )
        if research_id == "cultural-substrate-weaving":
            expected_openai_mode = "existing-per-locale-profile"
            expected_openai_pattern = (
                "adapters/openai-skill/{locale}/openai.{profile}.yaml"
            )
            expected_bundle_mode = "existing-locale-catalog-to-update"
        else:
            expected_openai_mode = "planned-promotion-from-research-prototype"
            expected_openai_pattern = (
                f"adapters/openai-skill/{{locale}}/{production_name}/"
                "openai.{profile}.yaml"
            )
            expected_bundle_mode = "bundle-via-locale-catalog"

        if openai_meta.get("mode") != expected_openai_mode:
            raise ValueError(
                "production descriptor OpenAI adapter metadata mode mismatch: "
                f"{research_id}: {openai_meta.get('mode')!r} != "
                f"{expected_openai_mode!r}"
            )
        if openai_meta.get("source_pattern") != expected_openai_pattern:
            raise ValueError(
                "production descriptor OpenAI adapter metadata path mismatch: "
                f"{research_id}: {openai_meta.get('source_pattern')!r} != "
                f"{expected_openai_pattern!r}"
            )

        for distribution in ("claude_plugin", "codex_plugin"):
            bundle_meta = adapter_metadata.get(distribution)
            if not isinstance(bundle_meta, dict):
                raise ValueError(
                    "production descriptor locale-bundle adapter metadata missing: "
                    f"{research_id}/{distribution}"
                )
            if bundle_meta.get("mode") != expected_bundle_mode:
                raise ValueError(
                    "production descriptor locale-bundle adapter metadata mode mismatch: "
                    f"{research_id}/{distribution}: {bundle_meta.get('mode')!r} != "
                    f"{expected_bundle_mode!r}"
                )
            if bundle_meta.get("source") != bundle_catalog_source:
                raise ValueError(
                    "production descriptor locale-bundle adapter metadata source mismatch: "
                    f"{research_id}/{distribution}: {bundle_meta.get('source')!r} != "
                    f"{bundle_catalog_source!r}"
                )


def _bundle_prototype_sources(adapter_plan: dict) -> dict[str, str]:
    """Return the one shared prototype wording source per locale."""

    distributions = adapter_plan["distributions"]
    names = _bundle_distribution_names(adapter_plan)

    for name in names:
        config = distributions[name]
        if config.get("review_required_for_multi_skill") is not True:
            raise ValueError(
                f"locale_bundle distribution {name} must require review for multi-Skill promotion"
            )

    first_name = names[0]
    first_locales = distributions[first_name].get("locales")
    if not isinstance(first_locales, dict) or not first_locales:
        raise ValueError(f"locale_bundle distribution {first_name} must declare locales")

    sources: dict[str, str] = {}
    for locale, entry in first_locales.items():
        if not isinstance(entry, dict):
            raise ValueError(f"locale_bundle metadata entry must be an object: {first_name}/{locale}")
        if entry.get("status") != "prototype":
            raise ValueError(
                f"locale_bundle metadata {first_name}/{locale} must remain prototype "
                "while promotion uses prototype wording source"
            )
        source = entry.get("prototype_source")
        if not isinstance(source, str) or not _safe_repo_path(source):
            raise ValueError(
                f"locale_bundle prototype source is invalid: {first_name}/{locale}: {source!r}"
            )
        expected_source_root = RESEARCH_BUNDLE_ROOT / locale
        if not _path_under(source, expected_source_root):
            raise ValueError(
                "locale_bundle prototype source is outside research bundle source class: "
                f"{first_name}/{locale}: {source!r}; "
                f"expected under {expected_source_root.as_posix()!r}"
            )
        sources[locale] = source

    expected_locales = set(sources)
    for name in names[1:]:
        locale_map = distributions[name].get("locales")
        if not isinstance(locale_map, dict) or set(locale_map) != expected_locales:
            actual = set(locale_map) if isinstance(locale_map, dict) else set()
            raise ValueError(
                "locale_bundle distributions must share one locale set: "
                f"{name}: missing={sorted(expected_locales - actual)}, "
                f"extra={sorted(actual - expected_locales)}"
            )
        for locale, expected_source in sources.items():
            entry = locale_map.get(locale)
            if not isinstance(entry, dict):
                raise ValueError(f"locale_bundle metadata entry must be an object: {name}/{locale}")
            if entry.get("status") != "prototype":
                raise ValueError(
                    f"locale_bundle metadata {name}/{locale} must remain prototype "
                    "while promotion uses prototype wording source"
                )
            actual_source = entry.get("prototype_source")
            if actual_source != expected_source:
                raise ValueError(
                    "locale_bundle distributions must share prototype source per locale: "
                    f"{name}/{locale}: {actual_source!r} != {expected_source!r}"
                )

    return sources


def validate_adapter_promotion_authorities(
    root: Path,
    adapter_plan: dict,
    descriptor: dict,
) -> list[str]:
    """Validate top-level authorities used by the adapter-promotion CLI."""

    errors: list[str] = []
    if not isinstance(adapter_plan, dict):
        errors.append("adapter metadata plan authority must be an object")
    else:
        errors.extend(validate_adapter_metadata(root, adapter_plan))
    if not isinstance(descriptor, dict):
        errors.append("production promotion descriptor authority must be an object")
    else:
        errors.extend(validate_production_suite_descriptor(descriptor))
    return errors


def plan_production_adapter_metadata_promotion(
    adapter_plan: dict,
    descriptor: dict,
    locale_catalog: dict,
    root: Path = ROOT,
) -> dict:
    if not isinstance(adapter_plan, dict):
        raise ValueError("adapter metadata plan authority must be an object")
    if not isinstance(descriptor, dict):
        raise ValueError("production promotion descriptor authority must be an object")
    if not isinstance(locale_catalog, dict):
        raise ValueError("production locale catalog must be an object")

    _assert_adapter_plan_distribution_modes(adapter_plan)

    descriptor_research_ids = [
        item.get("research_id")
        for item in descriptor.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    ]
    if len(descriptor_research_ids) != len(set(descriptor_research_ids)):
        raise ValueError("production descriptor contains duplicate research Skills")

    declared_locales = descriptor.get("locales")
    if (
        not isinstance(declared_locales, list)
        or not declared_locales
        or not all(isinstance(locale, str) and locale for locale in declared_locales)
        or len(declared_locales) != len(set(declared_locales))
    ):
        raise ValueError(
            "production descriptor locales must be a non-empty unique string list"
        )

    descriptor_by_id = _descriptor_by_id(descriptor)
    descriptor_skill_ids = set(descriptor_by_id)
    descriptor_locales = set(declared_locales)
    if not descriptor_skill_ids:
        raise ValueError("production descriptor must declare Skills")

    openai_distribution = adapter_plan["distributions"]["openai_skill"]
    openai_research = openai_distribution["skills"]
    if not isinstance(openai_research, dict):
        raise ValueError("OpenAI adapter metadata plan must declare a skills object")
    openai_skill_ids = set(openai_research)
    if openai_skill_ids != descriptor_skill_ids:
        raise ValueError(
            "OpenAI adapter metadata skill set must match production descriptor: "
            f"missing={sorted(descriptor_skill_ids - openai_skill_ids)}, "
            f"extra={sorted(openai_skill_ids - descriptor_skill_ids)}"
        )

    profiles = _openai_profile_names(adapter_plan)
    expected_profiles = set(profiles)

    openai: list[dict] = []
    for research_id, skill_metadata in openai_research.items():
        if not isinstance(skill_metadata, dict):
            raise ValueError(f"OpenAI adapter metadata Skill entry must be an object: {research_id}")
        locale_names = set(skill_metadata)
        if locale_names != descriptor_locales:
            raise ValueError(
                "OpenAI adapter metadata locales must match production descriptor: "
                f"{research_id}: missing={sorted(descriptor_locales - locale_names)}, "
                f"extra={sorted(locale_names - descriptor_locales)}"
            )
        descriptor_skill = descriptor_by_id[research_id]
        production_name = descriptor_skill["proposed_installable_name"]
        production_meta = descriptor_skill["adapter_metadata"]["openai_skill"]
        metadata_mode = production_meta.get("mode")
        source_pattern = production_meta.get("source_pattern")
        if metadata_mode not in {
            "existing-per-locale-profile",
            "planned-promotion-from-research-prototype",
        }:
            raise ValueError(
                f"unsupported OpenAI production metadata mode for {research_id}: {metadata_mode!r}"
            )
        if not isinstance(source_pattern, str):
            raise ValueError(f"OpenAI production metadata source pattern missing for {research_id}")

        expected_research_status = (
            "existing"
            if metadata_mode == "existing-per-locale-profile"
            else "prototype"
        )

        for locale, locale_profiles in skill_metadata.items():
            if not isinstance(locale_profiles, dict):
                raise ValueError(
                    f"OpenAI adapter metadata locale entry must be an object: {research_id}/{locale}"
                )
            profile_names = set(locale_profiles)
            if profile_names != expected_profiles:
                raise ValueError(
                    "OpenAI adapter metadata profiles must match declared profiles: "
                    f"{research_id}/{locale}: missing={sorted(expected_profiles - profile_names)}, "
                    f"extra={sorted(profile_names - expected_profiles)}"
                )
            for profile in profiles:
                research_item = locale_profiles[profile]
                research_status = research_item.get("status")
                if research_status != expected_research_status:
                    raise ValueError(
                        "OpenAI adapter metadata status does not match production metadata mode: "
                        f"{research_id}/{locale}/{profile}: "
                        f"{research_status!r} != {expected_research_status!r}"
                    )
                source = research_item.get("source")
                if not isinstance(source, str) or not _safe_repo_path(source):
                    raise ValueError(
                        "OpenAI adapter metadata source is invalid: "
                        f"{research_id}/{locale}/{profile}: {source!r}"
                    )
                expected_source_root = (
                    PurePosixPath("adapters/openai-skill") / locale
                    if expected_research_status == "existing"
                    else PurePosixPath(
                        "research/skill-prototypes/adapters/openai-skill"
                    )
                    / locale
                    / research_id
                )
                if not _path_under(source, expected_source_root):
                    raise ValueError(
                        "OpenAI adapter metadata source is outside declared source class: "
                        f"{research_id}/{locale}/{profile}: {source!r}; "
                        f"expected under {expected_source_root.as_posix()!r}"
                    )
                target = source_pattern.format(locale=locale, profile=profile)
                if (
                    not _safe_repo_path(target)
                    or not target.startswith("adapters/openai-skill/")
                ):
                    raise ValueError(
                        "OpenAI production metadata target is invalid: "
                        f"{research_id}/{locale}/{profile}: {target!r}"
                    )

                if metadata_mode == "existing-per-locale-profile":
                    openai.append(
                        {
                            "research_id": research_id,
                            "production_name": production_name,
                            "locale": locale,
                            "profile": profile,
                            "state": "existing-production-source",
                            "source": source,
                            "target": target,
                            "content_operation": "keep-existing-production-metadata",
                        }
                    )
                    continue

                text = (root / source).read_text(encoding="utf-8")
                _assert_public_identity_safe(
                    text,
                    research_id=research_id,
                    production_name=production_name,
                    label=f"OpenAI metadata source {source}",
                )
                openai.append(
                    {
                        "research_id": research_id,
                        "production_name": production_name,
                        "locale": locale,
                        "profile": profile,
                        "state": "planned-prototype-promotion",
                        "source": source,
                        "target": target,
                        "content_operation": "copy-byte-identical",
                        "sha256": _sha256_text(text),
                    }
                )

    bundle_distribution_names = _bundle_distribution_names(adapter_plan)
    bundle_catalog_source = _bundle_catalog_source(adapter_plan)
    _assert_locale_catalog_snapshot(root, bundle_catalog_source, locale_catalog)
    _assert_descriptor_adapter_metadata_authority(
        descriptor_by_id,
        bundle_catalog_source=bundle_catalog_source,
    )
    bundle_prototype_sources = _bundle_prototype_sources(adapter_plan)
    bundle_locales = set(bundle_prototype_sources)
    if bundle_locales != descriptor_locales:
        raise ValueError(
            "locale_bundle metadata locales must match production descriptor: "
            f"missing={sorted(descriptor_locales - bundle_locales)}, "
            f"extra={sorted(bundle_locales - descriptor_locales)}"
        )
    bundle_promotions: list[dict] = []
    public_skill_set = [item["proposed_installable_name"] for item in descriptor["skills"]]
    for locale, prototype_source in bundle_prototype_sources.items():
        prototype = json.loads((root / prototype_source).read_text(encoding="utf-8"))
        description = prototype["description"]
        for research_id, descriptor_skill in descriptor_by_id.items():
            _assert_public_identity_safe(
                description,
                research_id=research_id,
                production_name=descriptor_skill["proposed_installable_name"],
                label=f"locale-bundle description {prototype_source}",
            )
        current = locale_catalog[locale]
        bundle_promotions.append(
            {
                "locale": locale,
                "state": BUNDLE_PROMOTION_STATE,
                "prototype_source": prototype_source,
                "production_catalog": bundle_catalog_source,
                "preserve": {
                    "plugin_name": current["plugin_name"],
                    "skill_name": current["skill_name"],
                    "display": current["display"],
                },
                "update": {"description": description},
                "prototype_research_contains": prototype["contains"],
                "production_suite_contains": public_skill_set,
                "drop_prototype_fields_from_host_catalog": _bundle_drop_fields(prototype),
                "shared_by": list(bundle_distribution_names),
            }
        )

    return {
        "schema": PLAN_SCHEMA,
        "status": "design-only",
        "writes_production_metadata": False,
        "openai_profile_promotions": openai,
        "locale_bundle_promotions": bundle_promotions,
        "note": (
            "Research-only adapter metadata promotion plan. OpenAI sibling YAML content is "
            "promoted unchanged to descriptor-declared production paths. Locale-bundle "
            "distributions share the existing production catalog identity and promote only "
            "split-aware description wording; suite composition remains owned by the production "
            "suite descriptor."
        ),
    }


def _expected_openai_sources(
    adapter_plan: dict,
) -> dict[tuple[str, str, str], str]:
    profiles = _openai_profile_names(adapter_plan)
    skills = adapter_plan["distributions"]["openai_skill"]["skills"]
    sources: dict[tuple[str, str, str], str] = {}
    for research_id, skill_metadata in skills.items():
        for locale, locale_profiles in skill_metadata.items():
            for profile in profiles:
                entry = locale_profiles.get(profile)
                if not isinstance(entry, dict):
                    raise ValueError(
                        "OpenAI adapter metadata entry must be an object: "
                        f"{research_id}/{locale}/{profile}"
                    )
                source = entry.get("source")
                if not isinstance(source, str) or not _safe_repo_path(source):
                    raise ValueError(
                        "OpenAI adapter metadata source is invalid: "
                        f"{research_id}/{locale}/{profile}: {source!r}"
                    )
                sources[(research_id, locale, profile)] = source
    return sources


def _expected_openai_keys(adapter_plan: dict) -> set[tuple[str, str, str]]:
    return set(_expected_openai_sources(adapter_plan))


def _expected_openai_statuses(
    adapter_plan: dict,
) -> dict[tuple[str, str, str], str]:
    profiles = _openai_profile_names(adapter_plan)
    skills = adapter_plan["distributions"]["openai_skill"]["skills"]
    statuses: dict[tuple[str, str, str], str] = {}
    for research_id, skill_metadata in skills.items():
        for locale, locale_profiles in skill_metadata.items():
            for profile in profiles:
                entry = locale_profiles.get(profile)
                if not isinstance(entry, dict):
                    raise ValueError(
                        "OpenAI adapter metadata entry must be an object: "
                        f"{research_id}/{locale}/{profile}"
                    )
                status = entry.get("status")
                if not isinstance(status, str):
                    raise ValueError(
                        "OpenAI adapter metadata status is invalid: "
                        f"{research_id}/{locale}/{profile}: {status!r}"
                    )
                statuses[(research_id, locale, profile)] = status
    return statuses


def validate_production_adapter_metadata_promotion_plan(
    plan: dict,
    descriptor: dict,
    locale_catalog: dict,
    *,
    adapter_plan: dict | None = None,
    root: Path = ROOT,
) -> list[str]:
    if not isinstance(plan, dict):
        return ["adapter metadata promotion plan must be an object"]

    errors: list[str] = []
    if not isinstance(descriptor, dict):
        errors.append("production promotion descriptor must be an object")
        descriptor = {}
    else:
        errors.extend(validate_production_suite_descriptor(descriptor))
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"adapter metadata promotion plan schema must be {PLAN_SCHEMA}")
    if plan.get("status") != "design-only":
        errors.append("adapter metadata promotion plan must remain design-only")
    if plan.get("writes_production_metadata") is not False:
        errors.append("adapter metadata promotion plan must not write production metadata")
    if adapter_plan is None:
        errors.append(
            "adapter metadata promotion validation requires adapter-plan authority"
        )
    elif not isinstance(adapter_plan, dict):
        errors.append("adapter metadata plan authority must be an object")
        adapter_plan = None
    else:
        errors.extend(validate_adapter_metadata(root, adapter_plan))

    if isinstance(locale_catalog, dict):
        validated_locale_catalog = locale_catalog
    else:
        errors.append("production locale catalog must be an object")
        validated_locale_catalog = {}

    descriptor_skills = descriptor.get("skills")
    if not isinstance(descriptor_skills, list):
        descriptor_skills = []
    descriptor_research_ids = [
        item.get("research_id")
        for item in descriptor_skills
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    ]
    if len(descriptor_research_ids) != len(set(descriptor_research_ids)):
        errors.append("production descriptor contains duplicate research Skills")

    declared_locales = descriptor.get("locales")
    if (
        not isinstance(declared_locales, list)
        or not declared_locales
        or not all(isinstance(locale, str) and locale for locale in declared_locales)
        or len(declared_locales) != len(set(declared_locales))
    ):
        errors.append(
            "production descriptor locales must be a non-empty unique string list"
        )

    descriptor_by_id = _descriptor_by_id(descriptor)
    openai = plan.get("openai_profile_promotions")
    if not isinstance(openai, list):
        errors.append("OpenAI adapter promotion plan must be a list")
        openai = []

    expected_openai_sources: dict[tuple[str, str, str], str] | None
    expected_openai_statuses: dict[tuple[str, str, str], str] | None
    if adapter_plan is not None:
        try:
            _assert_adapter_plan_distribution_modes(adapter_plan)
            expected_openai_sources = _expected_openai_sources(adapter_plan)
            expected_openai_statuses = _expected_openai_statuses(adapter_plan)
            expected_openai_keys = set(expected_openai_sources)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"OpenAI adapter promotion authority is invalid: {exc}")
            expected_openai_sources = None
            expected_openai_statuses = None
            expected_openai_keys = set()
    else:
        expected_openai_sources = None
        expected_openai_statuses = None
        observed_profiles = {
            item.get("profile")
            for item in openai
            if isinstance(item, dict) and isinstance(item.get("profile"), str)
        }
        expected_openai_keys = {
            (research_id, locale, profile)
            for research_id in descriptor_by_id
            for locale in descriptor.get("locales", [])
            for profile in observed_profiles
        }

    seen_openai: set[tuple[str, str, str]] = set()
    for item in openai:
        if not isinstance(item, dict):
            errors.append("OpenAI adapter promotion entries must be objects")
            continue
        research_id = item.get("research_id")
        locale = item.get("locale")
        profile = item.get("profile")
        if not all(
            isinstance(value, str) and value
            for value in (research_id, locale, profile)
        ):
            errors.append(
                "OpenAI adapter promotion identity fields must be non-empty strings"
            )
            continue
        key = (research_id, locale, profile)
        if key in seen_openai:
            errors.append(f"duplicate OpenAI adapter promotion entry: {key}")
        seen_openai.add(key)
        descriptor_skill = descriptor_by_id.get(research_id)
        if descriptor_skill is None:
            errors.append(f"unknown research Skill in OpenAI adapter promotion: {research_id}")
            continue

        production_name = descriptor_skill.get("proposed_installable_name")
        if item.get("production_name") != production_name:
            errors.append(f"OpenAI adapter promotion production name mismatch: {research_id}")

        expected_source = (
            expected_openai_sources.get(key)
            if expected_openai_sources is not None
            else None
        )
        if expected_source is not None and item.get("source") != expected_source:
            errors.append(
                "OpenAI adapter promotion source mismatch: "
                f"{key}: {item.get('source')!r} != {expected_source!r}"
            )

        adapter_metadata = descriptor_skill.get("adapter_metadata")
        production_meta = (
            adapter_metadata.get("openai_skill", {})
            if isinstance(adapter_metadata, dict)
            else {}
        )
        metadata_mode = production_meta.get("mode")
        source_pattern = production_meta.get("source_pattern")
        expected_research_status = (
            "existing"
            if metadata_mode == "existing-per-locale-profile"
            else "prototype"
            if metadata_mode == "planned-promotion-from-research-prototype"
            else None
        )
        if expected_openai_statuses is not None:
            declared_status = expected_openai_statuses.get(key)
            if (
                expected_research_status is not None
                and declared_status != expected_research_status
            ):
                errors.append(
                    "OpenAI adapter metadata status does not match production metadata mode: "
                    f"{key}: {declared_status!r} != {expected_research_status!r}"
                )
        target = item.get("target")
        if not isinstance(target, str) or not _safe_repo_path(target) or not target.startswith("adapters/openai-skill/"):
            errors.append(f"unsafe OpenAI production metadata target: {target!r}")
        if isinstance(target, str) and target.startswith("research/"):
            errors.append(f"OpenAI production metadata target must not point into research: {target}")
        if isinstance(source_pattern, str) and isinstance(locale, str) and isinstance(profile, str):
            expected_target = source_pattern.format(locale=locale, profile=profile)
            if target != expected_target:
                errors.append(
                    f"OpenAI production metadata target must use {production_name}: "
                    f"{research_id}/{locale}/{profile}"
                )

        if metadata_mode == "planned-promotion-from-research-prototype":
            if item.get("state") != "planned-prototype-promotion":
                errors.append(f"sibling OpenAI metadata must remain planned prototype promotion: {key}")
            if item.get("content_operation") != "copy-byte-identical":
                errors.append(f"sibling OpenAI metadata content must promote byte-identically: {key}")
            digest = item.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64:
                errors.append(f"sibling OpenAI metadata must retain source sha256: {key}")
            elif expected_source is not None:
                try:
                    expected_digest = _sha256_text(
                        (root / expected_source).read_text(encoding="utf-8")
                    )
                except (OSError, UnicodeError) as exc:
                    errors.append(
                        "OpenAI adapter promotion source could not be read: "
                        f"{key}: {exc}"
                    )
                else:
                    if digest != expected_digest:
                        errors.append(
                            f"OpenAI adapter promotion source sha256 mismatch: {key}"
                        )
        elif metadata_mode == "existing-per-locale-profile":
            if item.get("state") != "existing-production-source":
                errors.append(f"existing OpenAI metadata must remain existing production source: {key}")
            if item.get("content_operation") != "keep-existing-production-metadata":
                errors.append(f"existing OpenAI metadata must keep production content: {key}")
            if item.get("source") != target:
                errors.append(f"existing OpenAI metadata source/target must remain identical: {key}")
        else:
            errors.append(f"unsupported OpenAI production metadata mode for {research_id}: {metadata_mode!r}")

    missing_openai = sorted(expected_openai_keys - seen_openai)
    extra_openai = sorted(seen_openai - expected_openai_keys)
    if missing_openai:
        errors.append(f"OpenAI adapter promotion plan is missing declared surfaces: {missing_openai}")
    if extra_openai:
        errors.append(f"OpenAI adapter promotion plan has undeclared surfaces: {extra_openai}")

    bundle = plan.get("locale_bundle_promotions")
    expected_locale_count = len(declared_locales) if isinstance(declared_locales, list) else 0
    if not isinstance(bundle, list) or len(bundle) != expected_locale_count:
        errors.append("bundle metadata promotion plan must contain one entry per locale")
        bundle = []
    expected_public = [
        item.get("proposed_installable_name")
        for item in descriptor_skills
        if isinstance(item, dict) and isinstance(item.get("proposed_installable_name"), str)
    ]
    expected_research = set(descriptor_by_id)

    if adapter_plan is not None:
        try:
            expected_shared_by = list(_bundle_distribution_names(adapter_plan))
            expected_catalog = _bundle_catalog_source(adapter_plan)
            if isinstance(locale_catalog, dict):
                _assert_locale_catalog_snapshot(root, expected_catalog, locale_catalog)
            expected_prototype_sources = _bundle_prototype_sources(adapter_plan)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"bundle adapter promotion authority is invalid: {exc}")
            expected_shared_by = None
            expected_catalog = None
            expected_prototype_sources = None
    else:
        expected_shared_by = None
        expected_catalog = None
        expected_prototype_sources = None

    expected_bundle_locales = (
        set(expected_prototype_sources)
        if expected_prototype_sources is not None
        else {
            locale
            for locale in descriptor.get("locales", [])
            if isinstance(locale, str)
        }
    )
    seen_bundle_locales: set[str] = set()

    for item in bundle:
        if not isinstance(item, dict):
            errors.append("bundle metadata promotion entries must be objects")
            continue
        locale = item.get("locale")
        if not isinstance(locale, str) or not locale:
            errors.append(
                "bundle metadata promotion locale must be a non-empty string"
            )
            continue
        if locale in seen_bundle_locales:
            errors.append(f"duplicate locale-bundle promotion entry: {locale}")
        seen_bundle_locales.add(locale)
        current = validated_locale_catalog.get(locale)
        if not isinstance(current, dict):
            errors.append(f"bundle promotion references unknown locale: {locale}")
            continue
        if item.get("state") != BUNDLE_PROMOTION_STATE:
            errors.append(
                "locale-bundle promotion state must match planned wording-update mode: "
                f"{locale}"
            )
        preserve = item.get("preserve")
        if preserve != {
            "plugin_name": current.get("plugin_name"),
            "skill_name": current.get("skill_name"),
            "display": current.get("display"),
        }:
            errors.append(f"bundle promotion must preserve existing locale/plugin identity: {locale}")
        update = item.get("update")
        if not isinstance(update, dict) or set(update) != {"description"} or not isinstance(update.get("description"), str):
            errors.append(f"bundle promotion may update description only: {locale}")
        research_contains = item.get("prototype_research_contains")
        if not isinstance(research_contains, list) or set(research_contains) != expected_research:
            errors.append(f"bundle prototype research composition mismatch: {locale}")
        if item.get("production_suite_contains") != expected_public:
            errors.append(f"bundle production composition must use public Skill identities: {locale}")
        if expected_shared_by is not None and item.get("shared_by") != expected_shared_by:
            errors.append(f"locale-bundle wording promotion distribution set mismatch: {locale}")
        if expected_catalog is not None and item.get("production_catalog") != expected_catalog:
            errors.append(f"locale-bundle production catalog mismatch: {locale}")
        if expected_prototype_sources is not None and isinstance(locale, str):
            expected_source = expected_prototype_sources.get(locale)
            if item.get("prototype_source") != expected_source:
                errors.append(f"locale-bundle prototype source mismatch: {locale}")
            if isinstance(expected_source, str):
                try:
                    prototype = json.loads(
                        (root / expected_source).read_text(encoding="utf-8")
                    )
                except (OSError, json.JSONDecodeError, UnicodeError) as exc:
                    errors.append(
                        f"locale-bundle prototype source could not be read: {locale}: {exc}"
                    )
                else:
                    if (
                        isinstance(update, dict)
                        and update.get("description") != prototype.get("description")
                    ):
                        errors.append(
                            f"locale-bundle description must match prototype source: {locale}"
                        )
                    if item.get("prototype_research_contains") != prototype.get("contains"):
                        errors.append(
                            f"locale-bundle research composition must match prototype source: {locale}"
                        )
                    expected_dropped = _bundle_drop_fields(prototype)
                    if item.get("drop_prototype_fields_from_host_catalog") != expected_dropped:
                        errors.append(
                            "locale-bundle prototype drop-field set must match prototype source: "
                            f"{locale}"
                        )
        dropped = item.get("drop_prototype_fields_from_host_catalog")
        if not isinstance(dropped, list):
            errors.append(
                f"prototype-only bundle fields must not enter production locale catalog: {locale}"
            )
        elif expected_prototype_sources is None and (
            "contains" not in dropped or "status" not in dropped
        ):
            errors.append(
                f"prototype-only bundle fields must not enter production locale catalog: {locale}"
            )

    missing_bundle_locales = sorted(expected_bundle_locales - seen_bundle_locales)
    extra_bundle_locales = sorted(seen_bundle_locales - expected_bundle_locales)
    if missing_bundle_locales:
        errors.append(
            "bundle metadata promotion plan is missing declared locales: "
            f"{missing_bundle_locales}"
        )
    if extra_bundle_locales:
        errors.append(
            "bundle metadata promotion plan has undeclared locales: "
            f"{extra_bundle_locales}"
        )

    return errors


def main() -> int:
    try:
        adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        bundle_catalog_source = _bundle_catalog_source(adapter_plan)
        locale_catalog = json.loads((ROOT / bundle_catalog_source).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"production adapter metadata promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_adapter_promotion_authorities(
        ROOT,
        adapter_plan,
        descriptor,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        plan = plan_production_adapter_metadata_promotion(
            adapter_plan,
            descriptor,
            locale_catalog,
        )
    except (KeyError, OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"production adapter metadata promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_adapter_metadata_promotion_plan(
        plan,
        descriptor,
        locale_catalog,
        adapter_plan=adapter_plan,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())