from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = SKILL_DIR.parent.parent

EXPECTED_AGENTS = {
    "tm_explorer.toml": ("tm_explorer", "gpt-5.6-luna", "max", "read-only"),
    "tm_planner.toml": ("tm_planner", "gpt-5.6-sol", "max", "workspace-write"),
    "tm_executor.toml": ("tm_executor", "gpt-5.6-sol", "max", "workspace-write"),
}

REQUIRED_SKILL_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/execution-plan.md",
}

REQUIRED_SOURCE_FILES = {
    "README.md",
    "README.en.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "assets/readme/hero.svg",
    "assets/readme/hero.en.svg",
    "assets/readme/relay-flow.svg",
    "assets/readme/relay-flow.en.svg",
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
    for relative in REQUIRED_SKILL_FILES:
        require((SKILL_DIR / relative).is_file(), f"missing Skill file: {relative}")

    skill_path = SKILL_DIR / "SKILL.md"
    text = read_text(skill_path)
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("\nname: sol-pair-relay\n" in text, "unexpected Skill name")
    require(
        "second fresh Sol Max" in text,
        "Skill description does not distinguish the split-context workflow",
    )
    placeholder_marker = "[" + "TODO"
    require(placeholder_marker not in text, "unfinished scaffold placeholder in SKILL.md")
    require(len(text.encode("utf-8")) <= 16_000, "SKILL.md exceeds the 16 KiB budget")
    require(len(text.splitlines()) <= 260, "SKILL.md exceeds the 260-line budget")

    yaml_text = read_text(SKILL_DIR / "agents" / "openai.yaml")
    require('display_name: "Sol Pair Relay"' in yaml_text, "openai.yaml display name mismatch")
    require("$sol-pair-relay" in yaml_text, "default prompt must mention $sol-pair-relay")
    require("allow_implicit_invocation: true" in yaml_text, "implicit invocation is not enabled")
    require("allow_implicit_invocation: false" not in yaml_text, "explicit-only policy found")

    short_match = re.search(r'short_description:\s*"([^"]+)"', yaml_text)
    require(short_match is not None, "openai.yaml short_description missing")
    short_description = short_match.group(1)
    require(25 <= len(short_description) <= 64, "short_description must contain 25-64 characters")


def validate_agents(agent_dir: Path, is_source: bool) -> None:
    require(not (agent_dir / "default.toml").exists(), "default.toml must not be installed")

    if is_source:
        source_profiles = {path.name for path in agent_dir.glob("*.toml")}
        require(source_profiles == set(EXPECTED_AGENTS), "source package must contain exactly 3 profiles")

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

    require(len(seen_names) == 3, "Agent count mismatch")


def validate_role_contracts(agent_dir: Path) -> None:
    explorer = read_text(agent_dir / "tm_explorer.toml")
    require("CodeGraph before grep" in explorer, "Explorer CodeGraph routing rule missing")
    require("EVIDENCE_READY" in explorer, "Explorer return packet missing")
    require("Do not edit files" in explorer, "Explorer mutation ban missing")

    planner = read_text(agent_dir / "tm_planner.toml")
    require("Planning Mode" in planner, "Planner mode boundary missing")
    require("plan.md" in planner, "Planner output path missing")
    require("Do not edit product code" in planner, "Planner product-write ban missing")
    require("one separate Sol executor" in planner, "Planner handoff target missing")

    executor = read_text(agent_dir / "tm_executor.toml")
    require("EXECUTION_PASS" in executor, "Executor success packet missing")
    require("actual final diff" in executor, "Executor diff inspection missing")
    require("acceptance matrix" in executor, "Executor acceptance gate missing")
    require("Only modify assigned files" in executor, "Executor ownership boundary missing")
    require("one targeted correction" in executor, "Executor correction limit missing")

    skill = read_text(SKILL_DIR / "SKILL.md")
    for snippet in (
        "Never send one child both planning and implementation",
        'prefer fork_turns = "none"',
        "The durable handoff is the approved plan.md",
        "planner and executor concurrently",
        "There is no automatic Reviewer, Integrator",
        "EXECUTION_PASS is technical evidence",
        "Never stage or commit .codex-team",
    ):
        require(snippet in skill, f"SKILL.md missing workflow invariant: {snippet}")

    plan = read_text(SKILL_DIR / "references" / "execution-plan.md")
    for field in (
        "Fixed Decisions:",
        "Evidence Basis:",
        "Writable Scope:",
        "Protected Paths and Contracts:",
        "Interfaces and Invariants:",
        "Acceptance Evidence:",
        "Checks:",
        "Stop When:",
        "## Acceptance Matrix",
        "Final Checks:",
        "Residual Gates:",
    ):
        require(field in plan, f"temporary plan field missing: {field}")


def validate_source_package(is_source: bool) -> None:
    if not is_source:
        return

    for relative in REQUIRED_SOURCE_FILES:
        require((PACKAGE_ROOT / relative).is_file(), f"missing source package file: {relative}")

    combined_parts = []
    for path in PACKAGE_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".toml", ".yaml", ".yml", ".py", ".ps1"}:
            combined_parts.append(read_text(path))
    combined = "\n".join(combined_parts)
    require("default.toml" not in {path.name for path in (PACKAGE_ROOT / "agents").iterdir()}, "default profile found")
    placeholder_marker = "[" + "TODO"
    require(placeholder_marker not in combined, "unfinished scaffold placeholder found")
    require("Poor Relay" in combined, "same-name profile conflict with Poor Relay is undocumented")

    notices = read_text(PACKAGE_ROOT / "THIRD_PARTY_NOTICES.md")
    for copyright_line in (
        "Copyright (c) 2026 Poor Relay contributors",
        "Copyright (c) 2026 oil-oil",
        "Copyright (c) 2024 Seth Hobson",
        "Copyright (c) 2025 AgentLand Contributors",
        "Copyright (c) 2025 Jesse Vincent",
    ):
        require(copyright_line in notices, f"third-party notice missing: {copyright_line}")


def main() -> int:
    agent_dir, is_source = locate_agent_dir()
    validate_skill()
    validate_agents(agent_dir, is_source)
    validate_role_contracts(agent_dir)
    validate_source_package(is_source)
    print(f"[OK] skill={SKILL_DIR}")
    print(f"[OK] agents={len(EXPECTED_AGENTS)} directory={agent_dir}")
    print("[OK] fresh-context split, models, effort, sandbox defaults, plan handoff, and acceptance gates validated")
    if not is_source:
        print("[NOTE] static validation does not prove fresh-task discovery or effective sandbox enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
