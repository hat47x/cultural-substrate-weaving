from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_m365_profile import validate_m365_profile  # noqa: E402


class M365LimitedProfileTests(unittest.TestCase):
    def test_generated_limited_profile_contract_is_valid(self) -> None:
        self.assertEqual(validate_m365_profile(), [])

    def test_build_uses_adapter_owned_self_contained_instructions(self) -> None:
        build = (SCRIPTS / "build.py").read_text(encoding="utf-8")

        self.assertIn('adapter_root / "instructions.md"', build)
        self.assertIn('target / "method-reference" / filename', build)
        self.assertIn('adapter_root / "package-readme.txt"', build)
        self.assertNotIn("compact_router", build)
        self.assertNotIn('ADAPTERS / "microsoft-copilot" / locale / "instructions-prefix.md"', build)

    def test_obsolete_m365_prefixes_are_removed(self) -> None:
        for locale in ("ja-JP", "en-US"):
            self.assertFalse(
                (ROOT / "adapters" / "microsoft-copilot" / locale / "instructions-prefix.md").exists()
            )
            self.assertTrue(
                (ROOT / "adapters" / "microsoft-copilot" / locale / "instructions.md").is_file()
            )

    def test_m365_profile_is_explicitly_composite_and_limited_in_both_locales(self) -> None:
        ja = (
            ROOT / "adapters/microsoft-copilot/ja-JP/instructions.md"
        ).read_text(encoding="utf-8")
        en = (
            ROOT / "adapters/microsoft-copilot/en-US/instructions.md"
        ).read_text(encoding="utf-8")

        self.assertIn("親和統合コアの最小互換手順を埋め込んでいます", ja)
        self.assertIn("This limited profile embeds a minimal compatible material-synthesis fallback", en)
        self.assertIn("完全なmulti-round orchestrationではありません", ja)
        self.assertIn("This is not complete multi-round orchestration", en)
        self.assertIn("AI解釈を混ぜない", ja)
        self.assertIn("AI interpretation", en)

        self.assertNotIn("文化的体系による構造探索とKJ法による統合の中核だけを扱います", ja)
        self.assertNotIn("It keeps the core of cultural-framework exploration and KJ integration", en)


if __name__ == "__main__":
    unittest.main()
