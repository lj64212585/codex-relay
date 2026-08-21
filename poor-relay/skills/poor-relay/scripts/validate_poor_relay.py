from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = SKILL_DIR.parent.parent

EXPECTED_AGENTS = {
    "tm_planner.toml": ("tm_planner", "gpt-5.6-sol", "xhigh", "workspace-write"),
    "tm_explorer.toml": ("tm_explorer", "gpt-5.6-luna", "medium", "read-only"),
    "tm_executor.toml": ("tm_executor", "gpt-5.6-luna", "high", "workspace-write"),
    "tm_reviewer.toml": ("tm_reviewer", "gpt-5.6-terra", "medium", "read-only"),
    "tm_integrator.toml": ("tm_integrator", "gpt-5.6-sol", "xhigh", "workspace-write"),
}

REQUIRED_REFERENCES = {
    "references/execution-plan.md",
    "references/runtime-state.md",
}

SOURCE_FILES = {
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "scripts/install.ps1",
    "scripts/uninstall.ps1",
    "scripts/verify.ps1",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    require(path.is_file(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def locate_agent_dir() -> tuple[Path, bool]:
    source_agents = PACKAGE_ROOT / "agents"
    if source_agents.is_dir():
        return source_agents, True

    installed_agents = Path.home() / ".codex" / "agents"
    if installed_agents.is_dir():
        return installed_agents, False

    fail("unable to locate package agents/ or installed ~/.codex/agents/")


def validate_skill() -> None:
    skill_path = SKILL_DIR / "SKILL.md"
    text = read_text(skill_path)
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("\nname: poor-relay\n" in text, "unexpected skill name")
    require("Orchestrate non-trivial project work" in text, "skill description is not discriminating")
    placeholder_marker = "[" + "TODO"
    require(placeholder_marker not in text, "unfinished scaffold placeholder in SKILL.md")
    require(len(text.encode("utf-8")) <= 16_000, "SKILL.md exceeds the 16 KiB budget")
    require(len(text.splitlines()) <= 250, "SKILL.md exceeds the 250-line budget")

    for relative in REQUIRED_REFERENCES:
        require((SKILL_DIR / relative).is_file(), f"missing reference: {relative}")

    yaml_text = read_text(SKILL_DIR / "agents" / "openai.yaml")
    require('display_name: "Poor Relay"' in yaml_text, "openai.yaml display name mismatch")
    require("$poor-relay" in yaml_text, "default prompt must mention $poor-relay")
    require("allow_implicit_invocation: true" in yaml_text, "implicit invocation is not enabled")
    require("allow_implicit_invocation: false" not in yaml_text, "explicit-only policy found")

    short_match = re.search(r'short_description:\s*"([^"]+)"', yaml_text)
    require(short_match is not None, "openai.yaml short_description missing")
    short_description = short_match.group(1)
    require(25 <= len(short_description) <= 64, "short_description must contain 25-64 characters")


def validate_agents(agent_dir: Path) -> None:
    require(not (agent_dir / "default.toml").exists(), "default.toml must not be installed")

    seen_names: set[str] = set()
    for filename, expected in EXPECTED_AGENTS.items():
        expected_name, expected_model, expected_effort, expected_sandbox = expected
        path = agent_dir / filename
        require(path.is_file(), f"missing Agent profile: {filename}")

        with path.open("rb") as handle:
            data = tomllib.load(handle)

        for key in ("name", "description", "developer_instructions"):
            value = data.get(key)
            require(isinstance(value, str) and value.strip(), f"{filename}: missing {key}")

        require(data["name"] == expected_name, f"{filename}: unexpected name")
        require(data.get("model") == expected_model, f"{filename}: unexpected model")
        require(data.get("model_reasoning_effort") == expected_effort, f"{filename}: unexpected effort")
        require(data.get("sandbox_mode") == expected_sandbox, f"{filename}: unexpected sandbox")
        require(data["name"] not in seen_names, f"duplicate Agent name: {data['name']}")
        seen_names.add(data["name"])

        instructions = data["developer_instructions"]
        require("Do not spawn subagents" in instructions, f"{filename}: missing descendant ban")
        require("Do not commit, push" in instructions, f"{filename}: missing delivery boundary")
        require("Preserve unrelated work" in instructions, f"{filename}: missing workspace boundary")

    require(len(seen_names) == len(EXPECTED_AGENTS), "Agent count mismatch")


def validate_role_contracts(agent_dir: Path) -> None:
    planner = read_text(agent_dir / "tm_planner.toml")
    require("Planning Mode" in planner, "planner mode boundary missing")
    require("plan.md" in planner and "Do not edit product code" in planner, "planner write boundary missing")

    explorer = read_text(agent_dir / "tm_explorer.toml")
    require("CodeGraph before grep" in explorer, "CodeGraph routing rule missing")
    require("EVIDENCE_READY" in explorer and "first-party sources" in explorer, "explorer packet missing")

    executor = read_text(agent_dir / "tm_executor.toml")
    require("smallest defensible diff" in executor, "minimal-change rule missing")
    require("one targeted correction" in executor, "executor correction limit missing")
    require("Only modify assigned files" in executor, "file ownership rule missing")

    reviewer = read_text(agent_dir / "tm_reviewer.toml")
    require("Return PASS" in reviewer and "return FAIL" in reviewer, "reviewer verdict contract missing")
    require("Omit style-only comments" in reviewer, "reviewer scope filter missing")

    integrator = read_text(agent_dir / "tm_integrator.toml")
    require("Escalation Mode or Final Mode" in integrator, "integrator modes missing")
    require("Do not delete runtime state" in integrator, "runtime cleanup ownership missing")

    skill = read_text(SKILL_DIR / "SKILL.md")
    for snippet in (
        "Every dispatch names an exact agent type",
        "Never stage or commit .codex-team",
        "Reviewer risk gate",
        "Terra remains a reviewer",
        "A wait timeout, silence, token use, or absence of a file is not proof of failure",
        "Accept FINAL_PASS only as technical evidence",
    ):
        require(snippet in skill, f"SKILL.md missing workflow invariant: {snippet}")

    plan = read_text(SKILL_DIR / "references" / "execution-plan.md")
    for field in ("Owns:", "Must Not Change:", "Interfaces:", "Acceptance:", "Checks:", "Risk:", "Review:"):
        require(field in plan, f"execution plan field missing: {field}")

    state = read_text(SKILL_DIR / "references" / "runtime-state.md")
    for field in ("status:", "executor:", "checks:", "review:", "retry:", "escalation:", "evidence:", "next:"):
        require(field in state, f"runtime state field missing: {field}")
    require("evidence, not authority" in state, "runtime recovery evidence boundary missing")


def validate_source_package(is_source: bool) -> None:
    if not is_source:
        return

    for relative in SOURCE_FILES:
        require((PACKAGE_ROOT / relative).is_file(), f"missing source package file: {relative}")

    all_text = []
    for path in PACKAGE_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".toml", ".yaml", ".yml", ".py", ".ps1"}:
            all_text.append(read_text(path))
    combined = "\n".join(all_text).lower()
    legacy_project_name = "codex-" + "team-mode-" + "lite"
    legacy_skill_name = "team-mode-" + "lite"
    require(legacy_project_name not in combined, "legacy project name remains")
    require(legacy_skill_name not in combined, "legacy skill name remains")

    notices = read_text(PACKAGE_ROOT / "THIRD_PARTY_NOTICES.md")
    for copyright_line in (
        "Copyright (c) 2026 oil-oil",
        "Copyright (c) 2024 Seth Hobson",
        "Copyright (c) 2025 AgentLand Contributors",
        "Copyright (c) 2025 Jesse Vincent",
    ):
        require(copyright_line in notices, f"third-party notice missing: {copyright_line}")


def main() -> int:
    agent_dir, is_source = locate_agent_dir()
    validate_skill()
    validate_agents(agent_dir)
    validate_role_contracts(agent_dir)
    validate_source_package(is_source)
    print(f"[OK] skill={SKILL_DIR}")
    print(f"[OK] agents={len(EXPECTED_AGENTS)} directory={agent_dir}")
    print("[OK] names, models, effort, sandbox defaults, workflow gates, and notices validated")
    if not is_source:
        print("[NOTE] static validation does not prove fresh-task discovery or effective sandbox enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
