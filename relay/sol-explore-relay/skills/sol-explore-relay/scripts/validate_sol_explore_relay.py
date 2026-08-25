from __future__ import annotations

import sys
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = SKILL_DIR.parent.parent

EXPECTED = {
    "sol_explore_code.toml": ("sol_explore_code", "gpt-5.6-luna"),
    "sol_explore_docs.toml": ("sol_explore_docs", "gpt-5.6-luna"),
    "sol_explore_runtime.toml": ("sol_explore_runtime", "gpt-5.6-luna"),
    "sol_explore_runtime_deep.toml": ("sol_explore_runtime_deep", "gpt-5.6-terra"),
}

REQUIRED_REFERENCES = {
    "references/contracts.md",
    "references/routing.md",
    "references/evaluation.md",
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


def locate_agent_dir() -> Path:
    candidates = [PACKAGE_ROOT / "agents"]
    if len(SKILL_DIR.parents) > 2:
        candidates.append(SKILL_DIR.parents[2] / ".codex" / "agents")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    fail("unable to locate package agents/ or installed project .codex/agents/")


def validate_skill() -> None:
    text = read_text(SKILL_DIR / "SKILL.md")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("\nname: sol-explore-relay\n" in text, "unexpected skill name")
    require(
        "automatically delegating only bounded read-only exploration" in text,
        "description must advertise the narrow implicit route",
    )
    require(len(text.encode("utf-8")) <= 16_000, "SKILL.md exceeds the 16 KiB package budget")
    require(len(text.splitlines()) <= 190, "SKILL.md exceeds the 190-line package budget")

    for snippet in (
        "All edits and implementation stay in parent Sol",
        "Only these routes may be delegated",
        "never use full-history inheritance",
        "at most three independent Explorers",
        "do not repeat the child's broad exploration",
        "Silence alone never authorizes interruption",
        "keep the child intact",
        "Retry a spawn or transport failure at most once",
        "The parent decides whether the evidence is sufficient",
    ):
        require(snippet in text, f"SKILL.md missing boundary: {snippet}")

    for relative in REQUIRED_REFERENCES:
        require((SKILL_DIR / relative).is_file(), f"missing reference: {relative}")

    yaml_text = read_text(SKILL_DIR / "agents" / "openai.yaml")
    require("allow_implicit_invocation: true" in yaml_text, "implicit invocation is not enabled")
    require("allow_implicit_invocation: false" not in yaml_text, "explicit-only policy found")
    require("$sol-explore-relay" in yaml_text, "default prompt must mention the skill")


def validate_agents(agent_dir: Path) -> None:
    source_agent_dir = PACKAGE_ROOT / "agents"
    if source_agent_dir.is_dir():
        source_files = {path.name for path in source_agent_dir.glob("*.toml")}
        require(source_files == set(EXPECTED), f"source Agent set mismatch: {sorted(source_files)}")
    require(not (agent_dir / "default.toml").exists(), "default.toml must not be installed")

    seen_names: set[str] = set()
    for filename, (expected_name, expected_model) in EXPECTED.items():
        path = agent_dir / filename
        require(path.is_file(), f"missing Agent profile: {filename}")
        with path.open("rb") as handle:
            data = tomllib.load(handle)

        for key in ("name", "description", "developer_instructions"):
            require(isinstance(data.get(key), str) and data[key].strip(), f"{filename}: missing {key}")

        require(data["name"] == expected_name, f"{filename}: unexpected name {data['name']!r}")
        require(data.get("model") == expected_model, f"{filename}: unexpected model")
        require(data.get("model_reasoning_effort") == "max", f"{filename}: effort must be max")
        require(data.get("sandbox_mode") == "read-only", f"{filename}: sandbox must be read-only")
        require(data["name"] not in seen_names, f"duplicate Agent name: {data['name']}")
        seen_names.add(data["name"])

        instructions = data["developer_instructions"]
        require("Do not spawn subagents" in instructions, f"{filename}: missing descendant ban")
        require("Do not commit, push" in instructions, f"{filename}: missing delivery boundary")
        require("Do not edit" in instructions or "Stay read-only" in instructions, f"{filename}: missing mutation ban")

    require(len(seen_names) == 4, "Agent count must be exactly four")


def validate_special_rules(agent_dir: Path) -> None:
    ordinary = read_text(agent_dir / "sol_explore_runtime.toml")
    require("one investigation pass" in ordinary, "ordinary runtime role must stop after one pass")
    require("return INCONCLUSIVE directly to the parent" in ordinary, "inconclusive return rule missing")
    require("Do not retry" in ordinary, "ordinary runtime retry ban missing")

    deep = read_text(agent_dir / "sol_explore_runtime_deep.toml")
    require("cross-system" in deep and "contradictory" in deep, "deep runtime gate missing")
    require("not a fallback" in deep, "deep runtime fallback ban missing")

    routing = read_text(SKILL_DIR / "references" / "routing.md")
    require("Never delegate these roles" in routing, "parent-only role boundary missing")
    for role in ("Executor", "Reviewer", "Integrator"):
        require(role in routing, f"routing boundary missing role: {role}")

    contracts = read_text(SKILL_DIR / "references" / "contracts.md")
    for field in (
        "Outcome",
        "Context benefit",
        "Question",
        "Sources",
        "Scope",
        "Allowed checks",
        "Stop when",
        "Return",
    ):
        require(field in contracts, f"dispatch field missing: {field}")
    require("## Checkpoint request" in contracts, "checkpoint contract missing")
    require("report any unexpected mutation immediately" in contracts, "read-only checkpoint invariant missing")
    require("is an orchestration event, not a result status" in contracts, "interruption boundary missing")

    evaluation = read_text(SKILL_DIR / "references" / "evaluation.md")
    require("## Fresh-session requirement" in evaluation, "fresh-session gate missing")
    require("NOT_ENFORCED" in evaluation, "permission failure label missing")
    require("must remain in parent Sol" in evaluation, "forward test for parent implementation missing")
    require("keep the child intact" in evaluation, "silent-child preservation rule missing")


def main() -> int:
    agent_dir = locate_agent_dir()
    validate_skill()
    validate_agents(agent_dir)
    validate_special_rules(agent_dir)
    print(f"[OK] skill={SKILL_DIR}")
    print(f"[OK] agents={len(EXPECTED)} directory={agent_dir}")
    print("[OK] Explore-only routing, exact models, max effort, read-only defaults, and parent-Sol ownership validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
