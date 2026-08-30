from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stage_environment(locale: str, environment: str) -> Path:
    source = ROOT / "adapters" / "microsoft-copilot" / locale / "env" / f".env.{environment}"
    project = ROOT / "dist" / locale / "microsoft-copilot" / "agent-project"
    target = project / "env" / source.name

    if not source.is_file():
        raise FileNotFoundError(
            f"deployment environment does not exist: {source.relative_to(ROOT)}; "
            "run scripts/init_m365_env.py first"
        )
    if not project.is_dir():
        raise FileNotFoundError(
            f"generated agent project does not exist: {project.relative_to(ROOT)}; "
            "run scripts/build.py first"
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage a deployment-only Microsoft 365 environment into a generated agent project."
    )
    parser.add_argument("--locale", default="ja-JP", choices=["ja-JP", "en-US"])
    parser.add_argument("--env", default="dev", choices=["dev", "staging", "prod"])
    args = parser.parse_args()

    try:
        target = stage_environment(args.locale, args.env)
    except FileNotFoundError as exc:
        print(exc)
        return 1

    print(f"Staged deployment-only environment: {target.relative_to(ROOT)}")
    print("Use it only for atk package/validate/provision/publish; public release packaging rejects it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
