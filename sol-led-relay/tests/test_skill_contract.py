from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "sol-led-relay"


class SolLedRelaySkillContractTests(unittest.TestCase):
    def test_skill_and_references(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("\nname: sol-led-relay\n", skill)
        self.assertIn("Use implicitly", skill)
        self.assertLessEqual(len(skill.encode("utf-8")), 18_000)
        self.assertLessEqual(len(skill.splitlines()), 220)
        for relative in ("contracts.md", "routing.md", "evaluation.md"):
            self.assertTrue((SKILL_DIR / "references" / relative).is_file())

    def test_implicit_policy_and_runtime_gate(self) -> None:
        metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("$sol-led-relay", metadata)

        ordinary = (ROOT / "agents" / "runtime_investigator.toml").read_text(encoding="utf-8")
        deep = (ROOT / "agents" / "runtime_investigator_deep.toml").read_text(encoding="utf-8")
        self.assertIn("one investigation pass", ordinary)
        self.assertIn("return INCONCLUSIVE directly to the parent", ordinary)
        self.assertIn("not a fallback", deep)

    def test_liveness_checkpoint_and_interruption_contract(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        contracts = (SKILL_DIR / "references" / "contracts.md").read_text(encoding="utf-8")
        evaluation = (SKILL_DIR / "references" / "evaluation.md").read_text(encoding="utf-8")
        bounded = (ROOT / "agents" / "bounded_executor.toml").read_text(encoding="utf-8")

        self.assertIn("A wait timeout is only a polling observation", skill)
        self.assertIn("Do not call `interrupt_agent` merely because", skill)
        self.assertIn("keep the child intact", skill)
        self.assertIn("record the partial-result audit", skill)
        self.assertIn("Silence never authorizes retry, takeover, or interruption by itself", skill)
        self.assertIn("never authorizes automatic retry", skill)
        self.assertIn("only when no child remains running", skill)
        self.assertIn("## Checkpoint request", contracts)
        self.assertIn("No file change does not mean no usable result", contracts)
        self.assertIn("allowed cancellation reason defined by the Skill", contracts)
        self.assertIn("## Liveness and interruption regressions", evaluation)
        self.assertIn("partial-result audit", evaluation)
        self.assertIn("keep the child intact", evaluation)
        self.assertIn("do not interrupt, retry, or take over merely because it is silent", evaluation)
        self.assertIn("A manually interrupted child is never retried automatically", evaluation)
        self.assertIn("open-ended discovery", bounded)
        self.assertIn("parent requests a checkpoint", bounded)
        self.assertIn("Continue afterward unless the parent records an allowed cancellation reason", bounded)

if __name__ == "__main__":
    unittest.main()
