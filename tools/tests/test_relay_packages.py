"""Exercise package validation on disposable source and installed layouts."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ("explore-relay", "implementation-relay")


class RelayPackageValidationTests(unittest.TestCase):
    def fixture(self, root: Path, package: str, installed: bool = False):
        source = ROOT / "relay" / package
        target = root / package
        skill = target / (".codex/skills" if installed else "skills") / package
        agents = target / (".codex/agents" if installed else "agents")
        shutil.copytree(source / "skills" / package, skill)
        shutil.copytree(source / "agents", agents)
        validator = skill / "scripts" / f"validate_{package.replace('-', '_')}.py"
        return skill, agents, validator

    def validate(self, validator: Path, valid: bool, message: str = ""):
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(validator)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode == 0, valid, output)
        if message:
            self.assertIn(message, output)

    def test_source_and_project_installation(self):
        for package in PACKAGES:
            for installed in (False, True):
                with self.subTest(package=package, installed=installed), tempfile.TemporaryDirectory() as temp:
                    _, agents, validator = self.fixture(Path(temp), package, installed)
                    if installed:
                        # Unrelated project roles are allowed alongside installed profiles.
                        (agents / "project_custom.toml").write_text('name = "project_custom"\n', encoding="utf-8")
                    self.validate(validator, True, "does not prove behavior")

    def test_invalid_profile_configuration_is_rejected(self):
        mutations = (
            ('model = "gpt-5.6-luna"', 'model = "unknown-model"', "unexpected model"),
            ('model_reasoning_effort = "max"', 'model_reasoning_effort = "none"', "effort must be max"),
            ('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"', "unexpected sandbox"),
        )
        for package in PACKAGES:
            filename = "explore_code.toml" if package == "explore-relay" else "code_explorer.toml"
            for old, new, message in mutations:
                with self.subTest(package=package, mutation=message), tempfile.TemporaryDirectory() as temp:
                    _, agents, validator = self.fixture(Path(temp), package)
                    profile = agents / filename
                    text = profile.read_text(encoding="utf-8")
                    self.assertIn(old, text)
                    profile.write_text(text.replace(old, new), encoding="utf-8")
                    self.validate(validator, False, message)

    def test_missing_profile_and_reference_are_rejected(self):
        for package in PACKAGES:
            for missing in ("profile", "reference"):
                with self.subTest(package=package, missing=missing), tempfile.TemporaryDirectory() as temp:
                    skill, agents, validator = self.fixture(Path(temp), package)
                    target = next(agents.glob("*.toml")) if missing == "profile" else skill / "references/contracts.md"
                    target.unlink()
                    self.validate(validator, False)

    def test_broken_nested_link_is_rejected(self):
        for package in PACKAGES:
            with self.subTest(package=package), tempfile.TemporaryDirectory() as temp:
                skill, _, validator = self.fixture(Path(temp), package)
                reference = skill / "references/contracts.md"
                with reference.open("a", encoding="utf-8") as handle:
                    handle.write("\n[Missing supporting contract](missing.md)\n")
                self.validate(validator, False, "broken local reference")

    def test_unknown_route_is_rejected(self):
        for package in PACKAGES:
            with self.subTest(package=package), tempfile.TemporaryDirectory() as temp:
                skill, _, validator = self.fixture(Path(temp), package)
                entry = skill / "SKILL.md"
                role = "explore_code" if package == "explore-relay" else "code_explorer"
                entry.write_text(entry.read_text(encoding="utf-8").replace(f"`{role}`", "`missing_role`"), encoding="utf-8")
                self.validate(validator, False, "route table")

    def test_missing_required_reference_link_is_rejected(self):
        for package in PACKAGES:
            with self.subTest(package=package), tempfile.TemporaryDirectory() as temp:
                skill, _, validator = self.fixture(Path(temp), package)
                entry = skill / "SKILL.md"
                text = entry.read_text(encoding="utf-8")
                entry.write_text(text.replace("[routing.md](references/routing.md)", "routing guidance"), encoding="utf-8")
                self.validate(validator, False, "required references must be linked")


if __name__ == "__main__":
    unittest.main()
