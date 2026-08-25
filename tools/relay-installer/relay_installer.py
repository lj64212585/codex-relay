from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import sys
import threading
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


APP_NAME = "Relay Installer"
CONFIG_NAME = "relay-installer.config.json"
MAX_REQUEST_BYTES = 1024 * 1024
MAX_README_BYTES = 512 * 1024
MAX_README_ASSET_BYTES = 2 * 1024 * 1024
RELAY_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
README_IMAGE_PATTERN = re.compile(
    r'(?:<img\b[^>]*\bsrc=["\']([^"\']+)["\']|'
    r'!\[[^\]]*\]\(([^)\s]+)(?:\s+["\'][^)]*["\'])?\))',
    re.IGNORECASE,
)
README_ASSET_TYPES = {
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}


class RelayInstallerError(Exception):
    code = "installer_error"
    status = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, *, details: Any | None = None) -> None:
        super().__init__(message)
        self.details = details


class ConfigError(RelayInstallerError):
    code = "config_error"


class ValidationError(RelayInstallerError):
    code = "validation_error"


class ConflictError(RelayInstallerError):
    code = "relay_conflict"
    status = HTTPStatus.CONFLICT


class UnsafeCollisionError(RelayInstallerError):
    code = "unmanaged_collision"
    status = HTTPStatus.CONFLICT


@dataclass(frozen=True)
class RelayDefinition:
    relay_id: str
    name: str
    badge: str
    description: str
    task_perfection_percent: int
    implementation_cost_percent: int
    translations: dict[str, dict[str, str]]
    source_dir: Path
    readme_sources: dict[str, Path]
    skill_source: Path
    skill_target: Path
    agents_source: Path
    agents_target: Path
    agent_files: tuple[str, ...]

    def public_dict(self) -> dict[str, Any]:
        return {
            "id": self.relay_id,
            "name": self.name,
            "badge": self.badge,
            "description": self.description,
            "metrics": {
                "taskPerfectionPercent": self.task_perfection_percent,
                "implementationCostPercent": self.implementation_cost_percent,
            },
            "translations": self.translations,
            "readmeLocales": sorted(self.readme_sources),
            "agentCount": len(self.agent_files),
            "targets": {
                "skill": self.skill_target.as_posix(),
                "agents": [
                    (self.agents_target / file_name).as_posix()
                    for file_name in self.agent_files
                ],
            },
        }


@dataclass(frozen=True)
class InstallerConfig:
    config_path: Path
    source_root: Path
    relays: tuple[RelayDefinition, ...]

    def relay_by_id(self, relay_id: str) -> RelayDefinition:
        for relay in self.relays:
            if relay.relay_id == relay_id:
                return relay
        raise ValidationError(f"未知的 Relay 类型：{relay_id}")


def _expand_path(raw_path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(raw_path)))


def _path_key(path: Path) -> str:
    return os.path.normcase(str(path.resolve(strict=False)))


def _resolve_under(base: Path, relative_path: str | Path, label: str) -> Path:
    raw_path = Path(relative_path)
    if raw_path.is_absolute():
        raise ConfigError(f"{label} 必须是相对路径：{raw_path}")

    base_resolved = base.resolve(strict=False)
    candidate = (base_resolved / raw_path).resolve(strict=False)
    try:
        common = Path(os.path.commonpath((str(base_resolved), str(candidate))))
    except ValueError as error:
        raise ConfigError(f"{label} 不在允许的根目录内：{raw_path}") from error

    if os.path.normcase(str(common)) != os.path.normcase(str(base_resolved)):
        raise ConfigError(f"{label} 不得跳出允许的根目录：{raw_path}")
    return candidate


def _validate_relative_target(relative_path: Path, label: str) -> None:
    if (
        relative_path.is_absolute()
        or relative_path == Path(".")
        or any(part == ".." for part in relative_path.parts)
    ):
        raise ConfigError(f"{label} 必须是安装根目录内的相对路径：{relative_path}")


def _require_string(container: dict[str, Any], key: str, label: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{label}.{key} 必须是非空字符串。")
    return value.strip()


def _require_dict(container: dict[str, Any], key: str, label: str) -> dict[str, Any]:
    value = container.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"{label}.{key} 必须是对象。")
    return value


def _require_percentage(
    container: dict[str, Any],
    key: str,
    label: str,
) -> int:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ConfigError(
            f"{label}.{key} 必须是非负整数；相对估值允许高于 100。"
        )
    return value


