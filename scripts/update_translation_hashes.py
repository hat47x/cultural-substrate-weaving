from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import ROOT, locale_source, manifest, sha256


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mark a translation as reviewed against the current canonical file hashes."
    )
    parser.add_argument("--locale", required=True, choices=["en-US"])
    args = parser.parse_args()

    config = manifest()
    canonical = config["canonical_locale"]
    path = ROOT / "i18n/translation-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for source in sorted(locale_source(canonical).rglob("*.md")):
        rel = str(source.relative_to(locale_source(canonical)))
        translated = locale_source(args.locale) / rel
        if not translated.exists():
            raise SystemExit(f"Missing translation: {translated}")
        digest = sha256(source)
        data["files"][rel] = {
            "ja_sha256": digest,
            "en_present": True,
            "en_source_ja_sha256": digest,
            "en_status": "translated",
        }

    data["locales"][args.locale]["source_version"] = config["version"]

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated translation source hashes and source version.")
    print("Use this command only after reviewing the translation against the current canonical source.")


if __name__ == "__main__":
    main()
