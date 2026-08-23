from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from common import (
    ADAPTERS, DIST, PLUGINS, ROOT, clean_generated, copy_file, locale_heading,
    locale_short, locale_source, locales, load_env_file, manifest,
    replace_router_links, sha256, version, write_text
)


def skill_frontmatter(name: str, description: str, claude_explicit: bool = False) -> str:
    lines = ["---", f"name: {name}", f"description: {description}"]
    if claude_explicit:
        lines.append("disable-model-invocation: true")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def copy_references(locale: str, target: Path, config: dict) -> None:
    source_root = locale_source(locale)
    for module in config["modules"]:
        copy_file(source_root / module["source"], target / "references" / module["skill_reference"])


def concatenate_modules(locale: str, config: dict, module_paths: list[str]) -> str:
    source_root = locale_source(locale)
    sections = [(source_root / rel).read_text(encoding="utf-8").rstrip() for rel in module_paths]
    return "\n\n---\n\n".join(sections) + "\n"


def build_openai(locale: str, config: dict, router: str) -> None:
    locale_info = config["locales"][locale]
    for profile in ("interactive", "metered"):
        target = DIST / locale / "openai-skill" / profile / config["name"]
        content = skill_frontmatter(config["name"], locale_info["description"])
        content += replace_router_links(router, config["modules"])
        write_text(target / "SKILL.md", content)
        copy_references(locale, target, config)
        copy_file(
            ADAPTERS / "openai-skill" / locale / f"openai.{profile}.yaml",
            target / "agents" / "openai.yaml",
        )


def build_claude(locale: str, config: dict, router: str, claude_config: dict) -> dict:
    c = claude_config[locale]
    plugin_root = PLUGINS / c["plugin_name"]
    skill_root = plugin_root / "skills" / c["skill_name"]

    plugin_manifest = {
        "name": c["plugin_name"],
        "description": c["description"],
        "version": version(),
        "author": {"name": "hat47x"},
        "homepage": "https://github.com/hat47x/cultural-substrate-weaving",
        "repository": "https://github.com/hat47x/cultural-substrate-weaving",
        "license": "MIT",
    }
    write_text(
        plugin_root / ".claude-plugin" / "plugin.json",
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
    )
    content = skill_frontmatter(c["skill_name"], config["locales"][locale]["description"], claude_explicit=True)
    content += replace_router_links(router, config["modules"])
    write_text(skill_root / "SKILL.md", content)
    copy_references(locale, skill_root, config)

    readme = (ADAPTERS / "claude-code" / locale / "README.md").read_text(encoding="utf-8")
    write_text(plugin_root / "README.md", readme.replace("{{VERSION}}", version()))

    # A locale-specific standalone marketplace package.
    dist_root = DIST / locale / "claude-plugin"
    shutil.copytree(plugin_root, dist_root / "plugins" / c["plugin_name"], dirs_exist_ok=True)
    standalone = {
        "name": f"cultural-substrate-weaving-{locale_short(locale)}",
        "owner": {"name": "hat47x"},
        "description": c["description"],
        "version": version(),
        "plugins": [{
            "name": c["plugin_name"],
            "source": f"./plugins/{c['plugin_name']}",
            "description": c["description"],
            "version": version(),
            "category": "productivity",
            "tags": ["analysis", "design", "writing", "architecture", locale_short(locale)],
        }],
    }
    write_text(
        dist_root / ".claude-plugin" / "marketplace.json",
        json.dumps(standalone, ensure_ascii=False, indent=2) + "\n",
    )

    return {
        "name": c["plugin_name"],
        "source": f"./plugins/{c['plugin_name']}",
        "description": c["description"],
        "version": version(),
        "category": "productivity",
        "tags": ["analysis", "design", "writing", "architecture", locale_short(locale)],
    }


