from __future__ import annotations

import argparse
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def ask(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", default="ja-JP", choices=["ja-JP", "en-US"])
    parser.add_argument("--env", default="dev", choices=["dev", "staging", "prod"])
    parser.add_argument("--sharepoint-url", default="")
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args()

    scope = {"dev": "personal", "staging": "shared", "prod": "tenant"}[args.env]
    if args.non_interactive:
        values = {
            "DEVELOPER_NAME": "Your Name or Organization",
            "DEVELOPER_WEBSITE_URL": "https://example.com",
            "PRIVACY_URL": "https://example.com/privacy",
            "TERMS_URL": "https://example.com/terms",
        }
    else:
        values = {
            "DEVELOPER_NAME": ask("Developer name", "Your Name or Organization"),
            "DEVELOPER_WEBSITE_URL": ask("Website URL", "https://example.com"),
            "PRIVACY_URL": ask("Privacy URL", "https://example.com/privacy"),
            "TERMS_URL": ask("Terms URL", "https://example.com/terms"),
        }

    env_dir = ROOT / "adapters" / "microsoft-copilot" / args.locale / "env"
    env_dir.mkdir(parents=True, exist_ok=True)
    path = env_dir / f".env.{args.env}"
    content = [
        f"TEAMSFX_ENV={args.env}",
        f"M365_APP_ID={uuid4()}",
        f"AGENT_SCOPE={scope}",
        *(f"{key}={value}" for key, value in values.items()),
        f"SHAREPOINT_SITE_URL={args.sharepoint_url}",
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)}")
    print("Run: python scripts/build.py")


if __name__ == "__main__":
    main()
