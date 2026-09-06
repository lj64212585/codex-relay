> Expanded mode: the parent (Astra recommended) retains core implementation. Delegate only settled, independently checkable slices with low remaining judgment. Work requiring continuing state, persistence, concurrency, security, or core interaction judgment stays with the parent. Review findings cover the named risk, not global acceptance. Short handoffs carry relevant constraints and any real budget; reports identify coverage and source freshness. Record cancellation reasons and confirm stopped state before resource reuse or write-ownership transfer.

<p align="right">
  <a href="./README.md">简体中文</a> · <strong>English</strong>
</p>

<p align="center">
  <img src="./assets/readme/hero-en.svg" width="100%" alt="Implementation Relay: a Codex multi-agent routing package where the parent controls bounded work across Explore, Execute, and Review lanes">
</p>

<p align="center">
  <strong>Keep Astra in control. Let complex work move through clearly bounded circuits.</strong><br>
  A narrow-role multi-agent routing package for project-level Codex work: explore on demand, execute within frozen scope, review independently, and leave integration and delivery to the parent task.
</p>

## What it solves

Complex work benefits from delegation, but delegation should not dilute ownership. Implementation Relay assigns isolatable work to 9 specialized profiles while keeping requirement clarification, architecture decisions, shared-file coordination, final verification, and external delivery with the parent.

- **Delegate for real benefit**: start a subagent only when context isolation, parallel investigation, or independent review justifies the coordination cost; complete small and obvious tasks directly.
- **Route by boundary**: Explorers gather evidence, Executors write only inside frozen scope, and Reviewers inspect an actual diff or acceptance evidence.
- **Handoff by contract**: give the outcome, useful sources, ownership, and acceptance evidence; optional field labels are not required.
- **Recover from evidence**: timeouts and no diff yet do not prove failure. Continue scoped corrections while new evidence supports progress, and confirm termination before transferring ownership.

## Routing board

<p align="center">
  <img src="./assets/readme/routing-board-en.svg" width="100%" alt="Implementation Relay routing board: the parent sends bounded work to four Explorers, three Executors, or two Reviewers, then receives evidence and performs final validation and integration">
</p>

| Lane | Use it for | Profiles | Default permission |
| --- | --- | --- | --- |
| **Explore ×4** | Code paths, external documentation, one bounded runtime question, or a cross-system or contradictory investigation | `code_explorer` · `docs_researcher` · `runtime_investigator` · `runtime_investigator_deep` | read-only |
| **Execute ×3** | Exact mechanical edits, a minimal fix for a confirmed root cause, or a feature slice with frozen interfaces and acceptance criteria | `mechanical_executor` · `minimal_fixer` · `bounded_executor` | workspace-write |
| **Review ×2** | Correctness and regression review of a real implementation, or criterion-by-criterion acceptance-evidence review | `code_reviewer` · `verification_reviewer` | read-only |

Every profile uses `model_reasoning_effort = "max"`. `runtime_investigator_deep`, `code_reviewer`, and `verification_reviewer` use `gpt-5.6-terra`; all other profiles use `gpt-5.6-luna`.

> `runtime_investigator_deep` needs a concrete cross-system question or conflicting evidence, which may be newly discovered. An inconclusive result alone does not justify automatic escalation.

## One complete relay

1. **The parent decides whether delegation is useful**: unresolved product, architecture, security, permission, and cross-system decisions stay with the parent.
2. **Select the smallest role set**: parallelize within host capacity; concurrent writers require disjoint files, stable interfaces, and separate generated outputs and runtime resources.
3. **Send a bounded packet**: state the outcome, sources, scope, and acceptance evidence; children may not spawn descendants.
4. **Receive evidence, not decision authority**: the parent inspects the actual files, diff, artifacts, and validation output before accepting a result.
5. **Close the loop in the parent task**: integration, Git operations, builds, publishing, external writes, and the final response remain parent-owned.