def build_codex_plugin(locale: str, claude_config: dict) -> dict:
    """Add a Codex plugin manifest to the plugin directory Claude Code already uses.

    Codex and Claude Code both read skills from `skills/<name>/SKILL.md`, so one
    plugin directory carries both manifests. Only the manifest and the
    marketplace catalog differ.
    """
    c = claude_config[locale]
    plugin_manifest = {
        "name": c["plugin_name"],
        "version": version(),
        "description": c["description"],
        "author": {"name": "hat47x"},
        "homepage": "https://github.com/hat47x/cultural-substrate-weaving",
        "repository": "https://github.com/hat47x/cultural-substrate-weaving",
        "license": "MIT",
        "keywords": ["analysis", "design", "writing", "architecture", locale_short(locale)],
        "skills": "./skills/",
        "interface": {
            "displayName": c["display"],
            "shortDescription": c["description"],
            "developerName": "hat47x",
            "category": "Productivity",
        },
    }
    write_text(
        PLUGINS / c["plugin_name"] / ".codex-plugin" / "plugin.json",
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
    )
    return {
        "name": c["plugin_name"],
        "source": {"source": "local", "path": f"./plugins/{c['plugin_name']}"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
        "category": "Productivity",
    }


def write_root_codex_marketplace(plugin_entries: list[dict]) -> None:
    marketplace = {
        "name": "cultural-substrate-weaving",
        "interface": {"displayName": "Cultural Substrate Weaving"},
        "plugins": plugin_entries,
    }
    write_text(
        ROOT / ".agents" / "plugins" / "marketplace.json",
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
    )


def build_gpt(locale: str, config: dict, router: str) -> None:
    target = DIST / locale / "chatgpt-gpt"
    prefix = (ADAPTERS / "chatgpt-gpt" / locale / "instructions-prefix.md").read_text(encoding="utf-8").rstrip()
    write_text(target / "instructions.md", prefix + "\n\n" + router)
    for filename, modules in config["knowledge_groups"].items():
        write_text(target / "knowledge" / filename, concatenate_modules(locale, config, modules))
    copy_file(
        ADAPTERS / "chatgpt-gpt" / locale / "conversation-starters.md",
        target / "conversation-starters.md",
    )
    copy_file(
        ADAPTERS / "chatgpt-gpt" / locale / "deploy-checklist.md",
        target / "deploy-checklist.md",
    )
    write_text(target / "VERSION.txt", f"{version()}\nlocale={locale}\n")


def substitute_manifest(template: dict, current_version: str):
    raw = json.dumps(template, ensure_ascii=False).replace("{{VERSION}}", current_version)
    return json.loads(raw)


def build_m365(locale: str, config: dict, router: str) -> None:
    target = DIST / locale / "microsoft-copilot"
    project = target / "agent-project"
    app_package = project / "appPackage"

    prefix = (ADAPTERS / "microsoft-copilot" / locale / "instructions-prefix.md").read_text(encoding="utf-8").rstrip()
    compact_router = router.split(locale_heading(locale), 1)[0].rstrip()
    instructions = prefix + "\n\n" + compact_router
    if len(instructions) > 8000:
        raise RuntimeError(f"{locale} Microsoft instructions exceed 8000 characters: {len(instructions)}")

    starters = json.loads(
        (ADAPTERS / "microsoft-copilot" / locale / "conversation-starters.json").read_text(encoding="utf-8")
    )
    names = {
        "ja-JP": ("Cultural Substrate Weaving — 日本語", "文化的体系とKJ法で構造候補と空白を探索し、対象側で検証します。"),
        "en-US": ("Cultural Substrate Weaving — English", "Explores structure candidates and gaps with cultural frameworks and KJ, then validates them on the target."),
    }
    agent = {
        "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.8/schema.json",
        "version": "v1.8",
        "name": names[locale][0],
        "description": names[locale][1],
        "instructions": instructions,
        "conversation_starters": starters,
    }

    env_path = ADAPTERS / "microsoft-copilot" / locale / "env" / ".env.dev"
    env_values = load_env_file(env_path)
    sharepoint_url = os.environ.get(f"CSW_M365_SHAREPOINT_SITE_URL_{locale.replace('-', '_')}", "").strip()
    if not sharepoint_url:
        sharepoint_url = env_values.get("SHAREPOINT_SITE_URL", "").strip()
    if sharepoint_url:
        agent["capabilities"] = [{
            "name": "OneDriveAndSharePoint",
            "items_by_url": [{"url": sharepoint_url}],
        }]

    template = json.loads(
        (ADAPTERS / "microsoft-copilot" / locale / "manifest.template.json").read_text(encoding="utf-8")
    )
    write_text(
        app_package / "manifest.json",
        json.dumps(substitute_manifest(template, version()), ensure_ascii=False, indent=2) + "\n",
    )
    write_text(
        app_package / "declarativeAgent.json",
        json.dumps(agent, ensure_ascii=False, indent=2) + "\n",
    )
    for icon in ("color.png", "outline.png"):
        copy_file(ADAPTERS / "microsoft-copilot" / "common" / icon, app_package / icon)
    copy_file(
        ADAPTERS / "microsoft-copilot" / "common" / "m365agents.yml",
        project / "m365agents.yml",
    )
    for example in (ADAPTERS / "microsoft-copilot" / "common" / "env").glob("*.example"):
        copy_file(example, project / "env" / example.name)
    if env_path.parent.exists():
        for actual in env_path.parent.glob(".env.*"):
            if not actual.name.endswith(".example"):
                copy_file(actual, project / "env" / actual.name)

    for filename, modules in config["knowledge_groups"].items():
        write_text(target / "knowledge" / filename, concatenate_modules(locale, config, modules))
    write_text(target / "instructions.txt", instructions + "\n")
    guide = "See docs/ja/platforms/microsoft-copilot.md\n" if locale == "ja-JP" else "See docs/en/platforms/microsoft-copilot.md\n"
    write_text(target / "README.txt", guide)


def build_canonical(locale: str) -> None:
    shutil.copytree(locale_source(locale), DIST / locale / "canonical-docs", dirs_exist_ok=True)


def write_root_marketplace(plugin_entries: list[dict]) -> None:
    marketplace = {
        "name": "cultural-substrate-weaving",
        "owner": {"name": "hat47x"},
        "description": "Localized skills for cultural-framework exploration, KJ integration, and target-side validation.",
        "version": version(),
        "plugins": plugin_entries,
    }
    write_text(
        ROOT / ".claude-plugin" / "marketplace.json",
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
    )


def write_release_manifest() -> None:
    files = []
    for path in sorted(p for p in DIST.rglob("*") if p.is_file()):
        if path.name == "release-manifest.json":
            continue
        files.append({
            "path": str(path.relative_to(DIST)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    write_text(
        DIST / "release-manifest.json",
        json.dumps({"version": version(), "locales": locales(), "files": files}, ensure_ascii=False, indent=2) + "\n",
    )


def main() -> None:
    clean_generated()
    config = manifest()
    claude_config = json.loads((ADAPTERS / "claude-code" / "locales.json").read_text(encoding="utf-8"))
    plugin_entries = []
    codex_entries = []

    for locale in locales():
        router = (locale_source(locale) / config["router"]).read_text(encoding="utf-8")
        build_openai(locale, config, router)
        plugin_entries.append(build_claude(locale, config, router, claude_config))
        codex_entries.append(build_codex_plugin(locale, claude_config))
        build_gpt(locale, config, router)
        build_m365(locale, config, router)
        build_canonical(locale)

    write_root_marketplace(plugin_entries)
    write_root_codex_marketplace(codex_entries)
    write_release_manifest()
    print(f"Built {config['name']} v{version()} for {', '.join(locales())}")


if __name__ == "__main__":
    main()
