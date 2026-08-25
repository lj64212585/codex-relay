<p align="right">
  <a href="./readme/README.zh-CN.md">简体中文</a> · <strong>English</strong>
</p>

<p align="center">
  <img src="./readme/assets/hero-en.svg" width="100%" alt="Codex Relay: choose cost-first routing, Explore-only parent implementation, a two-Sol fresh-context relay, or parent-Sol control across complete lanes">
</p>

<p align="center">
  <strong>Four routing philosophies. One clear set of boundaries.</strong><br>
  Choose cost-first delegation, outsource only exploration, relay planning into execution across two fresh Sol contexts, or let parent Sol control complete lanes.
</p>

<p align="center">
  <a href="#choose-your-relay">Choose a Relay</a> ·
  <a href="#relative-implementation-quality-and-cost-estimates">Comparison estimates</a> ·
  <a href="#use-relay-installer">Web installer</a> ·
  <a href="#quick-verification">Quick verification</a> ·
  <a href="#shared-principles">Shared principles</a> ·
  <a href="#repository-map">Repository map</a>
</p>

## Choose your Relay

`codex-relay` contains four independently installable Codex multi-agent routing packages. Each combines a Skill with custom Agent profiles and adds no new Runner or resident service. The real choice is which work may leave the parent session and what you most need to protect.

| Relay | Primary goal | Delegation surface | Best fit |
| --- | --- | --- | --- |
| [Poor Relay](./relay/poor-relay/README.en.md) | Let Luna carry most work and escalate only when risk or value justifies it | Cost-tiered planning, exploration, execution, review, and integration | Everyday work, budget sensitivity, less high-cost reasoning |
| [Sol Explore Relay](./relay/sol-explore-relay/README.en.md) | Save search context while parent Sol implements the task itself | **Only 4 read-only Explore profiles** | Quality-sensitive work, shared files, avoiding implementation handoffs |
| [Sol Pair Relay](./relay/sol-pair-relay/README.en.md) | Give separate Sol agents clean planning and execution contexts | Luna Max explores, one Sol Max plans, a second Sol Max executes and accepts | Luna / Terra parent conversations, implementation quality, temporary plans that prevent drift |
| [Sol-led Relay](./relay/sol-led-relay/README.en.md) | Keep decision, integration, and delivery authority with parent Sol | Explore ×4, Execute ×3, Review ×2 | Complex projects with bounded slices and independent review |

## Relative implementation quality and cost estimates

The following figures are relative estimates for the **same medium-to-high-complexity engineering task**. A single Sol completing exploration, implementation, checks, and acceptance in one parent session is set to `100%`. Task implementation quality is a relative index rather than an absolute success rate, so it may exceed `100%`; implementation cost measures total model reasoning consumption across all participating Agents and excludes human, device, release, or external-system acceptance costs.

