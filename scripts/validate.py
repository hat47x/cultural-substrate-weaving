from __future__ import annotations

import json
import sys
from pathlib import Path

from common import (
    DIST, PLUGINS, ROOT, locale_source, locales, manifest, read_json,
    sha256, version, write_text
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_json_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if any(part in {".git", "dist", "__pycache__"} for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
    for path in DIST.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"Invalid generated JSON: {path.relative_to(ROOT)}: {exc}")


def check_versions(errors: list[str]) -> None:
    config = manifest()
    if config["version"] != version():
        fail(errors, "VERSION and src/manifest.json do not match")
    if (ROOT / "pyproject.toml").read_text(encoding="utf-8").find(f'version = "{version()}"') < 0:
        fail(errors, "pyproject.toml version does not match VERSION")


def check_locale_parity(errors: list[str]) -> None:
    config = manifest()
    canonical = config["canonical_locale"]
    canonical_files = {
        str(path.relative_to(locale_source(canonical)))
        for path in locale_source(canonical).rglob("*.md")
    }
    for locale in locales():
        files = {str(path.relative_to(locale_source(locale))) for path in locale_source(locale).rglob("*.md")}
        if files != canonical_files:
            missing = sorted(canonical_files - files)
            extra = sorted(files - canonical_files)
            fail(errors, f"Locale tree mismatch for {locale}; missing={missing}, extra={extra}")


def check_translation_hashes(errors: list[str]) -> None:
    config = manifest()
    canonical = config["canonical_locale"]
    tracking = read_json(ROOT / "i18n/translation-manifest.json")
    for rel, item in tracking["files"].items():
        source = locale_source(canonical) / rel
        if not source.exists():
            fail(errors, f"Translation manifest references missing canonical file: {rel}")
            continue
        current = sha256(source)
        if item.get("ja_sha256") != current or item.get("en_source_ja_sha256") != current:
            fail(errors, f"Translation is stale or unreviewed for canonical file: {rel}")
        if not (locale_source("en-US") / rel).exists():
            fail(errors, f"English translation missing: {rel}")


def check_semantics(errors: list[str]) -> None:
    spec = read_json(ROOT / "evals/semantic-retention.json")
    config = manifest()
    for locale in locales():
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in locale_source(locale).rglob("*.md"))
        router = (locale_source(locale) / config["router"]).read_text(encoding="utf-8")
        for phrase in spec[locale]["required_phrases"]:
            if phrase not in corpus:
                fail(errors, f"{locale}: required phrase missing: {phrase}")
        for phrase in spec[locale]["forbidden_in_router"]:
            if phrase in router:
                fail(errors, f"{locale}: forbidden router phrase present: {phrase}")


def check_modules(errors: list[str]) -> None:
    config = manifest()
    for locale in locales():
        router = (locale_source(locale) / config["router"]).read_text(encoding="utf-8")
        for module in config["modules"]:
            source = locale_source(locale) / module["source"]
            if not source.exists():
                fail(errors, f"{locale}: missing source module {module['source']}")
            if module["source"] not in router:
                fail(errors, f"{locale}: router does not reference {module['source']}")
            for profile in ("interactive", "metered"):
                generated = DIST / locale / "openai-skill" / profile / config["name"] / "references" / module["skill_reference"]
                if not generated.exists():
                    fail(errors, f"Missing generated reference: {generated.relative_to(ROOT)}")
                elif generated.read_bytes() != source.read_bytes():
                    fail(errors, f"Generated reference differs from {locale}/{module['source']}")


def check_budgets(errors: list[str]) -> dict:
    budgets = read_json(ROOT / "evals/token-budgets.json")
    config = manifest()
    metrics = {}
    claude_config = read_json(ROOT / "adapters/claude-code/locales.json")
    for locale in locales():
        router_size = (locale_source(locale) / config["router"]).stat().st_size
        if router_size > budgets["router_max_bytes"][locale]:
            fail(errors, f"{locale}: router exceeds byte budget: {router_size}")
        for profile in ("interactive", "metered"):
            size = (DIST / locale / "openai-skill" / profile / config["name"] / "SKILL.md").stat().st_size
            if size > budgets["openai_skill_md_max_bytes"][locale]:
                fail(errors, f"{locale}: OpenAI {profile} SKILL.md exceeds budget: {size}")
        c = claude_config[locale]
        claude_size = (PLUGINS / c["plugin_name"] / "skills" / c["skill_name"] / "SKILL.md").stat().st_size
        if claude_size > budgets["claude_skill_md_max_bytes"][locale]:
            fail(errors, f"{locale}: Claude SKILL.md exceeds budget: {claude_size}")
        agent = read_json(DIST / locale / "microsoft-copilot/agent-project/appPackage/declarativeAgent.json")
        m365_chars = len(agent["instructions"])
        if m365_chars > budgets["m365_instructions_max_chars"]:
            fail(errors, f"{locale}: Microsoft instructions exceed budget: {m365_chars}")
        knowledge_count = len(list((DIST / locale / "chatgpt-gpt/knowledge").glob("*.md")))
        if knowledge_count > budgets["gpt_knowledge_max_files"]:
            fail(errors, f"{locale}: GPT Knowledge file count exceeds budget: {knowledge_count}")
        metrics[locale] = {
            "router_bytes": router_size,
            "claude_skill_bytes": claude_size,
            "m365_instruction_chars": m365_chars,
            "gpt_knowledge_files": knowledge_count,
        }
    return metrics


def check_claude_marketplace(errors: list[str]) -> None:
    marketplace = read_json(ROOT / ".claude-plugin/marketplace.json")
    expected = {"csw-method-ja", "csw-method-en"}
    actual = {plugin["name"] for plugin in marketplace.get("plugins", [])}
    if actual != expected:
        fail(errors, f"Claude marketplace plugins mismatch: {actual}")
    for plugin in marketplace.get("plugins", []):
        source = ROOT / plugin["source"]
        if not source.exists():
            fail(errors, f"Claude plugin source missing: {plugin['source']}")
        manifest_path = source / ".claude-plugin/plugin.json"
        if read_json(manifest_path).get("version") != version():
            fail(errors, f"Claude plugin version mismatch: {plugin['name']}")


def check_m365(errors: list[str]) -> None:
    for locale in locales():
        base = DIST / locale / "microsoft-copilot/agent-project/appPackage"
        agent = read_json(base / "declarativeAgent.json")
        if agent.get("version") != "v1.8":
            fail(errors, f"{locale}: declarative agent schema is not v1.8")
        if len(agent.get("conversation_starters", [])) > 12:
            fail(errors, f"{locale}: too many conversation starters")
        app = read_json(base / "manifest.json")
        if "copilotAgents" not in app:
            fail(errors, f"{locale}: Microsoft app manifest lacks copilotAgents")
        for icon in ("color.png", "outline.png"):
            if not (base / icon).exists():
                fail(errors, f"{locale}: Microsoft icon missing: {icon}")


def main() -> None:
    errors: list[str] = []
    check_json_files(errors)
    check_versions(errors)
    check_locale_parity(errors)
    check_translation_hashes(errors)
    check_semantics(errors)
    check_modules(errors)
    metrics = check_budgets(errors)
    check_claude_marketplace(errors)
    check_m365(errors)
    report = {
        "version": version(),
        "locales": locales(),
        "ok": not errors,
        "errors": errors,
        "metrics": metrics,
    }
    write_text(DIST / "reports/validation-report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Multilingual validation passed")


if __name__ == "__main__":
    main()
