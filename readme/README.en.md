<p align="right">
  <a href="../README.md">简体中文</a> · <strong>English</strong>
</p>

<p align="center">
  <img src="./assets/hero-en.svg" width="100%" alt="Codex Relay: choose between cost-first and Sol-controlled multi-agent routing">
</p>

<p align="center">
  <strong>Two routing philosophies. One clear set of boundaries.</strong><br>
  Choose progressive, cost-aware escalation or dedicated lanes controlled by parent Sol for complex Codex work.
</p>

<p align="center">
  <a href="#choose-your-relay">Choose a Relay</a> ·
  <a href="#quick-verification">Quick verification</a> ·
  <a href="#shared-principles">Shared principles</a> ·
  <a href="#repository-map">Repository map</a>
</p>

## Choose your Relay

`codex-relay` contains two Codex multi-agent routing packages with different tradeoffs. Both are built from a Skill and custom Agent profiles, with no new Runner or resident service. The choice is whether you most need to protect **model cost** or **parent authority and execution boundaries**.

| | [Poor Relay](../poor-relay/README.en.md) | [Sol-led Relay](../sol-led-relay/README.en.md) |
| --- | --- | --- |
| Primary goal | Let Luna carry the bulk of the work and escalate only when risk or value justifies it | Keep decision, integration, and delivery authority with parent Sol |
| Control model | A Coordinator chooses the shortest sufficient routing path | Parent Sol sends bounded work through dedicated lanes |
| Agent shape | 5 profiles: Luna workers, Terra review, Sol on demand | 9 profiles: Explore ×4, Execute ×3, Review ×2 |
| Installation | Windows PowerShell scripts; installs for the current user by default | Install Agents and the Skill into the target project's `.codex/` and `.agents/` |
| Best fit | Everyday project work, budget sensitivity, less high-cost reasoning | Complex projects, role isolation, evidence handoffs, and parent control |

### Poor Relay — cost first

Luna handles context-heavy investigation, routine implementation, and self-checks. Terra reviews only when automated evidence cannot cover a blocking risk, while Sol is reserved for multi-step planning, failed-task escalation, and final technical integration.

**Read the complete guide: [poor-relay/README.en.md](../poor-relay/README.en.md)**

### Sol-led Relay — control first

Parent Sol remains responsible for requirements, architecture, shared-file coordination, result acceptance, and final delivery. Explorers, Executors, and Reviewers receive only packets with explicit sources, scope, checks, and stop conditions.

**Read the complete guide: [sol-led-relay/README.en.md](../sol-led-relay/README.en.md)**

## Quick verification

Verify the source package you intend to use, then follow its README for installation.

<details>
<summary><strong>Verify Poor Relay</strong></summary>

```powershell
Push-Location .\poor-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>Verify Sol-led Relay</strong></summary>

```powershell
Push-Location .\sol-led-relay
python -X utf8 skills\sol-led-relay\scripts\validate_sol_led_relay.py
Pop-Location
```

</details>

> Static validation proves only that the package configuration and contracts are internally consistent. After installation, start a new Codex task and inspect the Agents actually discovered, including model, reasoning effort, sandbox, approval policy, and visible tools. Verify permission isolation with a disposable fixture inside the target project.

## Shared principles

- **Delegation must earn its cost:** small, obvious, one-step tasks stay in the parent session.
- **Every write has an owner:** an Executor modifies only its assigned file slice; the parent coordinates shared boundaries.
- **Return evidence, not authority:** subagents provide files, diffs, checks, and risks; the parent decides whether to accept them.
- **Failure does not expand authority:** timeout, silence, insufficient evidence, or a failed check never grants an automatic retry, escalation, or takeover.
- **Repository governance still wins:** a Relay does not override user permissions, project rules, Git workflow, or explicit acceptance gates.

## Repository map

```text
codex-relay/
├── poor-relay/                     # Cost- and risk-aware 5-profile routing package
│   └── README.en.md                 # Installation, policy, verification, and license
├── sol-led-relay/                  # Parent-Sol-controlled 9-profile routing package
│   └── README.en.md                 # Routing, contracts, installation, and verification
└── readme/
    ├── README.en.md                # This English repository overview
    └── assets/                     # Local visuals for the repository overview
```

Continue with the complete guides: **[Poor Relay](../poor-relay/README.en.md)** · **[Sol-led Relay](../sol-led-relay/README.en.md)**
