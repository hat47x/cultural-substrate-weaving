from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location("stage_m365_env", SCRIPTS / "stage_m365_env.py")
assert SPEC and SPEC.loader
STAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAGE)


class M365TenantBoundaryTests(unittest.TestCase):
    def test_public_build_does_not_read_or_copy_local_env_files(self) -> None:
        build = (SCRIPTS / "build.py").read_text(encoding="utf-8")
        self.assertNotIn("load_env_file", build)
        self.assertNotIn('glob(".env.*")', build)
        self.assertIn("explicit_m365_sharepoint_url", build)
        self.assertIn("CSW_M365_SHAREPOINT_SITE_URL", build)

    def test_canonical_build_outputs_are_tenant_neutral(self) -> None:
        for locale in ("ja-JP", "en-US"):
            project = ROOT / "dist" / locale / "microsoft-copilot" / "agent-project"
            env_dir = project / "env"
            self.assertTrue(env_dir.is_dir())
            emitted = sorted(path.name for path in env_dir.iterdir() if path.is_file())
            self.assertTrue(emitted, f"expected M365 environment templates for {locale}")
            self.assertTrue(
                all(name.endswith(".example") for name in emitted),
                f"public build emitted deployment environment for {locale}: {emitted}",
            )

            agent = json.loads(
                (project / "appPackage" / "declarativeAgent.json").read_text(encoding="utf-8")
            )
            sharepoint = [
                capability
                for capability in agent.get("capabilities", [])
                if isinstance(capability, dict)
                and capability.get("name") == "OneDriveAndSharePoint"
                and capability.get("items_by_url")
            ]
            self.assertEqual(
                sharepoint,
                [],
                f"canonical public build must not contain a tenant SharePoint URL for {locale}",
            )

    def test_m365_validation_workflow_stages_env_only_after_build(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "m365-package.yml").read_text(encoding="utf-8")
        self.assertIn("CSW_M365_SHAREPOINT_SITE_URL", workflow)
        self.assertIn("scripts/stage_m365_env.py", workflow)
        self.assertLess(workflow.index("python scripts/build.py"), workflow.index("scripts/stage_m365_env.py"))

        release = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertNotIn("CSW_M365_SHAREPOINT_SITE_URL", release)
        self.assertNotIn("stage_m365_env.py", release)

    def test_stage_environment_copies_only_when_source_and_project_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "adapters" / "microsoft-copilot" / "ja-JP" / "env" / ".env.dev"
            project = root / "dist" / "ja-JP" / "microsoft-copilot" / "agent-project"
            source.parent.mkdir(parents=True)
            project.mkdir(parents=True)
            source.write_text("TOKEN=deployment-only\n", encoding="utf-8")

            original_root = STAGE.ROOT
            STAGE.ROOT = root
            try:
                target = STAGE.stage_environment("ja-JP", "dev")
            finally:
                STAGE.ROOT = original_root

            self.assertEqual(
                target.read_text(encoding="utf-8"),
                "TOKEN=deployment-only\n",
            )
            self.assertEqual(
                target,
                project / "env" / ".env.dev",
            )

    def test_stage_environment_fails_when_source_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "dist" / "en-US" / "microsoft-copilot" / "agent-project"
            project.mkdir(parents=True)

            original_root = STAGE.ROOT
            STAGE.ROOT = root
            try:
                with self.assertRaisesRegex(FileNotFoundError, "init_m365_env.py"):
                    STAGE.stage_environment("en-US", "dev")
            finally:
                STAGE.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
