from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from relay_installer import (
    ConfigError,
    ConflictError,
    RelayInstallerService,
    UnsafeCollisionError,
    load_installer_config,
)


class RelayInstallerServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_directory.name)
        self.source_root = self.root / "packages"
        self.source_root.mkdir()
        self.project_root = self.root / "project"
        self.project_root.mkdir()
        self.home_root = self.root / "home"
        self.home_root.mkdir()

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def _create_relay(
        self,
        relay_id: str,
        agent_files: list[str],
        marker: str,
    ) -> dict[str, object]:
        package = self.source_root / relay_id
        skill = package / "skill"
        agents = package / "agents"
        skill.mkdir(parents=True)
        agents.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {relay_id}\n---\n\n{marker}\n",
            encoding="utf-8",
        )
        for file_name in agent_files:
            (agents / file_name).write_text(
                f'name = "{marker}"\n',
                encoding="utf-8",
            )
        return {
            "id": relay_id,
            "name": relay_id.title(),
            "badge": f"{len(agent_files)} roles",
            "description": f"{relay_id} test relay",
            "metrics": {
                "taskPerfectionPercent": 105,
                "implementationCostPercent": 75,
            },
            "sourcePath": relay_id,
            "skill": {
                "source": "skill",
                "target": f".agents/skills/{relay_id}",
            },
            "agents": {
                "source": "agents",
                "target": ".codex/agents",
                "files": agent_files,
            },
        }

    def _service(self, relay_entries: list[dict[str, object]]) -> RelayInstallerService:
        config_path = self.root / "installer.json"
        config_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "sourceRoot": "packages",
                    "relays": relay_entries,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        config = load_installer_config(config_path)
        return RelayInstallerService(
            config,
            home_root=self.home_root,
            default_project_root=self.project_root,
        )

    def test_installs_relay_into_current_user_global_root(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])

        result = service.install(
            scope="global",
            project_path=None,
            relay_id="alpha-relay",
            remove_conflicts=False,
        )

        self.assertEqual(str(self.home_root), result["targetRoot"])
        self.assertTrue(
            (self.home_root / ".agents/skills/alpha-relay/SKILL.md").is_file()
        )
        self.assertTrue(
            (self.home_root / ".codex/agents/alpha.toml").is_file()
        )

    def test_exposes_optional_relay_translations_in_bootstrap(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        alpha["translations"] = {
            "en": {
                "name": "Alpha Relay",
                "badge": "One role",
                "description": "An English relay description.",
            }
        }
        service = self._service([alpha])

        public_relay = service.bootstrap()["relays"][0]

        self.assertEqual(
            "An English relay description.",
            public_relay["translations"]["en"]["description"],
        )

    def test_exposes_relay_metrics_in_bootstrap(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])

        public_relay = service.bootstrap()["relays"][0]

        self.assertEqual(
            {
                "taskPerfectionPercent": 105,
                "implementationCostPercent": 75,
            },
            public_relay["metrics"],
        )

    def test_rejects_invalid_relay_metric(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        alpha["metrics"]["taskPerfectionPercent"] = -1

        with self.assertRaises(ConfigError):
            self._service([alpha])

    def test_rejects_incomplete_relay_translation(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        alpha["translations"] = {
            "en": {
                "name": "Alpha Relay",
                "badge": "One role",
            }
        }

        with self.assertRaises(ConfigError):
            self._service([alpha])

    def test_reads_localized_readme_and_embeds_local_image(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        package = self.source_root / "alpha-relay"
        assets = package / "assets"
        assets.mkdir()
        (assets / "hero.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
            encoding="utf-8",
        )
        (package / "README.md").write_text(
            '# Alpha\n\n<img src="./assets/hero.svg" alt="Alpha">\n',
            encoding="utf-8",
        )
        (package / "README.en.md").write_text(
            "# Alpha Relay\n\nEnglish documentation.\n",
            encoding="utf-8",
        )
        alpha["readmes"] = {
            "zh-CN": "README.md",
            "en": "README.en.md",
        }
        service = self._service([alpha])

        readme = service.read_readme("alpha-relay", "zh-CN")

        self.assertEqual("README.md", readme["fileName"])
        self.assertIn("# Alpha", readme["content"])
        self.assertTrue(
            readme["assets"]["./assets/hero.svg"].startswith(
                "data:image/svg+xml;base64,"
            )
        )
        self.assertEqual(
            ["en", "zh-CN"],
            service.bootstrap()["relays"][0]["readmeLocales"],
        )

    def test_rejects_readme_path_traversal_in_config(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        alpha["readmes"] = {"zh-CN": "../README.md"}

        with self.assertRaises(ConfigError):
            self._service([alpha])

    def test_installs_relay_into_project_targets(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])

        result = service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )

        self.assertTrue(result["ok"])
        self.assertTrue(
            (self.project_root / ".agents/skills/alpha-relay/SKILL.md").is_file()
        )
        self.assertEqual(
            'name = "alpha"\n',
            (self.project_root / ".codex/agents/alpha.toml").read_text(
                encoding="utf-8"
            ),
        )
        self.assertIsNone(result["backupPath"])

    def test_inspects_and_removes_managed_relays_with_backup(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])
        service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )
        custom_skill = self.project_root / ".agents/skills/custom/SKILL.md"
        custom_skill.parent.mkdir(parents=True)
        custom_skill.write_text("custom skill\n", encoding="utf-8")
        custom_agent = self.project_root / ".codex/agents/custom.toml"
        custom_agent.write_text('name = "custom"\n', encoding="utf-8")

        inspection = service.inspect_removal(
            scope="project",
            project_path=str(self.project_root),
        )

        self.assertTrue(inspection["canRemove"])
        self.assertEqual(
            ["alpha-relay"],
            [item["id"] for item in inspection["installations"]],
        )

        result = service.remove_relays(
            scope="project",
            project_path=str(self.project_root),
        )

        self.assertFalse(
            (self.project_root / ".agents/skills/alpha-relay").exists()
        )
        self.assertFalse(
            (self.project_root / ".codex/agents/alpha.toml").exists()
        )
        self.assertEqual("custom skill\n", custom_skill.read_text(encoding="utf-8"))
        self.assertEqual(
            'name = "custom"\n',
            custom_agent.read_text(encoding="utf-8"),
        )
        backup_root = Path(result["backupPath"])
        manifest = json.loads(
            (backup_root / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("remove", manifest["operation"])
        self.assertEqual(["alpha-relay"], manifest["removedRelays"])
        self.assertTrue(
            (backup_root / ".agents/skills/alpha-relay/SKILL.md").is_file()
        )

    def test_remove_relays_is_a_no_op_when_no_known_relay_exists(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])

        inspection = service.inspect_removal(
            scope="project",
            project_path=str(self.project_root),
        )
        result = service.remove_relays(
            scope="project",
            project_path=str(self.project_root),
        )

        self.assertFalse(inspection["canRemove"])
        self.assertEqual([], inspection["installations"])
        self.assertEqual([], result["removedRelays"])
        self.assertIsNone(result["backupPath"])

    def test_requires_confirmation_then_removes_other_relay(self) -> None:
        alpha = self._create_relay("alpha-relay", ["worker.toml"], "alpha")
        beta = self._create_relay("beta-relay", ["worker.toml"], "beta")
        service = self._service([alpha, beta])
        service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )

        inspection = service.inspect(
            scope="project",
            project_path=str(self.project_root),
            relay_id="beta-relay",
        )
        self.assertTrue(inspection["requiresConfirmation"])
        self.assertEqual(["alpha-relay"], [item["id"] for item in inspection["conflicts"]])

        with self.assertRaises(ConflictError):
            service.install(
                scope="project",
                project_path=str(self.project_root),
                relay_id="beta-relay",
                remove_conflicts=False,
            )

        result = service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="beta-relay",
            remove_conflicts=True,
        )
        self.assertFalse(
            (self.project_root / ".agents/skills/alpha-relay").exists()
        )
        self.assertTrue(
            (self.project_root / ".agents/skills/beta-relay/SKILL.md").is_file()
        )
        self.assertEqual(
            'name = "beta"\n',
            (self.project_root / ".codex/agents/worker.toml").read_text(
                encoding="utf-8"
            ),
        )
        self.assertTrue(Path(result["backupPath"]).is_dir())
        self.assertTrue(
            (Path(result["backupPath"]) / "manifest.json").is_file()
        )

    def test_other_relay_conflicts_even_without_shared_agent_names(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        gamma = self._create_relay("gamma-relay", ["gamma.toml"], "gamma")
        service = self._service([alpha, gamma])
        service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )

        inspection = service.inspect(
            scope="project",
            project_path=str(self.project_root),
            relay_id="gamma-relay",
        )

        self.assertEqual(1, len(inspection["conflicts"]))
        self.assertEqual("alpha-relay", inspection["conflicts"][0]["id"])

    def test_refuses_unmanaged_same_named_agent_file(self) -> None:
        alpha = self._create_relay("alpha-relay", ["worker.toml"], "alpha")
        service = self._service([alpha])
        collision = self.project_root / ".codex/agents/worker.toml"
        collision.parent.mkdir(parents=True)
        collision.write_text('name = "custom"\n', encoding="utf-8")

        inspection = service.inspect(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
        )

        self.assertFalse(inspection["canInstall"])
        self.assertEqual([str(collision)], inspection["unmanagedCollisions"])
        with self.assertRaises(UnsafeCollisionError):
            service.install(
                scope="project",
                project_path=str(self.project_root),
                relay_id="alpha-relay",
                remove_conflicts=True,
            )
        self.assertEqual(
            'name = "custom"\n',
            collision.read_text(encoding="utf-8"),
        )

    def test_same_relay_update_creates_recoverable_backup(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha-v1")
        service = self._service([alpha])
        service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )
        (self.source_root / "alpha-relay/agents/alpha.toml").write_text(
            'name = "alpha-v2"\n',
            encoding="utf-8",
        )

        result = service.install(
            scope="project",
            project_path=str(self.project_root),
            relay_id="alpha-relay",
            remove_conflicts=False,
        )

        self.assertEqual(
            'name = "alpha-v2"\n',
            (self.project_root / ".codex/agents/alpha.toml").read_text(
                encoding="utf-8"
            ),
        )
        backup_root = Path(result["backupPath"])
        self.assertEqual(
            'name = "alpha-v1"\n',
            (backup_root / ".codex/agents/alpha.toml").read_text(
                encoding="utf-8"
            ),
        )

    def test_rejects_target_path_traversal_in_config(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        alpha["skill"]["target"] = "../outside"
        config_path = self.root / "unsafe.json"
        config_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "sourceRoot": "packages",
                    "relays": [alpha],
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ConfigError):
            load_installer_config(config_path)


if __name__ == "__main__":
    unittest.main()
