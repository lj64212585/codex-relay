from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents"

EXPECTED = {
    "code_explorer.toml": ("code_explorer", "gpt-5.6-luna", "read-only"),
    "docs_researcher.toml": ("docs_researcher", "gpt-5.6-luna", "read-only"),
    "runtime_investigator.toml": ("runtime_investigator", "gpt-5.6-luna", "read-only"),
    "runtime_investigator_deep.toml": ("runtime_investigator_deep", "gpt-5.6-terra", "read-only"),
    "mechanical_executor.toml": ("mechanical_executor", "gpt-5.6-luna", "workspace-write"),
    "minimal_fixer.toml": ("minimal_fixer", "gpt-5.6-luna", "workspace-write"),
    "bounded_executor.toml": ("bounded_executor", "gpt-5.6-luna", "workspace-write"),
    "code_reviewer.toml": ("code_reviewer", "gpt-5.6-terra", "read-only"),
    "verification_reviewer.toml": ("verification_reviewer", "gpt-5.6-terra", "read-only"),
}


class SolLedRelayAgentProfileTests(unittest.TestCase):
    def test_exact_profile_set(self) -> None:
        actual = {path.name for path in AGENT_DIR.glob("*.toml")}
        self.assertEqual(set(EXPECTED), actual)
        self.assertNotIn("default.toml", actual)

    def test_models_effort_sandbox_and_boundaries(self) -> None:
        seen_names: set[str] = set()
        for filename, expected in EXPECTED.items():
            with (AGENT_DIR / filename).open("rb") as handle:
                data = tomllib.load(handle)
            expected_name, expected_model, expected_sandbox = expected
            self.assertEqual(expected_name, data["name"])
            self.assertEqual(expected_model, data["model"])
            self.assertEqual("max", data["model_reasoning_effort"])
            self.assertEqual(expected_sandbox, data["sandbox_mode"])
            self.assertIn("Do not spawn subagents", data["developer_instructions"])
            self.assertIn("Do not commit, push", data["developer_instructions"])
            self.assertNotIn(data["name"], seen_names)
            seen_names.add(data["name"])


if __name__ == "__main__":
    unittest.main()