def _load_translations(
    relay_payload: dict[str, Any],
    label: str,
) -> dict[str, dict[str, str]]:
    raw_translations = relay_payload.get("translations", {})
    if not isinstance(raw_translations, dict):
        raise ConfigError(f"{label}.translations 必须是对象。")

    translations: dict[str, dict[str, str]] = {}
    for locale, raw_translation in raw_translations.items():
        if not isinstance(locale, str) or not locale.strip():
            raise ConfigError(f"{label}.translations 的语言键无效。")
        if not isinstance(raw_translation, dict):
            raise ConfigError(
                f"{label}.translations.{locale} 必须是对象。"
            )
        translations[locale] = {
            field: _require_string(
                raw_translation,
                field,
                f"{label}.translations.{locale}",
            )
            for field in ("name", "badge", "description")
        }
    return translations


def _load_readmes(
    relay_payload: dict[str, Any],
    source_dir: Path,
    label: str,
) -> dict[str, Path]:
    raw_readmes = relay_payload.get("readmes", {})
    if not isinstance(raw_readmes, dict):
        raise ConfigError(f"{label}.readmes 必须是对象。")

    readmes: dict[str, Path] = {}
    normalized_locales: set[str] = set()
    for locale, raw_path in raw_readmes.items():
        if not isinstance(locale, str) or not locale.strip():
            raise ConfigError(f"{label}.readmes 的语言键无效。")
        normalized_locale = locale.strip()
        locale_key = normalized_locale.casefold()
        if locale_key in normalized_locales:
            raise ConfigError(f"{label}.readmes 包含重复语言：{normalized_locale}")
        normalized_locales.add(locale_key)
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ConfigError(
                f"{label}.readmes.{normalized_locale} 必须是非空字符串。"
            )
        readmes[normalized_locale] = _resolve_under(
            source_dir,
            raw_path.strip(),
            f"{label}.readmes.{normalized_locale}",
        )
    return readmes


