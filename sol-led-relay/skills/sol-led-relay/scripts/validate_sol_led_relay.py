from __future__ import annotations

import sys
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = SKILL_DIR.parent.parent

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
    fail("unable to locate root agents/ or installed project .codex/agents/")


def validate_skill() -> None:
    text = read_text(SKILL_DIR / "SKILL.md")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("\nname: sol-led-relay\n" in text, "unexpected skill name")
    require("Use implicitly" in text, "description must advertise implicit routing")
    require(len(text.encode("utf-8")) <= 18_000, "SKILL.md exceeds the 18 KiB package budget")
    require(len(text.splitlines()) <= 220, "SKILL.md exceeds the 220-line package budget")
    for snippet in (
        "A wait timeout is only a polling observation",
        "A writer can be live before its first file change",
        "Do not call `interrupt_agent` merely because",
        "suspected infrastructure hang",
        "keep the child intact",
        "record the partial-result audit",
        "Silence never authorizes retry, takeover, or interruption by itself",
        "a recorded parent cancellation required by",
        "`INTERRUPTED` is an orchestration event",
        "never authorizes automatic retry",
        "only when no child remains running",
    ):
        require(snippet in text, f"SKILL.md missing liveness rule: {snippet}")
    for relative in REQUIRED_REFERENCES:
        require((SKILL_DIR / relative).is_file(), f"missing reference: {relative}")

    yaml_text = read_text(SKILL_DIR / "agents" / "openai.yaml")
    require("allow_implicit_invocation: true" in yaml_text, "implicit invocation is not enabled")
    require("allow_implicit_invocation: false" not in yaml_text, "explicit-only policy found")
    require("$sol-led-relay" in yaml_text, "default prompt must mention the skill")


def validate_agents(agent_dir: Path) -> None:
    require(not (agent_dir / "default.toml").exists(), "default.toml guard must not be installed")

    seen_names: set[str] = set()
    for filename, (expected_name, expected_model, expected_sandbox) in EXPECTED.items():
        path = agent_dir / filename
        require(path.is_file(), f"missing Agent profile: {filename}")
        with path.open("rb") as handle:
            data = tomllib.load(handle)

        for key in ("name", "description", "developer_instructions"):
            require(isinstance(data.get(key), str) and data[key].strip(), f"{filename}: missing {key}")

        require(data["name"] == expected_name, f"{filename}: unexpected name {data['name']!r}")
        require(data.get("model") == expected_model, f"{filename}: unexpected model")
        require(data.get("model_reasoning_effort") == "max", f"{filename}: effort must be max")
        require(data.get("sandbox_mode") == expected_sandbox, f"{filename}: unexpected sandbox")
        require(data["name"] not in seen_names, f"duplicate Agent name: {data['name']}")
        seen_names.add(data["name"])

        instructions = data["developer_instructions"]
        require("Do not spawn subagents" in instructions, f"{filename}: missing descendant ban")
        require("Do not commit, push" in instructions, f"{filename}: missing delivery boundary")

    require(len(seen_names) == len(EXPECTED), "Agent count mismatch")


def validate_special_rules(agent_dir: Path) -> None:
    ordinary = read_text(agent_dir / "runtime_investigator.toml")
    require("one investigation pass" in ordinary, "runtime investigator must stop after one pass")
    require("return INCONCLUSIVE directly to the parent" in ordinary, "runtime investigator escalation rule missing")

    deep = read_text(agent_dir / "runtime_investigator_deep.toml")
    require("cross-system" in deep and "contradictory" in deep, "deep investigator gate missing")
    require("not a fallback" in deep, "deep investigator fallback ban missing")

    bounded = read_text(agent_dir / "bounded_executor.toml")
    require("open-ended discovery" in bounded, "bounded executor discovery stop rule missing")
    require("parent requests a checkpoint" in bounded, "bounded executor checkpoint rule missing")
    require("Continue afterward unless the parent records an allowed cancellation reason" in bounded, "bounded executor non-terminal checkpoint rule missing")

    contracts = read_text(SKILL_DIR / "references" / "contracts.md")
    require("## Checkpoint request" in contracts, "checkpoint result contract missing")
    for field in ("`Phase`", "`Evidence`", "`Changes`", "`Blocker`", "`Next`"):
        require(field in contracts, f"checkpoint field missing: {field}")
    require("No file change does not mean no usable result" in contracts, "partial-result audit rule missing")
    require("`INTERRUPTED` is an orchestration event" in contracts, "interruption state boundary missing")
    require("allowed cancellation reason defined by the Skill" in contracts, "checkpoint continuation boundary missing")

    evaluation = read_text(SKILL_DIR / "references" / "evaluation.md")
    require("## Liveness and interruption regressions" in evaluation, "liveness regression matrix missing")
    require("ten successful read-only checks" in evaluation, "no-file liveness regression missing")
    require("partial-result audit" in evaluation, "suspected-hang audit regression missing")
    require("keep the child intact" in evaluation, "suspected-hang preservation regression missing")
    require("do not interrupt, retry, or take over merely because it is silent" in evaluation, "suspected-hang fail-closed regression missing")
    require("A manually interrupted child is never retried automatically" in evaluation, "interrupted retry regression missing")


def main() -> int:
    agent_dir = locate_agent_dir()
    validate_skill()
    validate_agents(agent_dir)
    validate_special_rules(agent_dir)
    print(f"[OK] skill={SKILL_DIR}")
    print(f"[OK] agents={len(EXPECTED)} directory={agent_dir}")
    print("[OK] implicit routing, exact models, max effort, sandbox defaults, runtime, and liveness gates validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
