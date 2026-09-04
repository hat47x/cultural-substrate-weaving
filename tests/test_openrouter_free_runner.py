import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "research" / "empty-self-boundary-cases" / "run_openrouter_free.py"


class OpenRouterFreeRunnerTests(unittest.TestCase):
    def run_dry(self, model: str, payload: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            request_path = Path(tmp) / "request.json"
            request_path.write_text(json.dumps(payload), encoding="utf-8")
            env = dict(os.environ)
            env.pop("OPENROUTER_API_KEY", None)
            return subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--model",
                    model,
                    "--request",
                    str(request_path),
                    "--dry-run",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_accepts_explicit_free_model_without_api_key(self):
        result = self.run_dry(
            "example/model:free",
            {"messages": [{"role": "user", "content": "test"}]},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("free-only OpenRouter request is valid", result.stdout)

    def test_accepts_openrouter_free_router(self):
        result = self.run_dry(
            "openrouter/free",
            {"messages": [{"role": "user", "content": "test"}]},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_non_free_model(self):
        result = self.run_dry(
            "example/paid-model",
            {"messages": [{"role": "user", "content": "test"}]},
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be 'openrouter/free'", result.stderr)

    def test_rejects_model_fallback_array(self):
        result = self.run_dry(
            "example/model:free",
            {
                "models": ["example/model:free", "example/other:free"],
                "messages": [{"role": "user", "content": "test"}],
            },
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("fallback arrays are disabled", result.stderr)

    def test_rejects_plugins(self):
        result = self.run_dry(
            "example/model:free",
            {
                "plugins": [{"id": "web"}],
                "messages": [{"role": "user", "content": "test"}],
            },
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("plugins are disabled", result.stderr)

    def test_rejects_model_in_request_json(self):
        result = self.run_dry(
            "example/model:free",
            {
                "model": "example/model:free",
                "messages": [{"role": "user", "content": "test"}],
            },
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("set the model with --model", result.stderr)


if __name__ == "__main__":
    unittest.main()