def load_installer_config(config_path: Path) -> InstallerConfig:
    resolved_config = config_path.expanduser().resolve(strict=False)
    if not resolved_config.is_file():
        raise ConfigError(f"找不到配置文件：{resolved_config}")

    try:
        payload = json.loads(resolved_config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ConfigError(f"无法读取配置文件：{error}") from error

    if not isinstance(payload, dict) or payload.get("schemaVersion") != 1:
        raise ConfigError("配置文件 schemaVersion 必须为 1。")

    raw_source_root = _require_string(payload, "sourceRoot", "config")
    expanded_source_root = _expand_path(raw_source_root)
    if not expanded_source_root.is_absolute():
        expanded_source_root = resolved_config.parent / expanded_source_root
    source_root = expanded_source_root.resolve(strict=False)
    if not source_root.is_dir():
        raise ConfigError(f"Relay 源根目录不存在：{source_root}")

    raw_relays = payload.get("relays")
    if not isinstance(raw_relays, list) or not raw_relays:
        raise ConfigError("配置文件 relays 必须是非空数组。")

    relays: list[RelayDefinition] = []
    relay_ids: set[str] = set()
    for index, raw_relay in enumerate(raw_relays):
        label = f"relays[{index}]"
        if not isinstance(raw_relay, dict):
            raise ConfigError(f"{label} 必须是对象。")

        relay_id = _require_string(raw_relay, "id", label)
        if not RELAY_ID_PATTERN.fullmatch(relay_id):
            raise ConfigError(f"{label}.id 只能包含小写字母、数字与连字符。")
        if relay_id in relay_ids:
            raise ConfigError(f"Relay id 重复：{relay_id}")
        relay_ids.add(relay_id)

        source_path = _require_string(raw_relay, "sourcePath", label)
        source_dir = _resolve_under(source_root, source_path, f"{label}.sourcePath")
        metrics = _require_dict(raw_relay, "metrics", label)
        skill = _require_dict(raw_relay, "skill", label)
        agents = _require_dict(raw_relay, "agents", label)

        skill_source = _resolve_under(
            source_dir,
            _require_string(skill, "source", f"{label}.skill"),
            f"{label}.skill.source",
        )
        agents_source = _resolve_under(
            source_dir,
            _require_string(agents, "source", f"{label}.agents"),
            f"{label}.agents.source",
        )

        skill_target = Path(_require_string(skill, "target", f"{label}.skill"))
        agents_target = Path(_require_string(agents, "target", f"{label}.agents"))
        _validate_relative_target(skill_target, f"{label}.skill.target")
        _validate_relative_target(agents_target, f"{label}.agents.target")

        raw_agent_files = agents.get("files")
        if not isinstance(raw_agent_files, list) or not raw_agent_files:
            raise ConfigError(f"{label}.agents.files 必须是非空数组。")
        agent_files: list[str] = []
        for raw_file in raw_agent_files:
            if (
                not isinstance(raw_file, str)
                or not raw_file.strip()
                or Path(raw_file).name != raw_file
            ):
                raise ConfigError(
                    f"{label}.agents.files 只能包含不带目录的文件名。"
                )
            agent_files.append(raw_file)
        if len(agent_files) != len(set(agent_files)):
            raise ConfigError(f"{label}.agents.files 包含重复文件名。")

        relay = RelayDefinition(
            relay_id=relay_id,
            name=_require_string(raw_relay, "name", label),
            badge=_require_string(raw_relay, "badge", label),
            description=_require_string(raw_relay, "description", label),
            task_perfection_percent=_require_percentage(
                metrics,
                "taskPerfectionPercent",
                f"{label}.metrics",
            ),
            implementation_cost_percent=_require_percentage(
                metrics,
                "implementationCostPercent",
                f"{label}.metrics",
            ),
            translations=_load_translations(raw_relay, label),
            source_dir=source_dir,
            readme_sources=_load_readmes(raw_relay, source_dir, label),
            skill_source=skill_source,
            skill_target=skill_target,
            agents_source=agents_source,
            agents_target=agents_target,
            agent_files=tuple(agent_files),
        )
        _validate_relay_source(relay)
        relays.append(relay)

    return InstallerConfig(
        config_path=resolved_config,
        source_root=source_root,
        relays=tuple(relays),
    )


def _validate_relay_source(relay: RelayDefinition) -> None:
    for locale, readme_source in relay.readme_sources.items():
        if not readme_source.is_file():
            raise ConfigError(
                f"{relay.name} 缺少 {locale} README：{readme_source}"
            )
        if readme_source.stat().st_size > MAX_README_BYTES:
            raise ConfigError(
                f"{relay.name} 的 {locale} README 超过大小限制：{readme_source}"
            )
        try:
            readme_source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise ConfigError(
                f"{relay.name} 的 {locale} README 不是有效 UTF-8：{readme_source}"
            ) from error
    if not relay.skill_source.is_dir():
        raise ConfigError(
            f"{relay.name} 的 Skill 源目录不存在：{relay.skill_source}"
        )
    if not (relay.skill_source / "SKILL.md").is_file():
        raise ConfigError(
            f"{relay.name} 的 Skill 源目录缺少 SKILL.md：{relay.skill_source}"
        )
    if not relay.agents_source.is_dir():
        raise ConfigError(
            f"{relay.name} 的 Agent 源目录不存在：{relay.agents_source}"
        )
    for file_name in relay.agent_files:
        source_file = relay.agents_source / file_name
        if not source_file.is_file():
            raise ConfigError(f"{relay.name} 缺少 Agent 源文件：{source_file}")


def _files_equal(left: Path, right: Path) -> bool:
    if not left.is_file() or not right.is_file():
        return False
    if left.stat().st_size != right.stat().st_size:
        return False
    left_hash = hashlib.sha256(left.read_bytes()).digest()
    right_hash = hashlib.sha256(right.read_bytes()).digest()
    return hmac.compare_digest(left_hash, right_hash)


def _directory_digest(directory: Path) -> dict[str, str]:
    digest: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            digest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def _minimal_paths(paths: list[Path]) -> list[Path]:
    unique_paths = {path.resolve(strict=False) for path in paths if path.exists()}
    ordered = sorted(unique_paths, key=lambda path: (len(path.parts), str(path)))
    minimal: list[Path] = []
    for path in ordered:
        if any(
            os.path.commonpath((str(parent), str(path))) == str(parent)
            for parent in minimal
        ):
            continue
        minimal.append(path)
    return minimal


class RelayInstallerService:
    def __init__(
        self,
        config: InstallerConfig,
        *,
        home_root: Path | None = None,
        default_project_root: Path | None = None,
    ) -> None:
        self.config = config
        self.home_root = (home_root or Path.home()).resolve(strict=False)
        self.default_project_root = (
            default_project_root or Path.cwd()
        ).resolve(strict=False)
        self._operation_lock = threading.Lock()

    def bootstrap(self) -> dict[str, Any]:
        return {
            "appName": APP_NAME,
            "globalPath": str(self.home_root),
            "defaultProjectPath": str(self.default_project_root),
            "configPath": str(self.config.config_path),
            "relays": [relay.public_dict() for relay in self.config.relays],
        }

    def read_readme(self, relay_id: str, locale: str) -> dict[str, Any]:
        relay = self.config.relay_by_id(relay_id)
        if not isinstance(locale, str) or not locale.strip() or len(locale) > 32:
            raise ValidationError("README 语言无效。")

        locale_lookup = {
            available_locale.casefold(): available_locale
            for available_locale in relay.readme_sources
        }
        resolved_locale = locale_lookup.get(locale.strip().casefold())
        if resolved_locale is None:
            raise ValidationError(
                f"{relay.name} 没有 {locale.strip()} 版本的 README。"
            )

        readme_source = relay.readme_sources[resolved_locale]
        try:
            content = readme_source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise ValidationError(f"无法读取 README：{readme_source}") from error

        assets: dict[str, str] = {}
        for match in README_IMAGE_PATTERN.finditer(content):
            reference = next(
                (group for group in match.groups() if group is not None),
                "",
            ).strip()
            if not reference or reference in assets:
                continue
            parsed_reference = urlparse(reference)
            if (
                parsed_reference.scheme
                or parsed_reference.netloc
                or reference.startswith(("#", "//"))
            ):
                continue
            relative_asset = unquote(parsed_reference.path)
            try:
                asset_path = _resolve_under(
                    relay.source_dir,
                    relative_asset,
                    f"{relay.name} README 资源",
                )
            except ConfigError:
                continue
            content_type = README_ASSET_TYPES.get(asset_path.suffix.lower())
            if (
                content_type is None
                or not asset_path.is_file()
                or asset_path.stat().st_size > MAX_README_ASSET_BYTES
            ):
                continue
            try:
                encoded_asset = base64.b64encode(asset_path.read_bytes()).decode(
                    "ascii"
                )
            except OSError:
                continue
            assets[reference] = (
                f"data:{content_type};base64,{encoded_asset}"
            )

        return {
            "relayId": relay.relay_id,
            "locale": resolved_locale,
            "fileName": readme_source.name,
            "content": content,
            "assets": assets,
        }

    def _target_root(self, scope: str, project_path: str | None) -> Path:
        if scope == "global":
            target_root = self.home_root
        elif scope == "project":
            if not isinstance(project_path, str) or not project_path.strip():
                raise ValidationError("项目安装需要选择一个安装目录。")
            target_root = _expand_path(project_path.strip()).resolve(strict=False)
        else:
            raise ValidationError("安装范围只能是 global 或 project。")

        if not target_root.is_dir():
            raise ValidationError(f"安装目录不存在或不是目录：{target_root}")
        return target_root

    @staticmethod
    def _target_paths(relay: RelayDefinition, target_root: Path) -> dict[str, Any]:
        skill_path = _resolve_under(
            target_root, relay.skill_target, f"{relay.name} Skill 目标"
        )
        agent_paths = [
            _resolve_under(
                target_root,
                relay.agents_target / file_name,
                f"{relay.name} Agent 目标",
            )
            for file_name in relay.agent_files
        ]
        return {"skill": skill_path, "agents": agent_paths}

    def _detect_relay(
        self, relay: RelayDefinition, target_root: Path
    ) -> dict[str, Any]:
        targets = self._target_paths(relay, target_root)
        skill_path: Path = targets["skill"]
        agent_paths: list[Path] = targets["agents"]
        skill_exists = skill_path.exists()
        agent_evidence: list[dict[str, Any]] = []

        for file_name, target_path in zip(relay.agent_files, agent_paths):
            source_path = relay.agents_source / file_name
            exists = target_path.exists()
            matches = exists and _files_equal(source_path, target_path)
            agent_evidence.append(
                {
                    "path": target_path,
                    "exists": exists,
                    "matches": matches,
                }
            )

        matching_agents = [
            entry["path"] for entry in agent_evidence if entry["matches"]
        ]
        present = skill_exists or bool(matching_agents)
        owned_paths: list[Path] = []
        if skill_exists:
            owned_paths.append(skill_path)
            owned_paths.extend(
                entry["path"] for entry in agent_evidence if entry["exists"]
            )
        else:
            owned_paths.extend(matching_agents)

        complete = (
            skill_path.is_dir()
            and all(entry["path"].is_file() for entry in agent_evidence)
        )
        return {
            "relay": relay,
            "present": present,
            "status": "installed" if complete else "partial",
            "paths": _minimal_paths(owned_paths),
            "targets": targets,
        }

    def _inspect_raw(
        self,
        *,
        scope: str,
        project_path: str | None,
        relay_id: str,
    ) -> dict[str, Any]:
        target_root = self._target_root(scope, project_path)
        selected_relay = self.config.relay_by_id(relay_id)
        detections = [
            self._detect_relay(relay, target_root) for relay in self.config.relays
        ]
        selected_detection = next(
            detection
            for detection in detections
            if detection["relay"].relay_id == relay_id
        )
        conflicts = [
            detection
            for detection in detections
            if detection["present"]
            and detection["relay"].relay_id != relay_id
        ]

        claimed_paths = {
            _path_key(path)
            for detection in detections
            if detection["present"]
            for path in detection["paths"]
        }
        selected_targets = [
            selected_detection["targets"]["skill"],
            *selected_detection["targets"]["agents"],
        ]
        unmanaged_collisions = [
            path
            for path in selected_targets
            if path.exists() and _path_key(path) not in claimed_paths
        ]

        return {
            "scope": scope,
            "targetRoot": target_root,
            "selectedRelay": selected_relay,
            "selectedDetection": selected_detection,
            "conflicts": conflicts,
            "unmanagedCollisions": _minimal_paths(unmanaged_collisions),
        }

    @staticmethod
    def _serialize_detection(detection: dict[str, Any]) -> dict[str, Any]:
        relay: RelayDefinition = detection["relay"]
        return {
            "id": relay.relay_id,
            "name": relay.name,
            "status": detection["status"],
            "paths": [str(path) for path in detection["paths"]],
        }

    def _serialize_inspection(self, inspection: dict[str, Any]) -> dict[str, Any]:
        relay: RelayDefinition = inspection["selectedRelay"]
        selected_detection = inspection["selectedDetection"]
        targets = selected_detection["targets"]
        return {
            "scope": inspection["scope"],
            "targetRoot": str(inspection["targetRoot"]),
            "relay": relay.public_dict(),
            "currentInstallation": (
                self._serialize_detection(selected_detection)
                if selected_detection["present"]
                else None
            ),
            "writeTargets": {
                "skill": str(targets["skill"]),
                "agents": [str(path) for path in targets["agents"]],
            },
            "conflicts": [
                self._serialize_detection(conflict)
                for conflict in inspection["conflicts"]
            ],
            "unmanagedCollisions": [
                str(path) for path in inspection["unmanagedCollisions"]
            ],
            "requiresConfirmation": bool(inspection["conflicts"]),
            "canInstall": not inspection["unmanagedCollisions"],
        }

    def inspect(
        self,
        *,
        scope: str,
        project_path: str | None,
        relay_id: str,
    ) -> dict[str, Any]:
        inspection = self._inspect_raw(
            scope=scope,
            project_path=project_path,
            relay_id=relay_id,
        )
        return self._serialize_inspection(inspection)

    def _inspect_removal_raw(
        self,
        *,
        scope: str,
        project_path: str | None,
    ) -> dict[str, Any]:
        target_root = self._target_root(scope, project_path)
        installations = [
            detection
            for relay in self.config.relays
            if (detection := self._detect_relay(relay, target_root))["present"]
        ]
        active_paths = _minimal_paths(
            [
                path
                for detection in installations
                for path in detection["paths"]
            ]
        )
        return {
            "scope": scope,
            "targetRoot": target_root,
            "installations": installations,
            "activePaths": active_paths,
        }

    def _serialize_removal_inspection(
        self,
        inspection: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "scope": inspection["scope"],
            "targetRoot": str(inspection["targetRoot"]),
            "installations": [
                self._serialize_detection(detection)
                for detection in inspection["installations"]
            ],
            "paths": [str(path) for path in inspection["activePaths"]],
            "canRemove": bool(inspection["activePaths"]),
        }

    def inspect_removal(
        self,
        *,
        scope: str,
        project_path: str | None,
    ) -> dict[str, Any]:
        return self._serialize_removal_inspection(
            self._inspect_removal_raw(
                scope=scope,
                project_path=project_path,
            )
        )

    @staticmethod
    def _relative_backup_path(target_root: Path, source_path: Path) -> Path:
        relative = Path(os.path.relpath(source_path, target_root))
        if relative.is_absolute() or relative.parts[0] == "..":
            raise ValidationError(f"拒绝备份目标根目录外的路径：{source_path}")
        return relative

    @staticmethod
    def _remove_path(path: Path) -> None:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    def _move_paths_to_backup(
        self,
        *,
        target_root: Path,
        active_paths: list[Path],
        manifest_fields: dict[str, Any],
    ) -> tuple[Path | None, list[tuple[Path, Path]]]:
        if not active_paths:
            return None, []

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_root = _resolve_under(
            target_root,
            Path(".relay-installer-backups")
            / f"{stamp}-{secrets.token_hex(4)}",
            "备份目录",
        )
        moved_paths: list[tuple[Path, Path]] = []
        try:
            backup_root.mkdir(parents=True, exist_ok=False)
            for source_path in active_paths:
                relative = self._relative_backup_path(target_root, source_path)
                backup_path = backup_root / relative
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_path), str(backup_path))
                moved_paths.append((source_path, backup_path))

            manifest = {
                "createdAt": datetime.now().astimezone().isoformat(),
                "targetRoot": str(target_root),
                **manifest_fields,
                "paths": [
                    {
                        "original": str(original),
                        "backup": str(backup),
                    }
                    for original, backup in moved_paths
                ],
            }
            (backup_root / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            self._restore_moved_paths(moved_paths)
            if backup_root.exists():
                shutil.rmtree(backup_root)
            raise
        return backup_root, moved_paths

    @staticmethod
    def _restore_moved_paths(moved_paths: list[tuple[Path, Path]]) -> None:
        for original_path, backup_path in reversed(moved_paths):
            if backup_path.exists():
                original_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(backup_path), str(original_path))

    def _verify_installed(
        self,
        relay: RelayDefinition,
        target_root: Path,
    ) -> None:
        targets = self._target_paths(relay, target_root)
        skill_target: Path = targets["skill"]
        if _directory_digest(relay.skill_source) != _directory_digest(skill_target):
            raise RelayInstallerError("安装后的 Skill 内容校验失败。")
        for file_name, target_path in zip(relay.agent_files, targets["agents"]):
            if not _files_equal(relay.agents_source / file_name, target_path):
                raise RelayInstallerError(
                    f"安装后的 Agent 内容校验失败：{target_path}"
                )

    def install(
        self,
        *,
        scope: str,
        project_path: str | None,
        relay_id: str,
        remove_conflicts: bool,
    ) -> dict[str, Any]:
        if not self._operation_lock.acquire(blocking=False):
            raise RelayInstallerError("另一个安装或移除操作正在进行，请稍后重试。")

        try:
            inspection = self._inspect_raw(
                scope=scope,
                project_path=project_path,
                relay_id=relay_id,
            )
            serialized_inspection = self._serialize_inspection(inspection)
            if inspection["unmanagedCollisions"]:
                raise UnsafeCollisionError(
                    "目标位置存在无法确认归属的同名内容，安装器不会自动覆盖。",
                    details=serialized_inspection,
                )
            if inspection["conflicts"] and not remove_conflicts:
                raise ConflictError(
                    "检测到其他 Relay 调度，必须确认移除后才能继续。",
                    details=serialized_inspection,
                )

            target_root: Path = inspection["targetRoot"]
            relay: RelayDefinition = inspection["selectedRelay"]
            selected_detection = inspection["selectedDetection"]
            active_paths = list(selected_detection["paths"])
            for conflict in inspection["conflicts"]:
                active_paths.extend(conflict["paths"])
            active_paths = _minimal_paths(active_paths)

            moved_paths: list[tuple[Path, Path]] = []
            backup_root: Path | None = None
            targets = self._target_paths(relay, target_root)
            installed_targets = [targets["skill"], *targets["agents"]]

            try:
                if active_paths:
                    backup_root, moved_paths = self._move_paths_to_backup(
                        target_root=target_root,
                        active_paths=active_paths,
                        manifest_fields={
                            "operation": "install",
                            "installedRelay": relay.relay_id,
                            "removedRelays": [
                                conflict["relay"].relay_id
                                for conflict in inspection["conflicts"]
                            ],
                        },
                    )

                targets["skill"].parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(relay.skill_source, targets["skill"])
                targets["agents"][0].parent.mkdir(parents=True, exist_ok=True)
                for file_name, target_path in zip(
                    relay.agent_files, targets["agents"]
                ):
                    shutil.copy2(relay.agents_source / file_name, target_path)

                self._verify_installed(relay, target_root)
            except Exception:
                for installed_path in reversed(installed_targets):
                    if installed_path.exists():
                        self._remove_path(installed_path)
                self._restore_moved_paths(moved_paths)
                if backup_root and backup_root.exists():
                    shutil.rmtree(backup_root)
                raise

            return {
                "ok": True,
                "relay": relay.public_dict(),
                "scope": scope,
                "targetRoot": str(target_root),
                "installedPaths": [str(path) for path in installed_targets],
                "removedRelays": [
                    self._serialize_detection(conflict)
                    for conflict in inspection["conflicts"]
                ],
                "backupPath": str(backup_root) if backup_root else None,
                "message": f"{relay.name} 已安装完成。",
            }
        finally:
            self._operation_lock.release()

    def remove_relays(
        self,
        *,
        scope: str,
        project_path: str | None,
    ) -> dict[str, Any]:
        if not self._operation_lock.acquire(blocking=False):
            raise RelayInstallerError("另一个安装或移除操作正在进行，请稍后重试。")

        try:
            inspection = self._inspect_removal_raw(
                scope=scope,
                project_path=project_path,
            )
            target_root: Path = inspection["targetRoot"]
            installations: list[dict[str, Any]] = inspection["installations"]
            active_paths: list[Path] = inspection["activePaths"]
            if not active_paths:
                return {
                    "ok": True,
                    "scope": scope,
                    "targetRoot": str(target_root),
                    "removedRelays": [],
                    "removedPaths": [],
                    "backupPath": None,
                    "message": "目标目录中没有可移除的已知 Relay。",
                }

            backup_root: Path | None = None
            moved_paths: list[tuple[Path, Path]] = []
            try:
                backup_root, moved_paths = self._move_paths_to_backup(
                    target_root=target_root,
                    active_paths=active_paths,
                    manifest_fields={
                        "operation": "remove",
                        "removedRelays": [
                            detection["relay"].relay_id
                            for detection in installations
                        ],
                    },
                )
                remaining_paths = [path for path in active_paths if path.exists()]
                if remaining_paths:
                    raise RelayInstallerError(
                        "移除后的路径校验失败。",
                        details={"paths": [str(path) for path in remaining_paths]},
                    )
            except Exception:
                self._restore_moved_paths(moved_paths)
                if backup_root and backup_root.exists():
                    shutil.rmtree(backup_root)
                raise

            return {
                "ok": True,
                "scope": scope,
                "targetRoot": str(target_root),
                "removedRelays": [
                    self._serialize_detection(detection)
                    for detection in installations
                ],
                "removedPaths": [str(path) for path in active_paths],
                "backupPath": str(backup_root) if backup_root else None,
                "message": "已移除当前目录中的已知 Relay 调度文件。",
            }
        finally:
            self._operation_lock.release()


