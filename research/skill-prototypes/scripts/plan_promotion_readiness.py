#!/usr/bin/env python3
"""Observe research promotion evidence without issuing a promotion decision.

This planner reads existing repository authorities and reports what kind of
evidence is currently present. It deliberately does not collapse heterogeneous
evidence into a single ready/not-ready score and never authorizes production
promotion.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DESCRIPTOR = Path("research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json")
BUILDER_CONTRACT = Path("research/skill-prototypes/P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json")
PAIRED_RUN = Path("research/skill-prototypes/evals/THREE-LAYER-PAIRED-RUN-2026-09-06.md")
HANDOFF_CASES = Path("research/skill-prototypes/evals/CSW-HANDOFF-CASES.md")
HANDOFF_CAPSULE = Path("research/skill-prototypes/evals/L1-L2-HANDOFF-CAPSULE-2026-09-07.md")
HOST_MATERIALIZER = Path("research/skill-prototypes/scripts/materialize_host_package.py")
HOST_MATERIALIZER_TEST = Path("tests/test_research_host_package_materializer.py")
CROSS_SURFACE_TEST = Path("tests/test_research_host_package_cross_surface_parity.py")
BUILD_SCRIPT = Path("scripts/build.py")
VALIDATE_SCRIPT = Path("scripts/validate.py")
PRODUCTION_SKILL_SET = Path("src/skill-set.json")
RELEASE_PLAN = Path("research/skill-prototypes/P4-RELEASE-INTERNAL-COMPOSITION-PLAN-2026-09-07.md")

OBSERVATION_IDS = (
    "complete_checkout_execution",
    "public_name_recheck",
    "english_independent_review",
    "method_split_evaluation",
    "cross_layer_handoff",
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


def _obs(
    observation_id: str,
    state: str,
    *,
    authority: str | None = None,
    evidence: list[str] | None = None,
    evidence_kind: str,
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


def _mechanical_state(*, design_present: bool, implementation_present: bool) -> str:
    if design_present and implementation_present:
        return "design-and-mechanical-implementation-present-unexecuted"
    if design_present:
        return "design-only"
    if implementation_present:
        return "mechanical-generalization-present-unexecuted"
    return "not-observed-in-this-branch"


def observe_promotion_readiness(root: Path = ROOT) -> dict:
    descriptor = _load_json(root, DESCRIPTOR)
    builder_contract = _optional_json(root, BUILDER_CONTRACT)
    observations: list[dict] = []

    complete = descriptor.get("complete_checkout_validation")
    if not isinstance(complete, dict):
        raise ValueError("production descriptor must declare complete_checkout_validation")
    observations.append(
        _obs(
            "complete_checkout_execution",
            str(complete.get("status", "invalid")),
            authority=DESCRIPTOR.as_posix(),
            evidence=[str(complete.get("evidence"))] if complete.get("evidence") else [],
            evidence_kind="execution-gate",
            notes=["Static repository inspection is not command-execution evidence."],
            details={"required_commands": complete.get("required_commands", [])},
        )
    )

    name_gate = descriptor.get("public_name_recheck")
    if not isinstance(name_gate, dict):
        raise ValueError("production descriptor must declare public_name_recheck")
    skill_name_states = {
        str(skill.get("research_id")): skill.get("public_name_status")
        for skill in descriptor.get("skills", [])
        if isinstance(skill, dict) and skill.get("research_id")
    }
    name_evidence = name_gate.get("evidence")
    name_state = (
        "evidence-present"
        if isinstance(name_evidence, str) and _exists(root, Path(name_evidence))
        else "evidence-missing"
    )
    observations.append(
        _obs(
            "public_name_recheck",
            name_state,
            authority=DESCRIPTOR.as_posix(),
            evidence=[name_evidence] if isinstance(name_evidence, str) else [],
            evidence_kind="collision-recheck-evidence",
            notes=["A collision recheck is time-bounded evidence and is not promotion authorization."],
            details={"date": name_gate.get("date"), "skill_name_states": skill_name_states},
        )
    )

    english = descriptor.get("english_independent_review")
    if not isinstance(english, dict):
        raise ValueError("production descriptor must declare english_independent_review")
    english_evidence = [
        value
        for value in (english.get("packet"), english.get("targets"), english.get("completed_review"))
        if isinstance(value, str)
    ]
    observations.append(
        _obs(
            "english_independent_review",
            str(english.get("status", "invalid")),
            authority=DESCRIPTOR.as_posix(),
            evidence=english_evidence,
            evidence_kind="independent-review-gate",
            notes=["The review gate is reported verbatim; this observer does not infer completion."],
        )
    )

    paired = _text(root, PAIRED_RUN)
    if paired is None:
        paired_state = "not-observed-in-this-branch"
        paired_kind = "none"
    elif "same-model comparative authoring exercise" in paired:
        paired_state = "same-model-evidence-present"
        paired_kind = "same-model-comparative-evaluation"
    else:
        paired_state = "evaluation-evidence-present"
        paired_kind = "research-evaluation"
    observations.append(
        _obs(
            "method_split_evaluation",
            paired_state,
            authority=PAIRED_RUN.as_posix() if paired is not None else None,
            evidence=[PAIRED_RUN.as_posix()] if paired is not None else [],
            evidence_kind=paired_kind,
            notes=["Same-model comparative evidence must not be relabeled as independent evaluation."],
        )
    )

    handoff_cases = _text(root, HANDOFF_CASES)
    handoff_capsule = _text(root, HANDOFF_CAPSULE)
    if handoff_cases is not None and handoff_capsule is not None:
        handoff_state = "fixture-only"
        handoff_evidence = [HANDOFF_CASES.as_posix(), HANDOFF_CAPSULE.as_posix()]
    else:
        handoff_state = "not-observed-in-this-branch"
        handoff_evidence = [
            path.as_posix()
            for path, value in ((HANDOFF_CASES, handoff_cases), (HANDOFF_CAPSULE, handoff_capsule))
            if value is not None
        ]
    observations.append(
        _obs(
            "cross_layer_handoff",
            handoff_state,
            authority="research/skill-prototypes/evals/",
            evidence=handoff_evidence,
            evidence_kind="regression-fixture",
            notes=["Fixtures define failure/pass conditions but are not independent production-readiness evidence."],
        )
    )

    host_present = _exists(root, HOST_MATERIALIZER)
    host_test_present = _exists(root, HOST_MATERIALIZER_TEST)
    if host_present and host_test_present:
        host_state = "contract-present-unexecuted"
    elif host_present:
        host_state = "implementation-present-unexecuted"
    else:
        host_state = "not-observed-in-this-branch"
    observations.append(
        _obs(
            "host_package_materialization",
            host_state,
            authority=HOST_MATERIALIZER.as_posix() if host_present else None,
            evidence=[
                path.as_posix()
                for path in (HOST_MATERIALIZER, HOST_MATERIALIZER_TEST)
                if _exists(root, path)
            ],
            evidence_kind="repository-contract-and-tests",
            notes=["Presence of tests is not equivalent to a recorded test execution."],
        )
    )

    cross_surface_present = _exists(root, CROSS_SURFACE_TEST)
    observations.append(
        _obs(
            "cross_surface_host_parity",
            "oracle-present-unexecuted" if cross_surface_present else "not-observed-in-this-branch",
            authority=CROSS_SURFACE_TEST.as_posix() if cross_surface_present else None,
            evidence=[CROSS_SURFACE_TEST.as_posix()] if cross_surface_present else [],
            evidence_kind="cross-surface-byte-parity-oracle",
            notes=["The oracle records an invariant; execution evidence belongs to the complete-checkout gate."],
        )
    )

    source_modes = {
        str(skill.get("research_id")): (
            skill.get("production_source", {}).get("mode")
            if isinstance(skill.get("production_source"), dict)
            else None
        )
        for skill in descriptor.get("skills", [])
        if isinstance(skill, dict) and skill.get("research_id")
    }
    observations.append(
        _obs(
            "production_source_contract",
            "design-only" if descriptor.get("status") == "design-only" else "declared",
            authority=DESCRIPTOR.as_posix(),
            evidence=[DESCRIPTOR.as_posix()],
            evidence_kind="promotion-design",
            notes=["Research promotion design is not a production builder input."],
            details={"source_modes": source_modes},
        )
    )

    design_present = builder_contract is not None
    design_status = builder_contract.get("status") if builder_contract is not None else None
    build_text = _text(root, BUILD_SCRIPT) or ""
    builder_present = "def write_skill_tree(" in build_text and "def canonical_reference_files(" in build_text
    builder_evidence = [BUILD_SCRIPT.as_posix()]
    if design_present:
        builder_evidence.insert(0, BUILDER_CONTRACT.as_posix())
    observations.append(
        _obs(
            "production_builder_generalization",
            _mechanical_state(design_present=design_present, implementation_present=builder_present),
            authority=BUILDER_CONTRACT.as_posix() if design_present else BUILD_SCRIPT.as_posix(),
            evidence=builder_evidence,
            evidence_kind="production-mechanics-design-and-implementation",
            notes=[
                "A design contract and a production implementation are distinct evidence layers.",
                "This observation does not decide which sibling source kind should be promoted.",
            ],
            details={
                "design_status": design_status,
                "implementation_probe": builder_present,
                "planned_suite_descriptor": (
                    builder_contract.get("production_files", {}).get("planned_suite_descriptor")
                    if isinstance(builder_contract, dict)
                    else None
                ),
            },
        )
    )

    validate_text = _text(root, VALIDATE_SCRIPT) or ""
    validator_present = (
        "def check_projected_reference(" in validate_text
        and "def check_skill_entry_budget(" in validate_text
    )
    validator_evidence = [VALIDATE_SCRIPT.as_posix()]
    if design_present:
        validator_evidence.insert(0, BUILDER_CONTRACT.as_posix())
    observations.append(
        _obs(
            "production_validator_generalization",
            _mechanical_state(design_present=design_present, implementation_present=validator_present),
            authority=BUILDER_CONTRACT.as_posix() if design_present else VALIDATE_SCRIPT.as_posix(),
            evidence=validator_evidence,
            evidence_kind="production-validation-design-and-implementation",
            notes=["Validation requirements in a design contract are not proof that production validate.py implements them."],
            details={
                "design_status": design_status,
                "implementation_probe": validator_present,
                "validation_requirements": (
                    builder_contract.get("validation_requirements", {})
                    if isinstance(builder_contract, dict)
                    else {}
                ),
            },
        )
    )

    skill_set_present = _exists(root, PRODUCTION_SKILL_SET)
    observations.append(
        _obs(
            "production_inclusion_descriptor",
            "descriptor-present-unexecuted" if skill_set_present else "not-observed-in-this-branch",
            authority=PRODUCTION_SKILL_SET.as_posix() if skill_set_present else None,
            evidence=[PRODUCTION_SKILL_SET.as_posix()] if skill_set_present else [],
            evidence_kind="production-inclusion-boundary",
            notes=["Absence here does not negate a separate PR; this observer only reports the checked-out branch."],
        )
    )

    release_present = _exists(root, RELEASE_PLAN) and isinstance(descriptor.get("release_shape"), dict)
    observations.append(
        _obs(
            "release_internal_composition",
            "design-only" if release_present else "not-observed-in-this-branch",
            authority=RELEASE_PLAN.as_posix() if release_present else None,
            evidence=[RELEASE_PLAN.as_posix(), DESCRIPTOR.as_posix()] if release_present else [],
            evidence_kind="release-composition-design",
            notes=["A release composition plan is not a generated release validation result."],
        )
    )

    observations.append(
        _obs(
            "real_host_behavior",
            "unobserved",
            authority=None,
            evidence=[],
            evidence_kind="real-host-execution",
            notes=["No canonical real-host execution evidence authority is declared by this observer."],
        )
    )

    actual_ids = tuple(item["id"] for item in observations)
    if actual_ids != OBSERVATION_IDS:
        raise ValueError(f"promotion readiness observation order drifted: {actual_ids!r}")

    return {
        "schema": "csw.research-promotion-readiness-observation/v1",
        "descriptor": DESCRIPTOR.as_posix(),
        "descriptor_status": descriptor.get("status"),
        "observations": observations,
        "authorization": {
            "issued": False,
            "reason": (
                "This observer preserves heterogeneous evidence states and never issues "
                "production promotion authorization."
            ),
        },
    }


def main() -> int:
    try:
        report = observe_promotion_readiness(ROOT)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"research promotion readiness observation failed: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
