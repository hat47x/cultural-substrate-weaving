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
    def run_runner(
        self,
        model: str,
        payload: dict,
        *extra_args: str,
    ) -> subprocess.CompletedProcess[str]:
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
                    *extra_args,
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

    def run_dry(self, model: str, payload: dict) -> subprocess.CompletedProcess[str]:
        return self.run_runner(model, payload, "--dry-run")

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

    def test_rejects_web_search_options(self):
        result = self.run_dry(
            "example/model:free",
            {
                "web_search_options": {"search_context_size": "low"},
                "messages": [{"role": "user", "content": "test"}],
            },
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("web search is disabled", result.stderr)

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

    def test_rejects_repository_tracked_output_before_reading_key(self):
        result = self.run_runner(
            "example/model:free",
            {"messages": [{"role": "user", "content": "test"}]},
            "--output",
            str(ROOT / "research" / "raw-response.json"),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be under .tmp/ or .living-lab/", result.stderr)
        self.assertNotIn("OPENROUTER_API_KEY is not set", result.stderr)

    def test_private_tmp_output_passes_path_guard_then_requires_key(self):
        result = self.run_runner(
            "example/model:free",
            {"messages": [{"role": "user", "content": "test"}]},
            "--output",
            str(ROOT / ".tmp" / "openrouter" / "raw-response.json"),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("OPENROUTER_API_KEY is not set", result.stderr)
        self.assertNotIn("must be under .tmp/ or .living-lab/", result.stderr)


if __name__ == "__main__":
    unittest.main()