def choose_directory(initial_path: str | None) -> str | None:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as error:
        raise RelayInstallerError(
            "当前 Python 环境缺少 Tk，无法打开原生目录选择器。"
        ) from error

    initial = _expand_path(initial_path).resolve(strict=False) if initial_path else None
    if not initial or not initial.is_dir():
        initial = Path.cwd().resolve(strict=False)

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        selected = filedialog.askdirectory(
            parent=root,
            title="选择 Relay 项目安装目录",
            initialdir=str(initial),
            mustexist=True,
        )
    finally:
        root.destroy()
    return selected or None


def _runtime_roots() -> list[Path]:
    roots: list[Path] = []
    if getattr(sys, "frozen", False):
        roots.append(Path(sys.executable).resolve().parent)
    if hasattr(sys, "_MEIPASS"):
        roots.append(Path(getattr(sys, "_MEIPASS")).resolve())
    roots.append(Path(__file__).resolve().parent)
    unique: list[Path] = []
    for root in roots:
        if root not in unique:
            unique.append(root)
    return unique


def default_config_path() -> Path:
    for root in _runtime_roots():
        candidate = root / CONFIG_NAME
        if candidate.is_file():
            return candidate
    return _runtime_roots()[0] / CONFIG_NAME


def default_web_root() -> Path:
    for root in _runtime_roots():
        candidate = root / "web"
        if candidate.is_dir():
            return candidate
    return _runtime_roots()[0] / "web"


