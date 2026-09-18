from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build as build_module  # noqa: E402


class OpenAIBuildAdapterParityTests(unittest.TestCase):
    def test_openai_adapter_metadata_is_copied_verbatim(self) -> None:
        config = json.loads((ROOT / "src/manifest.json").read_text(encoding="utf-8"))

        for locale in ("ja-JP", "en-US"):
            router = (
                ROOT / "src" / locale / config["router"]
            ).read_text(encoding="utf-8")

            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as tmp:
                generated_dist = Path(tmp) / "dist"
                with patch.object(build_module, "DIST", generated_dist):
                    build_module.build_openai(locale, config, router)

                for profile in ("interactive", "metered"):
                    with self.subTest(locale=locale, profile=profile):
                        source = (
                            ROOT
                            / "adapters"
                            / "openai-skill"
                            / locale
                            / f"openai.{profile}.yaml"
                        )
                        generated = (
                            generated_dist
                            / locale
                            / "openai-skill"
                            / profile
                            / config["name"]
                            / "agents"
                            / "openai.yaml"
                        )
                        self.assertTrue(generated.is_file())
                        self.assertEqual(source.read_bytes(), generated.read_bytes())


if __name__ == "__main__":
    unittest.main()