## Install into a project

The standard installation surface has only two locations:

```text
<target-project>/
├── .codex/agents/*.toml
└── .codex/skills/implementation-relay/**
```

This PowerShell example stops when it finds an existing Agent or Skill with the same name. It does not overwrite files of unknown origin:

```powershell
$relaySource = "D:\path\to\codex-relay\relay\implementation-relay"
$targetProject = "D:\path\to\target-project"
$agentTarget = Join-Path $targetProject ".codex\agents"
$skillTarget = Join-Path $targetProject ".codex\skills\implementation-relay"

$profileNames = Get-ChildItem (Join-Path $relaySource "agents\*.toml") | Select-Object -ExpandProperty Name
$conflicts = $profileNames | Where-Object { Test-Path (Join-Path $agentTarget $_) }
if ($conflicts -or (Test-Path $skillTarget)) {
    throw "Found an existing Agent or Skill with the same name; verify its source first: $($conflicts -join ', ')"
}

New-Item -ItemType Directory -Force $agentTarget, $skillTarget | Out-Null
Copy-Item (Join-Path $relaySource "agents\*.toml") $agentTarget
Copy-Item (Join-Path $relaySource "skills\implementation-relay\*") $skillTarget -Recurse
```

If the target project already has a Skill installer or Junction convention, connect `skills/implementation-relay` as the single source directory. Do not create or overwrite another copy whose provenance is unclear.

## Verification

Run the static validator from the `implementation-relay` package root:

```powershell
python -X utf8 skills\implementation-relay\scripts\validate_implementation_relay.py
```

The validator checks the 9 profiles, exact models, `max` reasoning effort, sandbox defaults, implicit Skill invocation, route references, and local links. Instruction-following behavior is evaluated separately.

Valid configuration files do not prove that runtime discovery or isolation is effective. After installation, open a **new Codex task** and verify each discovered Agent name, model, reasoning effort, effective sandbox and approval policy, and visible tools. When permission isolation is an acceptance requirement, run mutation probes only against a disposable fixture inside the target project. If a read-only role can mutate it, record the result as `NOT_ENFORCED`.

## Package layout

```text
implementation-relay/
├── agents/                         # Install into target .codex/agents/
│   ├── code_explorer.toml
│   ├── docs_researcher.toml
│   ├── runtime_investigator*.toml
│   ├── *_executor.toml
│   └── *_reviewer.toml
├── skills/implementation-relay/           # Install into target .codex/skills/
│   ├── SKILL.md                    # Activation, routing, concurrency, failure boundaries
│   ├── agents/openai.yaml          # Display metadata and implicit invocation policy
│   ├── references/                 # Dispatch, routing, and evaluation contracts
│   └── scripts/                    # Static validator
├── README.en.md
└── README.md
```

There is no `default.toml`: the package does not let one broad default role absorb every task. `agents/` and the Skill are also distributed separately—the former declares runtime profiles; the latter decides when delegation is useful, how work is routed, and which authority must remain in the parent task.

## Design boundaries

| Subagents may | The parent retains |
| --- | --- |
| Investigate within named sources and scope | Requirement, product, architecture, security, and permission decisions |
| Modify one explicitly owned file slice | Shared-file coordination and cross-slice integration |
| Run assigned deterministic checks | Authority to accept or reject subagent results |
| Return evidence, risk, and the smallest next step | Git, remote builds, publishing, external writes, and final delivery |

Read the complete behavior contract in [`skills/implementation-relay/SKILL.md`](./skills/implementation-relay/SKILL.md). The detailed contracts live in [`contracts.md`](./skills/implementation-relay/references/contracts.md), [`routing.md`](./skills/implementation-relay/references/routing.md), and [`evaluation.md`](./skills/implementation-relay/references/evaluation.md).

Use the repository Relay Installer for existing-install migration, backup, and switching. Manual copy is for clean targets only.