def make_request_handler(
    service: RelayInstallerService,
    web_root: Path,
    session_token: str,
) -> type[BaseHTTPRequestHandler]:
    allowed_static_files = {
        "/": ("index.html", "text/html; charset=utf-8"),
        "/index.html": ("index.html", "text/html; charset=utf-8"),
        "/styles.css": ("styles.css", "text/css; charset=utf-8"),
        "/readme-renderer.js": (
            "readme-renderer.js",
            "text/javascript; charset=utf-8",
        ),
        "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    }

    class RequestHandler(BaseHTTPRequestHandler):
        server_version = "RelayInstaller/1.0"

        def log_message(self, format_string: str, *args: Any) -> None:
            if getattr(self.server, "verbose", False):
                super().log_message(format_string, *args)

        def _host_is_allowed(self) -> bool:
            host = self.headers.get("Host", "").split(":", 1)[0].lower()
            return host in {"127.0.0.1", "localhost"}

        def _send_security_headers(self) -> None:
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self'; "
                "img-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'none'; "
                "form-action 'self'",
            )

        def _send_json(
            self,
            payload: dict[str, Any],
            status: HTTPStatus = HTTPStatus.OK,
        ) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self._send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        def _send_error_payload(self, error: Exception) -> None:
            if isinstance(error, RelayInstallerError):
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": error.code,
                            "message": str(error),
                            "details": error.details,
                        },
                    },
                    error.status,
                )
                return
            self._send_json(
                {
                    "ok": False,
                    "error": {
                        "code": "internal_error",
                        "message": "安装器发生未预期错误，请查看终端日志。",
                    },
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            print(f"[ERROR] {error}", file=sys.stderr)

        def _require_local_host(self) -> bool:
            if self._host_is_allowed():
                return True
            self._send_json(
                {
                    "ok": False,
                    "error": {
                        "code": "invalid_host",
                        "message": "仅允许通过本机地址访问安装器。",
                    },
                },
                HTTPStatus.MISDIRECTED_REQUEST,
            )
            return False

        def do_GET(self) -> None:
            if not self._require_local_host():
                return
            request_path = urlparse(self.path).path
            if request_path == "/api/bootstrap":
                payload = service.bootstrap()
                payload["sessionToken"] = session_token
                self._send_json({"ok": True, "data": payload})
                return
            if request_path == "/favicon.ico":
                self.send_response(HTTPStatus.NO_CONTENT)
                self._send_security_headers()
                self.end_headers()
                return
            static_file = allowed_static_files.get(request_path)
            if not static_file:
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": "not_found",
                            "message": "页面不存在。",
                        },
                    },
                    HTTPStatus.NOT_FOUND,
                )
                return

            file_name, content_type = static_file
            file_path = (web_root / file_name).resolve(strict=False)
            if web_root.resolve(strict=False) not in file_path.parents:
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": "invalid_path",
                            "message": "拒绝访问页面目录外的文件。",
                        },
                    },
                    HTTPStatus.FORBIDDEN,
                )
                return
            try:
                body = file_path.read_bytes()
            except OSError as error:
                self._send_error_payload(error)
                return

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self._send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict[str, Any]:
            content_length = self.headers.get("Content-Length")
            if content_length is None:
                raise ValidationError("请求缺少 Content-Length。")
            try:
                length = int(content_length)
            except ValueError as error:
                raise ValidationError("Content-Length 无效。") from error
            if length < 0 or length > MAX_REQUEST_BYTES:
                raise ValidationError("请求内容过大。")
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValidationError("请求 JSON 无效。") from error
            if not isinstance(payload, dict):
                raise ValidationError("请求正文必须是 JSON 对象。")
            return payload

        def _require_session_token(self) -> bool:
            received_token = self.headers.get("X-Installer-Token", "")
            if hmac.compare_digest(received_token, session_token):
                return True
            self._send_json(
                {
                    "ok": False,
                    "error": {
                        "code": "invalid_session",
                        "message": "安装器会话已失效，请刷新页面。",
                    },
                },
                HTTPStatus.FORBIDDEN,
            )
            return False

        def do_POST(self) -> None:
            if not self._require_local_host() or not self._require_session_token():
                return
            request_path = unquote(urlparse(self.path).path)
            try:
                payload = self._read_json()
                if request_path == "/api/browse":
                    selected = choose_directory(payload.get("initialPath"))
                    self._send_json(
                        {"ok": True, "data": {"path": selected}}
                    )
                    return
                if request_path == "/api/readme":
                    readme = service.read_readme(
                        relay_id=payload.get("relayId"),
                        locale=payload.get("locale"),
                    )
                    self._send_json({"ok": True, "data": readme})
                    return
                if request_path == "/api/inspect":
                    inspection = service.inspect(
                        scope=payload.get("scope"),
                        project_path=payload.get("projectPath"),
                        relay_id=payload.get("relayId"),
                    )
                    self._send_json({"ok": True, "data": inspection})
                    return
                if request_path == "/api/install":
                    result = service.install(
                        scope=payload.get("scope"),
                        project_path=payload.get("projectPath"),
                        relay_id=payload.get("relayId"),
                        remove_conflicts=payload.get("removeConflicts") is True,
                    )
                    self._send_json({"ok": True, "data": result})
                    return
                if request_path == "/api/remove/inspect":
                    inspection = service.inspect_removal(
                        scope=payload.get("scope"),
                        project_path=payload.get("projectPath"),
                    )
                    self._send_json({"ok": True, "data": inspection})
                    return
                if request_path == "/api/remove":
                    result = service.remove_relays(
                        scope=payload.get("scope"),
                        project_path=payload.get("projectPath"),
                    )
                    self._send_json({"ok": True, "data": result})
                    return
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": "not_found",
                            "message": "接口不存在。",
                        },
                    },
                    HTTPStatus.NOT_FOUND,
                )
            except Exception as error:
                self._send_error_payload(error)

    return RequestHandler


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="启动配置驱动的 Relay 本地网页安装器。"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="配置文件路径；默认优先读取可执行文件旁的配置。",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="本机端口；0 表示自动选择空闲端口。",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="启动服务但不自动打开浏览器。",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="只校验配置与 Relay 源文件，不启动服务。",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="输出 HTTP 访问日志。",
    )
    return parser


def _configure_standard_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    _configure_standard_streams()
    args = _build_parser().parse_args(argv)
    config_path = args.config or default_config_path()
    try:
        config = load_installer_config(config_path)
        web_root = default_web_root()
        if not args.check and not web_root.is_dir():
            raise ConfigError(f"找不到网页资源目录：{web_root}")
    except RelayInstallerError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    if args.check:
        print(f"[OK] 配置有效：{config.config_path}")
        print(f"[OK] Relay 源目录：{config.source_root}")
        print(f"[OK] 已发现 {len(config.relays)} 种 Relay。")
        return 0

    service = RelayInstallerService(config)
    session_token = secrets.token_urlsafe(32)
    handler = make_request_handler(service, web_root, session_token)
    server = HTTPServer(("127.0.0.1", args.port), handler)
    server.verbose = args.verbose  # type: ignore[attr-defined]
    port = server.server_address[1]
    url = f"http://127.0.0.1:{port}/"

    print(f"[READY] {APP_NAME}: {url}")
    print(f"[CONFIG] {config.config_path}")
    print("[STOP] 按 Ctrl+C 停止本地服务。")
    if not args.no_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        print("\n[STOPPED] Relay Installer 已停止。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
