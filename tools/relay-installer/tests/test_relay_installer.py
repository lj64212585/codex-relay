from __future__ import annotations

import json
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from relay_installer import (
    ConfigError,
    ConflictError,
    RelayInstallerService,
    UnsafeCollisionError,
    _run_desktop_window,
    app_version,
    load_installer_config,
    main,
)


class RelayInstallerServiceTests(unittest.TestCase):
    def test_repository_catalog_has_implementation_instead_of_pair(self) -> None:
        installer_root = Path(__file__).resolve().parents[1]
        config = load_installer_config(installer_root / "relay-installer.config.json")
        self.assertEqual(
            ["explore-relay", "implementation-relay", "budget-relay"],
            [relay.relay_id for relay in config.relays],
        )
        implementation = config.relay_by_id("implementation-relay")
        self.assertEqual(9, len(implementation.agent_files))
        service = RelayInstallerService(config)
        self.assertEqual(3, len(service.bootstrap()["relays"]))
        self.assertFalse((config.source_root / "plan-execute-relay").exists())

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
            "sourcePath": relay_id,
            "skill": {
                "source": "skill",
                "target": f".codex/skills/{relay_id}",
            },
            "agents": {
                "source": "agents",
                "target": ".codex/agents",
                "files": agent_files,
            },
        }

    def _service(self, relay_entries: list[dict[str, object]], retired: list[dict[str, object]] | None = None) -> RelayInstallerService:
        config_path = self.root / "installer.json"
        config_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "sourceRoot": "packages",
                    "relays": relay_entries,
                    "retiredRelays": retired or [],
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
            (self.home_root / ".codex/skills/alpha-relay/SKILL.md").is_file()
        )
        self.assertTrue(
            (self.home_root / ".codex/agents/alpha.toml").is_file()
        )

    def _legacy_install(self) -> dict[str, object]:
        files = {
            ".agents/skills/legacy-relay/SKILL.md": "---\nname: legacy-relay\n---\nOld rules\n",
            ".codex/agents/legacy.toml": 'name = "legacy"\n',
        }
        for relative, content in files.items():
            path = self.project_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.replace("\n", "\r\n").encode())
        return {
            "id": "legacy-relay", "name": "Legacy Relay",
            "skillTarget": ".agents/skills/legacy-relay",
            "files": {p: hashlib.sha256(s.encode()).hexdigest() for p, s in files.items()},
        }

    def test_legacy_switch_requires_confirmation_and_backs_up(self) -> None:
        legacy = self._legacy_install()
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha], [legacy])
        args = dict(scope="project", project_path=str(self.project_root), relay_id="alpha-relay")
        inspection = service.inspect(**args)
        self.assertEqual("retired", inspection["conflicts"][0]["status"])
        self.assertTrue(inspection["canInstall"])
        with self.assertRaises(ConflictError):
            service.install(**args, remove_conflicts=False)
        result = service.install(**args, remove_conflicts=True)
        self.assertFalse((self.project_root / legacy["skillTarget"]).exists())
        self.assertFalse((self.project_root / ".codex/agents/legacy.toml").exists())
        self.assertTrue((Path(result["backupPath"]) / "manifest.json").is_file())
        self.assertEqual("legacy-relay", result["removedRelays"][0]["id"])

    def test_legacy_custom_file_blocks_switch_and_removal(self) -> None:
        legacy = self._legacy_install()
        extra = self.project_root / legacy["skillTarget"] / "custom.md"
        extra.write_text("user notes", encoding="utf-8")
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha], [legacy])
        args = dict(scope="project", project_path=str(self.project_root), relay_id="alpha-relay")
        self.assertFalse(service.inspect(**args)["canInstall"])
        with self.assertRaises(UnsafeCollisionError):
            service.install(**args, remove_conflicts=True)
        with self.assertRaises(UnsafeCollisionError):
            service.inspect_removal(scope="project", project_path=str(self.project_root))
        self.assertEqual("user notes", extra.read_text(encoding="utf-8"))

    def test_legacy_modified_agent_is_not_overwritten(self) -> None:
        legacy = self._legacy_install()
        target = self.project_root / ".codex/agents/legacy.toml"
        target.write_text("custom model", encoding="utf-8")
        alpha = self._create_relay("alpha-relay", ["legacy.toml"], "alpha")
        service = self._service([alpha], [legacy])
        with self.assertRaises(UnsafeCollisionError):
            service.install(scope="project", project_path=str(self.project_root), relay_id="alpha-relay", remove_conflicts=True)
        self.assertEqual("custom model", target.read_text(encoding="utf-8"))

    def test_legacy_switch_failure_restores_old_files(self) -> None:
        legacy = self._legacy_install()
        before = {p: (self.project_root / p).read_bytes() for p in legacy["files"]}
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha], [legacy])
        with patch.object(service, "_verify_installed", side_effect=RuntimeError("verify failed")):
            with self.assertRaises(RuntimeError):
                service.install(scope="project", project_path=str(self.project_root), relay_id="alpha-relay", remove_conflicts=True)
        for path, content in before.items():
            self.assertEqual(content, (self.project_root / path).read_bytes())
        self.assertFalse((self.project_root / ".codex/skills/alpha-relay").exists())

    def test_legacy_paths_cannot_escape_install_surface(self) -> None:
        legacy = self._legacy_install()
        legacy["files"] = {"../outside.txt": "a" * 64}
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        with self.assertRaises(ConfigError):
            self._service([alpha], [legacy])

    def test_same_name_old_skill_path_migrates_once_and_preserves_other_skills(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        old = self.project_root / ".agents/skills/alpha-relay"
        old.mkdir(parents=True)
        content = (self.source_root / "alpha-relay/skill/SKILL.md").read_bytes()
        (old / "SKILL.md").write_bytes(content)
        custom = self.project_root / ".agents/skills/custom/SKILL.md"
        custom.parent.mkdir(parents=True)
        custom.write_text("other AI skill", encoding="utf-8")
        legacy = {
            "id": "alpha-relay-agents-path", "name": "Alpha old path",
            "skillTarget": ".agents/skills/alpha-relay",
            "files": {".agents/skills/alpha-relay/SKILL.md": hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()},
        }
        service = self._service([alpha], [legacy])
        args = dict(scope="project", project_path=str(self.project_root), relay_id="alpha-relay")
        with self.assertRaises(ConflictError):
            service.install(**args, remove_conflicts=False)
        result = service.install(**args, remove_conflicts=True)
        self.assertFalse(old.exists())
        self.assertEqual(content, (self.project_root / ".codex/skills/alpha-relay/SKILL.md").read_bytes())
        self.assertEqual(content, (Path(result["backupPath"]) / ".agents/skills/alpha-relay/SKILL.md").read_bytes())
        self.assertEqual("other AI skill", custom.read_text(encoding="utf-8"))
        self.assertEqual([], service.inspect(**args)["conflicts"])

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

    def test_bootstrap_needs_no_estimated_metrics(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        public_relay = self._service([alpha]).bootstrap()["relays"][0]
        self.assertNotIn("metrics", public_relay)
        self.assertEqual("alpha-relay test relay", public_relay["description"])

    def test_exposes_application_version_in_bootstrap(self) -> None:
        alpha = self._create_relay("alpha-relay", ["alpha.toml"], "alpha")
        service = self._service([alpha])

        self.assertEqual(app_version(), service.bootstrap()["appVersion"])

    def test_writes_version_report_without_loading_config(self) -> None:
        report_path = self.root / "version.txt"

        result = main(["--write-version", str(report_path)])

        self.assertEqual(0, result)
        self.assertEqual(
            app_version(),
            report_path.read_text(encoding="utf-8").strip(),
        )

    def test_desktop_window_uses_edge_webview_and_stops_server(self) -> None:
        calls: dict[str, object] = {}

        class FakeServer:
            def serve_forever(self, *, poll_interval: float) -> None:
                calls["pollInterval"] = poll_interval

            def shutdown(self) -> None:
                calls["shutdown"] = True

            def server_close(self) -> None:
                calls["serverClose"] = True

        def create_window(title: str, url: str, **options: object) -> None:
            calls["title"] = title
            calls["url"] = url
            calls["windowOptions"] = options

        def start(**options: object) -> None:
            calls["startOptions"] = options

        fake_webview = SimpleNamespace(
            create_window=create_window,
            start=start,
        )
        storage_root = self.root / "local-app-data"
        with (
            patch.dict(sys.modules, {"webview": fake_webview}),
            patch.dict(os.environ, {"LOCALAPPDATA": str(storage_root)}),
        ):
            result = _run_desktop_window(
                FakeServer(),  # type: ignore[arg-type]
                "http://127.0.0.1:43123/",
                verbose=False,
            )

        self.assertEqual(0, result)
        self.assertEqual("http://127.0.0.1:43123/", calls["url"])
        self.assertEqual("edgechromium", calls["startOptions"]["gui"])
        self.assertFalse(calls["startOptions"]["private_mode"])
        self.assertTrue(calls["shutdown"])
        self.assertTrue(calls["serverClose"])

    def test_web_ui_defaults_to_english(self) -> None:
        installer_root = Path(__file__).resolve().parents[1]
        app_script = (installer_root / "web/app.js").read_text(encoding="utf-8")
        index_html = (installer_root / "web/index.html").read_text(
            encoding="utf-8"
        )

        self.assertIn('locale: "en"', app_script)
        self.assertIn('applyLanguage(stored || "en", false)', app_script)
        self.assertNotIn("navigator.language.toLowerCase()", app_script)
        self.assertIn('<html lang="en">', index_html)
        self.assertIn(
            'class="language-option is-active"\n'
            '              type="button"\n'
            '              data-locale="en"\n'
            '              aria-pressed="true"',
            index_html,
        )

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
            (self.project_root / ".codex/skills/alpha-relay/SKILL.md").is_file()
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
        custom_skill = self.project_root / ".codex/skills/custom/SKILL.md"
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
            (self.project_root / ".codex/skills/alpha-relay").exists()
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
            (backup_root / ".codex/skills/alpha-relay/SKILL.md").is_file()
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
            (self.project_root / ".codex/skills/alpha-relay").exists()
        )
        self.assertTrue(
            (self.project_root / ".codex/skills/beta-relay/SKILL.md").is_file()
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
