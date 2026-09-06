# Codex Relay

[English](./README.md) · [简体中文](./readme/README.zh-CN.md)

<p align="center">
  <img src="./readme/assets/hero-en.svg" width="100%" alt="Codex Relay: the parent owns the critical path through exploration, implementation, and verification">
</p>

**Agent delegation for Codex, with critical understanding, implementation, and acceptance owned by the parent.**

This repository provides three installable sets of Skills and Agent profiles. Start with **Explore Relay**; choose another mode for settled implementation slices, targeted review, or budget priority. Responsibility names stay stable; configuration selects models.

[Choose a mode](#choose-a-mode) · [Quick start](#quick-start) · [Working agreements](#working-agreements) · [Verification](#verification)

## Choose a mode

| Mode | Task and responsibility |
| :--- | :--- |
| **[Explore Relay](./relay/explore-relay/README.en.md)** | **Default for complex work.** Parent implements; 4 read-only roles gather evidence. |
| **[Implementation Relay](./relay/implementation-relay/README.en.md)** | **Settled slices or targeted review.** Parent owns core work; 4 explorers, 3 writers, 2 reviewers. |
| **[Budget Relay](./relay/budget-relay/README.en.md)** | **Budget priority, settled boundaries.** Bounded execution, risk review, technical integration. |

> **Choose by implementation uncertainty.** Small scope can still require difficult judgment. Explore needs parent verification of critical evidence; Implementation needs settled behavior; Budget should escalate uncertainty early.

## Quick start

On Windows with **Python 3.11+**, start the installer from the repository root:

```powershell
.\tools\relay-installer\start.ps1
```

Choose the installation scope and Relay, inspect preflight results, then install. Use one governing mode per task domain. When switching, the installer backs up recognized legacy files; custom-file conflicts block automatic operations.

[Installer configuration, backup, and rollback](./tools/relay-installer/README.md)

<details>
<summary>Migrate from an older version</summary>

Rename `sol-explore-relay` to `explore-relay`, `sol-led-relay` to `implementation-relay`, and `poor-relay` to `budget-relay`. `sol-pair-relay` and its interim name `plan-execute-relay` are removed. Explorer IDs use `explore_*`; Implementation and Budget retain their existing responsibility-based Agent IDs.

Source renames do not remove installed copies. Use installer preflight and confirmed switching: recognized legacy files are backed up; custom files block automatic operations. Old names remain only for migration recognition and historical copyright attribution, not callable aliases. Use one governing mode per task domain. Select Implementation only for settled slices or a precise review benefit; existing implicit discovery settings are preserved.

</details>

<details>
<summary>Build the Win64 installer</summary>

```powershell
.\packaging\build-win64.bat
```

[Installer configuration, backup, and rollback](./tools/relay-installer/README.md)

</details>

## Working agreements

1. **Set boundaries before dispatch.** Include fixed constraints, decision context, budget, and stop conditions.
2. **Connect contexts with evidence.** Reports include Coverage and Snapshot; a scoped negative finding does not prove absence. The parent reads critical call paths without repeating broad searches.
3. **Confirm stop before handoff.** One timeout is not failure. Budget exhaustion, sufficient evidence, or obsolete work can end delegation with a recorded reason. Confirm stopped state and audit changes before resource reuse or write-ownership transfer.
4. **Match verification to the change.** Use appropriate runtime, visual, or interaction evidence; avoid repeating unaffected passing checks.

<details>
<summary>Model configuration and the parent session</summary>

Astra is the recommended parent; a Skill does not switch the parent model. Explore keeps three Luna Max and one Terra Max roles. Implementation keeps six Luna Max and three Terra Max roles; the parent retains core implementation. Budget uses `gpt-6-astra` xHigh for planning and integration; its other Luna/Terra settings are unchanged. Model upgrades do not require role renames.

</details>

## Verification

Static checks establish package and installer consistency, not fresh-task Agent discovery, effective permission isolation, or quality/cost gains. Compare direct Astra, previous Explore with Astra, and revised Explore with Astra at the same starting state, tools, and acceptance gates. Record defects, human interventions, all-agent consumption, and elapsed time. No unmeasured quality or cost percentages are presented.

<details>
<summary>Run package and installer checks</summary>

```powershell
python -X utf8 relay/explore-relay/skills/explore-relay/scripts/validate_explore_relay.py
python -X utf8 relay/implementation-relay/skills/implementation-relay/scripts/validate_implementation_relay.py
python -X utf8 relay/budget-relay/skills/budget-relay/scripts/validate_budget_relay.py
python tools/relay-installer/relay_installer.py --check
Push-Location tools/relay-installer
python -m unittest discover -s tests
Pop-Location
```

</details>

## Explore the repository

| Entry | Contents |
| :--- | :--- |
| [Relay packages](./relay/) | Mode guides, Skills, and Agent profiles |
| [Installer](./tools/relay-installer/) | Install, switch, backup, rollback |
| [Win64 packaging](./packaging/) | Desktop installer build entry point |

[MIT License](./LICENSE)
