<p align="right">
  <a href="./README.md">简体中文</a> · <strong>English</strong>
</p>

<p align="center">
  <img src="./assets/readme/hero-en.svg" width="100%" alt="Sol Explore Relay delegates only bounded read-only exploration to four Explorers while parent Sol keeps every implementation and delivery task">
</p>

<p align="center">
  <strong>Send out the search context. Keep implementation quality in the main session.</strong><br>
  Parent Sol delegates only bounded read-only exploration, then plans, edits, reviews, verifies, and delivers the work itself.
</p>

<p align="center">
  <a href="#what-it-solves">Core boundary</a> ·
  <a href="#routing-board">Routing board</a> ·
  <a href="#install-into-a-project">Install</a> ·
  <a href="#verification">Verify</a>
</p>

## What it solves

Complex implementation often begins with a large amount of code, official documentation, or runtime evidence. Keeping all of it in the parent session crowds out the context needed for design, editing, and verification. Delegating implementation as well introduces interface drift, shared-file conflicts, and a second acceptance burden.

`sol-explore-relay` removes only the first cost:

- all 4 profiles are read-only Explorers;
- there are 0 Executors, Fixers, Reviewers, Integrators, or `default` catch-alls;
- children return compressed evidence maps, and parent Sol rechecks only decision-critical slices;
- every mutation, implementation choice, check interpretation, and completion claim remains parent-owned.

> This relay assumes a Sol parent session. It does not create another Coordinator or hand the user conversation to a child.

## Routing board

<p align="center">
  <img src="./assets/readme/routing-board-en.svg" width="100%" alt="Parent Sol decides whether exploration is worth delegating, four read-only Explorers return evidence, and the parent then plans, edits, verifies, and delivers">
</p>

| Evidence question | Agent | Model | Stop boundary |
| --- | --- | --- | --- |
| Repository ownership, symbols, call paths, dependencies, data flow, or blast radius | `sol_explore_code` | Luna Max | Cited file and line evidence is sufficient, or scope must expand |
| Current official docs, APIs, version behavior, standards, or upstream facts | `sol_explore_docs` | Luna Max | Primary sources answer the question, or materially conflict |
| One log, trace, test failure, process state, or runtime hypothesis | `sol_explore_runtime` | Luna Max | One pass concludes, or returns `INCONCLUSIVE` directly |
| Evidence is cross-system or materially contradictory at dispatch time | `sol_explore_runtime_deep` | Terra Max | Named systems reconcile, or a precise missing-evidence boundary is reached |

Deep Runtime is not an automatic upgrade from ordinary Runtime. An inconclusive ordinary pass returns to parent Sol instead of being rerun through another Agent.

## One complete flow

1. Parent Sol decides whether isolated exploration saves more context than dispatch costs.
2. The parent freezes the question, sources, read boundary, allowed checks, stop condition, and return format.
3. One or more Explorers investigate in isolated context, with at most 3 independent questions in parallel.
4. Each Explorer returns a direct answer, exact evidence, conflicts, unknowns, and the smallest next step; it changes no files.
5. Parent Sol rechecks decision-critical evidence, then plans, edits, runs completion checks, inspects the real diff, and delivers.

Small, obvious one-step lookups stay direct. Dispatch is not a mandatory pipeline and cannot become a reason to postpone implementation.

## Install into a project

There are only two installation surfaces:

```text
<target-project>/
├── .codex/agents/sol_explore_*.toml
└── .agents/skills/sol-explore-relay/**
```

The four Agents use a unique `sol_explore_*` prefix so they remain distinct from other Relay profiles. This PowerShell example stops on a same-name source instead of silently overwriting it:

```powershell
$relaySource = "D:\path\to\codex-relay\sol-explore-relay"
$targetProject = "D:\path\to\target-project"
$agentTarget = Join-Path $targetProject ".codex\agents"
$skillTarget = Join-Path $targetProject ".agents\skills\sol-explore-relay"

$profileNames = Get-ChildItem (Join-Path $relaySource "agents\*.toml") |
    Select-Object -ExpandProperty Name
$conflicts = $profileNames |
    Where-Object { Test-Path (Join-Path $agentTarget $_) }
if ($conflicts -or (Test-Path $skillTarget)) {
    throw "A same-name Agent or Skill already exists; confirm its source first: $($conflicts -join ', ')"
}

New-Item -ItemType Directory -Force $agentTarget, $skillTarget | Out-Null
Copy-Item (Join-Path $relaySource "agents\*.toml") $agentTarget
Copy-Item (Join-Path $relaySource "skills\sol-explore-relay\*") $skillTarget -Recurse
```

If the target project already has a Skill installer or Junction convention, wire `skills/sol-explore-relay` into that flow as the single canonical source.

## Verification

Run from this package root:

```powershell
python -X utf8 skills\sol-explore-relay\scripts\validate_sol_explore_relay.py
```

The validator checks exactly 4 profiles, unique names, models, `max` reasoning effort, `read-only` sandbox defaults, implicit Skill invocation, Explore-only routing, dispatch contracts, and parent-owned implementation.

Parsing configuration does not prove runtime discovery. After installation, start a new Codex task and inspect the Agents actually discovered, including model, reasoning effort, effective sandbox and approval policy, and visible tools. If read-only isolation is an acceptance requirement, use only a disposable fixture inside the target project for mutation probes. Record any successful Explorer write as `NOT_ENFORCED`.

## Package map

```text
sol-explore-relay/
├── agents/                              # 4 uniquely named read-only Explorers
│   ├── sol_explore_code.toml
│   ├── sol_explore_docs.toml
│   ├── sol_explore_runtime.toml
│   └── sol_explore_runtime_deep.toml
├── skills/sol-explore-relay/
│   ├── SKILL.md                         # Activation, routing, concurrency, parent boundary
│   ├── agents/openai.yaml               # UI metadata and implicit invocation
│   ├── references/                      # Dispatch, routing, and evaluation contracts
│   └── scripts/                         # Static validator
├── assets/readme/                       # Bilingual editable pure SVG
├── README.en.md
└── README.md
```

## Design boundary

| Explorers may | Only parent Sol may |
| --- | --- |
| Trace repository facts within named read sources | Decide requirements, architecture, interfaces, permissions, and scope |
| Verify current primary documentation and version facts | Choose an implementation and modify any file |
| Analyze existing logs, traces, and runtime evidence | Run or interpret completion checks, review the diff, and accept risk |
| Return precise citations, conflicts, and unknowns | Mutate Git, create build artifacts, publish, write externally, communicate with the user, and deliver |

The complete behavior is in [`SKILL.md`](./skills/sol-explore-relay/SKILL.md), with detailed contracts in [`contracts.md`](./skills/sol-explore-relay/references/contracts.md), [`routing.md`](./skills/sol-explore-relay/references/routing.md), and [`evaluation.md`](./skills/sol-explore-relay/references/evaluation.md).