| Routing strategy | Task implementation quality | Implementation cost | Basis for the estimate |
| --- | ---: | ---: | --- |
| Single Sol working alone | **100%** | **100%** | Baseline; no handoff loss and no review gain from an independent context |
| [Poor Relay](./relay/poor-relay/README.en.md) | ${\color[RGB]{154,103,0}\mathbf{95\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{45\\%}}$ | Luna handles exploration and routine implementation while Terra and Sol enter only for risk, planning, or integration; it has the lowest cost, with some subtle implementation quality and global consistency traded for budget |
| [Sol Explore Relay](./relay/sol-explore-relay/README.en.md) | ${\color[RGB]{26,127,55}\mathbf{110\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{90\\%}}$ | Luna / Terra isolates noisy exploration while parent Sol retains full implementation authority; less context pollution buys a quality gain for modest dispatch and recheck overhead |
| [Sol Pair Relay](./relay/sol-pair-relay/README.en.md) | ${\color[RGB]{26,127,55}\mathbf{120\\%}}$ | ${\color[RGB]{207,34,46}\mathbf{180\\%}}$ | Two fresh Sol Max agents separately plan and execute with acceptance, giving the highest quality ceiling; duplicated understanding, plan handoff, and two Sol reasoning passes also make it the most expensive |
| [Sol-led Relay](./relay/sol-led-relay/README.en.md) | ${\color[RGB]{26,127,55}\mathbf{115\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{85\\%}}$ | Parent Sol keeps decisions and integration, Luna executes bounded slices, and Terra reviews independently; despite multi-role coordination overhead, it balances high quality with lower cost |

> These figures compare routing priorities; they are not measured benchmarks. One-step tasks usually cannot amortize dispatch cost. As task complexity and exploration noise increase—and slice boundaries become clearer—the relative benefit of each Relay is more likely to approach the estimate above.
>
> You can adjust each profile's model reasoning strength (`model_reasoning_effort`) within every routing strategy to match your task complexity, quality target, and budget. The table assumes the repository defaults; changing those settings will also change the quality and cost estimates.

### Poor Relay — cost first

Luna handles context-heavy investigation, routine implementation, and self-checks. Terra reviews only when automated evidence cannot cover a blocking risk, while Sol keeps multi-step planning, failed-task escalation, and final technical integration.

**Complete guide: [relay/poor-relay/README.en.md](./relay/poor-relay/README.en.md)**

### Sol Explore Relay — outsource only exploration

Four read-only Explorers trace the repository, verify official sources, investigate one runtime question, or reconcile contradictory cross-system evidence. Parent Sol rechecks critical slices, then plans, edits, tests, reviews the real diff, and delivers. There are no delegated writers or reviewers.

**Complete guide: [relay/sol-explore-relay/README.en.md](./relay/sol-explore-relay/README.en.md)**

### Sol Pair Relay — two fresh Sol contexts

Luna or Terra keeps the parent conversation while Luna Max compresses optional exploration evidence. One fresh Sol Max writes only a temporary `plan.md`; a different fresh Sol Max follows it, runs checks, inspects the real diff, and performs technical acceptance. The two Sol agents share no long transcript—only the approved plan and minimal decision-critical evidence.

**Complete guide: [relay/sol-pair-relay/README.en.md](./relay/sol-pair-relay/README.en.md)**

### Sol-led Relay — controlled lanes

Parent Sol owns requirements, architecture, shared-file coordination, result acceptance, and final delivery while bounded packets with explicit sources, scope, checks, and stop conditions move through Explorer, Executor, and Reviewer lanes.

**Complete guide: [relay/sol-led-relay/README.en.md](./relay/sol-led-relay/README.en.md)**

## Use Relay Installer

If you prefer not to copy Skill and Agent files by hand, start the configuration-driven local web installer from the repository root. It requires Python 3.11 or later, listens only on `127.0.0.1`, defaults to English, and provides an English/Chinese switch plus light and dark themes.

```powershell
.\tools\relay-installer\start.ps1
```

After the page opens:

1. Under **Installation scope**, choose **Global** or **Project**. Global affects only the current Windows user. In Project mode, enter the target root or select it with **Browse**.
2. Choose one **Relay type**. Each horizontal option shows its task implementation quality and implementation cost estimates; use the **Details** button on the left to open the Relay README for the current UI language.
3. Select **Check and install**. The installer preflights the target first. If another Relay is present, it explains that competing implicit-routing rules can conflict, then waits for confirmation before backing up and removing recognized old routing files and completing the install.
4. To clean the active target, use the red **Remove Relay files from this directory** button at the bottom of Installation scope. The confirmation dialog lists the affected Relay and paths before anything is changed.

> The installer touches only Skill directories and Agent files that can be attributed to its configuration; unknown custom files are not deleted. Before switching or removing a Relay, it stores recoverable content under `.relay-installer-backups` in the target root.

<details>
<summary><strong>Configuration check and executable packaging</strong></summary>

Validate the configuration and every Relay source file without installing:

```powershell
py -3 -B .\tools\relay-installer\relay_installer.py --check
```

After installing 64-bit Python 3.11+ and the build dependencies, use the repository packaging entry point to build one Win64 desktop executable containing all four Relays. Double-clicking the result opens only the Relay Installer window, without a console or external browser:

```powershell
python -m pip install -r .\tools\relay-installer\requirements-build.txt
.\packaging\build-win64.bat
```

The BAT reads its version from the Git-ignored `packaging/version.txt`, then validates the desktop entry point, bundled content, embedded version, and Windows version metadata. It writes `packaging/out/win64/relay-installer-v<version>.exe`; the window title and Windows file properties both expose that version. The desktop window uses the system Microsoft Edge WebView2 Runtime. See the **[Relay Installer reference (Chinese)](./tools/relay-installer/README.md)** for the version format, configuration fields, path boundaries, and advanced packaging options.

</details>

## Quick verification

Verify the source package you intend to use, then follow its README to install it. All four Skills support implicit invocation, so choose one governing strategy per task domain rather than letting overlapping rules compete for the same route.

<details>
<summary><strong>Verify Poor Relay</strong></summary>

```powershell
Push-Location .\relay\poor-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>Verify Sol Explore Relay</strong></summary>

```powershell
Push-Location .\relay\sol-explore-relay
python -X utf8 skills\sol-explore-relay\scripts\validate_sol_explore_relay.py
Pop-Location
```

</details>

<details>
<summary><strong>Verify Sol Pair Relay</strong></summary>

```powershell
Push-Location .\relay\sol-pair-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>Verify Sol-led Relay</strong></summary>

```powershell
Push-Location .\relay\sol-led-relay
python -X utf8 skills\sol-led-relay\scripts\validate_sol_led_relay.py
Pop-Location
```

</details>

> Static validation proves only package consistency. After installation, start a new Codex task and inspect the Agents actually discovered, including model, reasoning effort, effective sandbox and approval policy, and visible tools. Verify claimed read-only isolation with a disposable fixture inside the target project.

## Shared principles

- **Delegation must earn its cost:** small, obvious, one-step tasks stay in the parent session.
- **Activate only the chosen boundary:** cost tiers, Explore-only routing, the two-Sol relay, and full-lane routing are distinct strategies and should not govern the same task domain together.
- **Return evidence, not authority:** children provide files, lines, sources, checks, and risks; the parent decides whether to accept them.
- **Every write has an explicit owner:** Sol Explore Relay reserves writes for the parent; other Relays still name an owner for every writable slice.
- **Context isolation must be real:** Sol Pair Relay requires different Planner and Executor Agents, with temporary `plan.md` as their only durable handoff.
- **Failure does not expand authority:** timeout, silence, insufficient evidence, or a failed check never grants an automatic retry, escalation, or takeover.
- **Repository governance still wins:** a Relay does not override user permissions, project rules, Git workflow, or explicit acceptance gates.

## Repository map

```text
codex-relay/
├── relay/
│   ├── poor-relay/                 # Cost- and risk-aware 5-profile routing package
│   ├── sol-explore-relay/          # Explore-only, parent-implemented 4-profile package
│   ├── sol-pair-relay/             # Luna / Terra parent, two-Sol relay, 3-profile package
│   └── sol-led-relay/              # Parent-Sol-controlled 9-profile, three-lane package
├── packaging/
│   ├── build-win64.bat             # One-file Win64 build and bundled-content check
│   ├── version.txt                 # Git-ignored local version source
│   └── out/win64/                  # Git-ignored generated output
├── tools/
│   └── relay-installer/            # Desktop/web UI, install, switch, removal, and packaging
├── README.md                       # English repository overview
└── readme/
    ├── README.zh-CN.md             # Simplified Chinese repository overview
    └── assets/                     # Local visuals for the repository overview
```

Continue with the complete guides: **[Poor Relay](./relay/poor-relay/README.en.md)** · **[Sol Explore Relay](./relay/sol-explore-relay/README.en.md)** · **[Sol Pair Relay](./relay/sol-pair-relay/README.en.md)** · **[Sol-led Relay](./relay/sol-led-relay/README.en.md)**
