from __future__ import annotations

import json
from pathlib import Path

from common import DIST, PLUGINS, ROOT, locale_source, locales, manifest, read_json, write_text


def estimate_tokens(locale: str, chars: int) -> dict[str, int]:
    if locale == "ja-JP":
        return {"low": round(chars / 1.2), "high": round(chars / 0.75)}
    return {"low": round(chars / 4.5), "high": round(chars / 3.0)}


def entry(locale: str, path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {
        "locale": locale,
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "characters": len(text),
        "estimated_tokens": estimate_tokens(locale, len(text)),
    }


def main() -> None:
    config = manifest()
    claude = read_json(ROOT / "adapters/claude-code/locales.json")
    files = []
    references = []
    corpus = {}
    for locale in locales():
        c = claude[locale]
        router = locale_source(locale) / config["router"]
        paths = [
            router,
            DIST / locale / "openai-skill/interactive" / config["name"] / "SKILL.md",
            DIST / locale / "openai-skill/metered" / config["name"] / "SKILL.md",
            PLUGINS / c["plugin_name"] / "skills" / c["skill_name"] / "SKILL.md",
            DIST / locale / "chatgpt-gpt/instructions.md",
            DIST / locale / "microsoft-copilot/instructions.txt",
        ]
        files.extend(entry(locale, path) for path in paths)
        sources = sorted(locale_source(locale).rglob("*.md"))
        references.extend(entry(locale, path) for path in sources if path != router)
        chars = sum(len(path.read_text(encoding="utf-8")) for path in sources)
        corpus[locale] = {
            "files": len(sources),
            "bytes": sum(path.stat().st_size for path in sources),
            "characters": chars,
            "estimated_tokens": estimate_tokens(locale, chars),
        }
    report = {
        "note": "Planning ranges only; platform tokenizers differ.",
        "corpus": corpus,
        "delivery_files": files,
        "reference_files": references,
    }
    write_text(DIST / "reports/token-budget.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for item in files + references:
        t = item["estimated_tokens"]
        print(f"{item['locale']} {item['path']}: {item['bytes']} bytes, approx {t['low']}-{t['high']} tokens")
    for locale, item in corpus.items():
        t = item["estimated_tokens"]
        print(f"{locale} CORPUS ({item['files']} files): {item['bytes']} bytes, approx {t['low']}-{t['high']} tokens")


if __name__ == "__main__":
    main()
