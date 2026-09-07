#!/usr/bin/env python3
"""Observe heterogeneous promotion evidence without issuing a promotion decision."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DESCRIPTOR = Path("research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json")
BUILDER_CONTRACT = Path("research/skill-prototypes/P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json")
SUITE_MANIFEST = Path("research/skill-prototypes/suite-manifest.json")
TRANSLATION_STATUS = Path("research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json")
PAIRED_RUN = Path("research/skill-prototypes/evals/THREE-LAYER-PAIRED-RUN-2026-09-06.md")
HANDOFF_CASES = Path("research/skill-prototypes/evals/CSW-HANDOFF-CASES.md")
HANDOFF_CAPSULE = Path("research/skill-prototypes/evals/L1-L2-HANDOFF-CAPSULE-2026-09-07.md")
TENSION_CASES = Path("research/skill-prototypes/evals/CSW-TENSION-EMERGENCE-CASES.md")
TENSION_TEST = Path("tests/test_research_tension_emergence.py")
HOST_MATERIALIZER = Path("research/skill-prototypes/scripts/materialize_host_package.py")
HOST_MATERIALIZER_TEST = Path("tests/test_research_host_package_materializer.py")
CROSS_SURFACE_TEST = Path("tests/test_research_host_package_cross_surface_parity.py")
RELEASE_PLAN = Path("research/skill-prototypes/P4-RELEASE-INTERNAL-COMPOSITION-PLAN-2026-09-07.md")

OBSERVATION_IDS = (
    "complete_checkout_execution",
    "translation_refresh_state",
    "public_name_recheck",
    "english_independent_review",
    "method_split_evaluation",
    "method_definition_parity",
    "cross_layer_handoff",
    "csw_tension_ownership_evaluation",
    "host_package_materialization",
    "cross_surface_host_parity",
    "production_source_contract",
    "production_builder_generalization",
    "production_validator_generalization",
    "production_inclusion_descriptor",
    "release_internal_composition",
    "real_host_behavior",
)


def _load_json(root: Path, relative: Path) -> dict:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain a JSON object")
    return value


def _optional_json(root: Path, relative: Path) -> dict | None:
    return _load_json(root, relative) if (root / relative).is_file() else None


def _text(root: Path, relative: Path) -> str | None:
    path = root / relative
    return path.read_text(encoding="utf-8") if path.is_file() else None


def _exists(root: Path, relative: Path) -> bool:
    return (root / relative).is_file()


def _declared_field(text: str | None, field: str) -> str | None:
    if text is None:
        return None
    prefix = f"{field}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            return value or None
    return None


def _obs(
    observation_id: str,
    state: str,
    *,
    evidence_kind: str,
    authority: str | None = None,
    evidence: list[str] | None = None,
    notes: list[str] | None = None,
    details: dict | None = None,
) -> dict:
    return {
        "id": observation_id,
        "state": state,
        "evidence_kind": evidence_kind,
        "authority": authority,
        "evidence": evidence or [],
        "notes": notes or [],
        "details": details or {},
        "production_promotion_authorized": False,
    }


def _design_and_file_state(*, design_present: bool, production_file_present: bool) -> str:
    if design_present and production_file_present:
        return "design-and-production-file-present-unclassified"
    if design_present:
        return "design-only"
    if production_file_present:
        return "production-file-present-unclassified"
    return "not-observed-in-this-branch"


def _production_path(contract: dict | None, key: str) -> Path | None:
    if contract is None:
        return None
    production_files = contract.get("production_files")
    if not isinstance(production_files, dict):
        return None
    value = production_files.get(key)
    return Path(value) if isinstance(value, str) else None


def _iterative_parity_check(root: Path, suite: dict) -> tuple[str, list[str], dict]:
    skill = next(
        (
            item
            for item in suite.get("skills", [])
            if isinstance(item, dict) and item.get("id") == "iterative-inquiry-synthesis"
        ),
        None,
    )
    if not isinstance(skill, dict):
        return "not-observed-in-this-branch", [], {}
    checks = skill.get("checks")
    declared = [value for value in checks if isinstance(value, str)] if isinstance(checks, list) else []
    present = [value for value in declared if _exists(root, Path(value))]
    if declared and len(present) == len(declared):
        state = "declared-checks-present-unexecuted"
    elif declared:
        state = "declared-checks-incomplete"
    else:
        state = "not-observed-in-this-branch"
    return state, present, {"declared_checks": declared}


def observe_promotion_readiness(root: Path = ROOT) -> dict:
    descriptor = _load_json(root, DESCRIPTOR)
    suite = _load_json(root, SUITE_MANIFEST)
    builder_contract = _optional_json(root, BUILDER_CONTRACT)
    observations: list[dict] = []

    complete = descriptor.get("complete_checkout_validation")
    if not isinstance(complete, dict):
        raise ValueError("production descriptor must declare complete_checkout_validation")
    observations.append(_obs(
        "complete_checkout_execution",
        str(complete.get("status", "invalid")),
        authority=DESCRIPTOR.as_posix(),
        evidence=[str(complete.get("evidence"))] if complete.get("evidence") else [],
        evidence_kind="execution-gate",
        notes=["Static repository inspection is not command-execution evidence."],
        details={"required_commands": complete.get("required_commands", [])},
    ))

    translation = _optional_json(root, TRANSLATION_STATUS)
    if translation is None:
        translation_state = "not-observed-in-this-branch"
        translation_evidence: list[str] = []
        translation_details: dict = {}
    else:
        translation_state = str(translation.get("status", "invalid"))
        translation_evidence = [TRANSLATION_STATUS.as_posix()]
        human_record = translation.get("human_record")
        if isinstance(human_record, str):
            translation_evidence.append(human_record)
        translation_details = {
            "locale": translation.get("locale"),
            "expected_stale_files": translation.get("expected_stale_files", []),
            "refresh_command": translation.get("refresh_command"),
            "followup_commands": translation.get("followup_commands", []),
        }
    observations.append(_obs(
        "translation_refresh_state",
        translation_state,
        authority=TRANSLATION_STATUS.as_posix() if translation is not None else None,
        evidence=translation_evidence,
        evidence_kind="translation-source-tracking-gate",
        notes=[
            "Hash synchronization records source tracking; it is not independent translation review.",
            "Translation refresh state never authorizes production promotion by itself.",
        ],
        details=translation_details,
    ))

    name_gate = descriptor.get("public_name_recheck")
    if not isinstance(name_gate, dict):
        raise ValueError("production descriptor must declare public_name_recheck")
    name_evidence = name_gate.get("evidence")
    name_state = (
        "evidence-present"
        if isinstance(name_evidence, str) and _exists(root, Path(name_evidence))
        else "evidence-missing"
    )
    skill_name_states = {
        str(skill.get("research_id")): skill.get("public_name_status")
        for skill in descriptor.get("skills", [])
        if isinstance(skill, dict) and skill.get("research_id")
    }
    observations.append(_obs(
        "public_name_recheck",
        name_state,
        authority=DESCRIPTOR.as_posix(),
        evidence=[name_evidence] if isinstance(name_evidence, str) else [],
        evidence_kind="collision-recheck-evidence",
        notes=["A collision recheck is time-bounded evidence, not promotion authorization."],
        details={"date": name_gate.get("date"), "skill_name_states": skill_name_states},
    ))

    english = descriptor.get("english_independent_review")
    if not isinstance(english, dict):
        raise ValueError("production descriptor must declare english_independent_review")
    english_evidence = [
        value
        for value in (
            english.get("packet"),
            english.get("targets"),
            english.get("technical_asset_localization"),
            english.get("completed_review"),
        )
        if isinstance(value, str)
    ]
    observations.append(_obs(
        "english_independent_review",
        str(english.get("status", "invalid")),
        authority=DESCRIPTOR.as_posix(),
        evidence=english_evidence,
        evidence_kind="independent-review-gate",
        notes=["Review packet/targets do not imply review completion."],
    ))

    paired = _text(root, PAIRED_RUN)
    evaluation_type = _declared_field(paired, "Evaluation type")
    evaluation_status = _declared_field(paired, "Status")
    if paired is None:
        paired_state = "not-observed-in-this-branch"
        paired_kind = "none"
    elif evaluation_type is None:
        paired_state = "evaluation-record-present-unclassified"
        paired_kind = "self-described-research-evaluation"
    elif evaluation_type.lower().startswith("same-model"):
        paired_state = "same-model-evidence-present"
        paired_kind = "self-described-same-model-comparative-evaluation"
    else:
        paired_state = "evaluation-record-present"
        paired_kind = "self-described-research-evaluation"
    observations.append(_obs(
        "method_split_evaluation",
        paired_state,
        authority=PAIRED_RUN.as_posix() if paired is not None else None,
        evidence=[PAIRED_RUN.as_posix()] if paired is not None else [],
        evidence_kind=paired_kind,
        notes=[
            "The observer reads the evidence record's declared Evaluation type field; it does not classify evidence strength by prose substring search.",
            "Same-model comparative evidence is not independent review.",
        ],
        details={"declared_status": evaluation_status, "declared_evaluation_type": evaluation_type},
    ))

    parity_state, parity_evidence, parity_details = _iterative_parity_check(root, suite)
    observations.append(_obs(
        "method_definition_parity",
        parity_state,
        authority=SUITE_MANIFEST.as_posix(),
        evidence=parity_evidence,
        evidence_kind="declared-method-parity-check",
        notes=["Declared check presence is not complete-checkout execution evidence."],
        details=parity_details,
    ))

    handoff_evidence = [
        path.as_posix()
        for path in (HANDOFF_CASES, HANDOFF_CAPSULE)
        if _exists(root, path)
    ]
    observations.append(_obs(
        "cross_layer_handoff",
        "fixture-only" if len(handoff_evidence) == 2 else "not-observed-in-this-branch",
        authority="research/skill-prototypes/evals/" if handoff_evidence else None,
        evidence=handoff_evidence,
        evidence_kind="regression-fixture",
        notes=["Fixtures define boundaries but are not executed independent evaluation."],
    ))

    tension_evidence = [
        path.as_posix()
        for path in (TENSION_CASES, TENSION_TEST)
        if _exists(root, path)
    ]
    observations.append(_obs(
        "csw_tension_ownership_evaluation",
        "fixture-and-regression-present-unexecuted"
        if len(tension_evidence) == 2
        else "not-observed-in-this-branch",
        authority=TENSION_CASES.as_posix() if _exists(root, TENSION_CASES) else None,
        evidence=tension_evidence,
        evidence_kind="csw-specific-regression-fixture-and-test",
        notes=[
            "The observer records fixture/test presence only; it does not infer invariant coverage from prose or Python function-name substrings.",
            "Regression source presence is not regression execution PASS.",
        ],
    ))

    host_present = _exists(root, HOST_MATERIALIZER)
    host_test_present = _exists(root, HOST_MATERIALIZER_TEST)
    host_state = (
        "contract-present-unexecuted"
        if host_present and host_test_present
        else "implementation-file-present-unclassified"
        if host_present
        else "not-observed-in-this-branch"
    )
    observations.append(_obs(
        "host_package_materialization",
        host_state,
        authority=HOST_MATERIALIZER.as_posix() if host_present else None,
        evidence=[
            path.as_posix()
            for path in (HOST_MATERIALIZER, HOST_MATERIALIZER_TEST)
            if _exists(root, path)
        ],
        evidence_kind="repository-contract-and-tests",
        notes=["Presence of tests is not a recorded test execution."],
    ))

    cross_surface_present = _exists(root, CROSS_SURFACE_TEST)
    observations.append(_obs(
        "cross_surface_host_parity",
        "oracle-present-unexecuted" if cross_surface_present else "not-observed-in-this-branch",
        authority=CROSS_SURFACE_TEST.as_posix() if cross_surface_present else None,
        evidence=[CROSS_SURFACE_TEST.as_posix()] if cross_surface_present else [],
        evidence_kind="cross-surface-byte-parity-oracle",
        notes=["Oracle presence and oracle execution remain distinct."],
    ))

    source_modes = {
        str(skill.get("research_id")): (
            skill.get("production_source", {}).get("mode")
            if isinstance(skill.get("production_source"), dict)
            else None
        )
        for skill in descriptor.get("skills", [])
        if isinstance(skill, dict) and skill.get("research_id")
    }
    observations.append(_obs(
        "production_source_contract",
        "design-only" if descriptor.get("status") == "design-only" else "declared",
        authority=DESCRIPTOR.as_posix(),
        evidence=[DESCRIPTOR.as_posix()],
        evidence_kind="promotion-design",
        notes=["Research promotion design is not a production builder input."],
        details={"source_modes": source_modes},
    ))

    design_present = builder_contract is not None
    design_status = builder_contract.get("status") if builder_contract is not None else None
    builder_path = _production_path(builder_contract, "builder")
    validator_path = _production_path(builder_contract, "validator")

    builder_file_present = builder_path is not None and _exists(root, builder_path)
    builder_evidence = [BUILDER_CONTRACT.as_posix()] if design_present else []
    if builder_file_present and builder_path is not None:
        builder_evidence.append(builder_path.as_posix())
    observations.append(_obs(
        "production_builder_generalization",
        _design_and_file_state(
            design_present=design_present,
            production_file_present=builder_file_present,
        ),
        authority=BUILDER_CONTRACT.as_posix() if design_present else None,
        evidence=builder_evidence,
        evidence_kind="production-mechanics-design-and-file-presence",
        notes=[
            "The observer does not infer generalized implementation from internal function names or source substrings.",
            "Checked-out production-file presence is not generated-artifact parity or execution PASS.",
        ],
        details={"design_status": design_status, "production_file": builder_path.as_posix() if builder_path else None},
    ))

    validator_file_present = validator_path is not None and _exists(root, validator_path)
    validator_evidence = [BUILDER_CONTRACT.as_posix()] if design_present else []
    if validator_file_present and validator_path is not None:
        validator_evidence.append(validator_path.as_posix())
    observations.append(_obs(
        "production_validator_generalization",
        _design_and_file_state(
            design_present=design_present,
            production_file_present=validator_file_present,
        ),
        authority=BUILDER_CONTRACT.as_posix() if design_present else None,
        evidence=validator_evidence,
        evidence_kind="production-validation-design-and-file-presence",
        notes=[
            "The observer does not infer validator generalization from internal function names or source substrings.",
            "Checked-out production-file presence is not validation execution PASS.",
        ],
        details={"design_status": design_status, "production_file": validator_path.as_posix() if validator_path else None},
    ))

    planned_descriptor = _production_path(builder_contract, "planned_suite_descriptor")
    inclusion_present = planned_descriptor is not None and _exists(root, planned_descriptor)
    observations.append(_obs(
        "production_inclusion_descriptor",
        "descriptor-present-unexecuted" if inclusion_present else "not-observed-in-this-branch",
        authority=planned_descriptor.as_posix() if inclusion_present and planned_descriptor else None,
        evidence=[planned_descriptor.as_posix()] if inclusion_present and planned_descriptor else [],
        evidence_kind="production-inclusion-boundary",
        notes=[
            "The planned production descriptor path comes from the builder contract; the observer does not guess a legacy filename.",
            "Only the checked-out branch is observed; PR state is not inferred.",
        ],
    ))

    release_present = _exists(root, RELEASE_PLAN) and isinstance(descriptor.get("release_shape"), dict)
    observations.append(_obs(
        "release_internal_composition",
        "design-only" if release_present else "not-observed-in-this-branch",
        authority=RELEASE_PLAN.as_posix() if release_present else None,
        evidence=[RELEASE_PLAN.as_posix(), DESCRIPTOR.as_posix()] if release_present else [],
        evidence_kind="release-composition-design",
        notes=["A release composition plan is not a generated release validation result."],
    ))

    observations.append(_obs(
        "real_host_behavior",
        "unobserved",
        authority=None,
        evidence=[],
        evidence_kind="real-host-execution",
        notes=["Package prototypes and metadata tests do not establish real-host invocation/routing behavior."],
    ))

    actual_ids = tuple(item["id"] for item in observations)
    if actual_ids != OBSERVATION_IDS:
        raise ValueError(f"promotion readiness observation order drifted: {actual_ids!r}")

    return {
        "schema": "csw.research-promotion-readiness-observation/v3",
        "descriptor": DESCRIPTOR.as_posix(),
        "descriptor_status": descriptor.get("status"),
        "observations": observations,
        "authorization": {
            "issued": False,
            "reason": "This observer preserves heterogeneous evidence states and never issues production promotion authorization.",
        },
    }


def main() -> int:
    try:
        report = observe_promotion_readiness(ROOT)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, StopIteration) as exc:
        print(f"research promotion readiness observation failed: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
