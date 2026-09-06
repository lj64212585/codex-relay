from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = SKILL_DIR.parent.parent
SKILL_NAME = "explore-relay"

EXPECTED = {
    "explore_code.toml": ("explore_code", "gpt-5.6-luna", "read-only"),
    "explore_docs.toml": ("explore_docs", "gpt-5.6-luna", "read-only"),
    "explore_runtime.toml": ("explore_runtime", "gpt-5.6-luna", "read-only"),
    "explore_runtime_deep.toml": ("explore_runtime_deep", "gpt-5.6-terra", "read-only"),
}

REQUIRED_REFERENCES = {
    "references/contracts.md",
    "references/routing.md",
    "references/evaluation.md",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_text(path: Path) -> str:
    require(path.is_file(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def locate_agent_dir() -> Path:
    source = PACKAGE_ROOT / "agents"
    if PACKAGE_ROOT.name not in (".codex", ".agents") and source.is_dir():
        return source
    installed = SKILL_DIR.parents[2] / ".codex" / "agents"
    require(installed.is_dir(), "unable to locate source agents/ or installed project .codex/agents/")
    return installed


def validate_skill() -> None:
    text = read_text(SKILL_DIR / "SKILL.md")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    require(frontmatter is not None, "SKILL.md must start with YAML frontmatter")
    fields = frontmatter.group(1)
    require(re.search(rf"^name: {re.escape(SKILL_NAME)}$", fields, re.MULTILINE) is not None, "unexpected skill name")
    require(re.search(r"^description: *\S.*$", fields, re.MULTILINE) is not None, "missing skill description")
    require(len(text.encode("utf-8")) <= 16000, "SKILL.md exceeds package size budget")
    require(len(text.splitlines()) <= 190, "SKILL.md exceeds package line budget")

    # Check actual table references, not prescriptive prose or exact sentence wording.
    routes = re.findall(r"^\|[^\n]*?`([a-z_]+)`[^\n]*\|$", text, re.MULTILINE)
    expected_names = {row[0] for row in EXPECTED.values()}
    require(set(routes) == expected_names and len(routes) == len(expected_names), "route table must reference each configured profile exactly once")

    links = set(re.findall(r"\[[^\]]*\]\(([^)]+)\)", text))
    require(REQUIRED_REFERENCES <= links, "required references must be linked from SKILL.md")
    for path in [SKILL_DIR / "SKILL.md", *(SKILL_DIR / name for name in sorted(REQUIRED_REFERENCES))]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", read_text(path)):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            require((path.parent / relative).is_file(), f"broken local reference in {path.name}: {target}")

    metadata = read_text(SKILL_DIR / "agents" / "openai.yaml")
    require(re.search(r"^  allow_implicit_invocation: true$", metadata, re.MULTILINE) is not None, "implicit invocation is not enabled")
    require("allow_implicit_invocation: false" not in metadata, "conflicting invocation policy")
    require(f"${SKILL_NAME}" in metadata, "default prompt must reference this skill")


def validate_agents(agent_dir: Path) -> None:
    if PACKAGE_ROOT.name not in (".codex", ".agents") and agent_dir == PACKAGE_ROOT / "agents":
        require({path.name for path in agent_dir.glob("*.toml")} == set(EXPECTED), "unexpected source profile set")
    require(not (agent_dir / "default.toml").exists(), "default.toml must not be installed")
    seen: set[str] = set()
    for filename, (name, model, sandbox) in EXPECTED.items():
        data = tomllib.loads(read_text(agent_dir / filename))
        for key in ("name", "description", "developer_instructions"):
            require(isinstance(data.get(key), str) and bool(data[key].strip()), f"{filename}: missing {key}")
        require(data["name"] == name, f"{filename}: unexpected name")
        require(name not in seen, f"duplicate profile name: {name}")
        seen.add(name)
        require(data.get("model") == model, f"{filename}: unexpected model")
        require(data.get("model_reasoning_effort") == "max", f"{filename}: effort must be max")
        require(data.get("sandbox_mode") == sandbox, f"{filename}: unexpected sandbox")


def main() -> int:
    try:
        agent_dir = locate_agent_dir()
        validate_skill()
        validate_agents(agent_dir)
    except (ValueError, OSError) as error:
        print(f"[FAIL] {error}")
        return 1
    print(f"[OK] skill={SKILL_DIR}")
    print(f"[OK] agents={len(EXPECTED)} directory={agent_dir}")
    print("[OK] profile configuration, route references, local links, and invocation metadata")
    print("[NOTE] static validation does not prove behavior, runtime discovery, or sandbox enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
