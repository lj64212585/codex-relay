# Codex Relay

[English](./README.md) · [简体中文](./readme/README.zh-CN.md)

![Codex Relay](./readme/assets/hero-en.svg)

**Route by responsibility. Choose by task.**

Use Explore by default so the parent continuously understands, implements, and verifies. Choose the other modes for settled implementation delegation, targeted review, or budget priority. Skill and Agent names describe responsibilities; configuration selects models.

| Mode | Best fit | Implementation and context | Main risk |
|---|---|---|---|
| [Explore Relay](./relay/explore-relay/README.en.md) | Default; quality-sensitive, core interaction, complex implementation | Parent implements; four read-only evidence roles | Missing or stale evidence; parent must understand the core path |
| [Implementation Relay](./relay/implementation-relay/README.en.md) | Settled implementation slices or targeted independent review | Parent owns core work; 4 explorers, 3 writers, 2 reviewers | Small scope can hide difficult judgment; require low implementation uncertainty |
| [Budget Relay](./relay/budget-relay/README.en.md) | Budget priority, settled behavior and boundaries | Bounded execution, risk review, technical integration | A plan cannot transfer all implementation judgment; route uncertainty early |

Astra is the recommended parent; a Skill does not switch the parent model. Explore keeps three Luna Max and one Terra Max roles. Implementation keeps six Luna Max and three Terra Max roles; the parent retains core implementation. Budget uses `gpt-6-astra` xHigh for planning and integration; its other Luna/Terra settings are unchanged. Model upgrades do not require role renames.

## Working rules

Dispatch includes fixed constraints, decision context, budget, and stop conditions. Reports include Coverage and Snapshot; a scoped negative finding does not prove absence. The parent reads critical call paths without repeating broad searches. One timeout is not failure; budget exhaustion, sufficient evidence, or obsolete work can end delegation with a recorded reason. Confirm stopped state before resource reuse, and audit changes before transferring write ownership. Use matching runtime, visual, or interaction evidence and avoid repeating unaffected passing checks.

## Installation and migration

```powershell
.\tools\relay-installer\start.ps1
```

Rename `sol-explore-relay` to `explore-relay`, `sol-led-relay` to `implementation-relay`, and `poor-relay` to `budget-relay`. `sol-pair-relay` and its interim name `plan-execute-relay` are removed. Explorer IDs use `explore_*`; Implementation and Budget retain their existing responsibility-based Agent IDs.

Source renames do not remove installed copies. Use installer preflight and confirmed switching: recognized legacy files are backed up; custom files block automatic operations. Old names remain only for migration recognition and historical copyright attribution, not callable aliases. Use one governing mode per task domain. Select Implementation only for settled slices or a precise review benefit; existing implicit discovery settings are preserved.

[Installer configuration, backup, and Win64 packaging](./tools/relay-installer/README.md)

```powershell
.\packaging\build-win64.bat
```

## Verification

```powershell
python -X utf8 relay/explore-relay/skills/explore-relay/scripts/validate_explore_relay.py
python -X utf8 relay/implementation-relay/skills/implementation-relay/scripts/validate_implementation_relay.py
python -X utf8 relay/budget-relay/skills/budget-relay/scripts/validate_budget_relay.py
python tools/relay-installer/relay_installer.py --check
Push-Location tools/relay-installer
python -m unittest discover -s tests
Pop-Location
```

Static checks establish package and installer consistency, not fresh-task Agent discovery, effective permission isolation, or quality/cost gains. Compare direct Astra, previous Explore with Astra, and revised Explore with Astra at the same starting state, tools, and acceptance gates. Record defects, human interventions, all-agent consumption, and elapsed time. No unmeasured quality or cost percentages are presented.

## Repository map

```text
relay/explore-relay/       # Parent implementation + evidence
relay/implementation-relay/  # Settled slices + targeted risk review
relay/budget-relay/        # Budget-oriented bounded implementation
tools/relay-installer/     # Install, switch, backup, rollback
packaging/                # Win64 build
readme/                   # Chinese overview and SVG assets
```
