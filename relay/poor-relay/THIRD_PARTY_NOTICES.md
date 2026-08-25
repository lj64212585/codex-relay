# Third-party notices

Poor Relay is independently written, but its workflow design adapts selected
ideas from the MIT-licensed projects below. No upstream repository, complete
prompt library, persona catalog, command system, or full workflow is bundled.

## oil-oil/codex-team-mode

- Repository: https://github.com/oil-oil/codex-team-mode
- Copyright: Copyright (c) 2026 oil-oil
- License: MIT
- Relevant upstream files:
  - skills/team-mode/SKILL.md
  - agents/Explorer.toml
  - agents/Executor.toml
  - agents/Reviewer.toml
- Adapted ideas: smallest useful delegation, isolated child context, explicit
  dispatch packets, Explorer/Executor/Reviewer boundaries, fresh review context,
  bounded retries, and parent inspection of actual evidence.
- Not copied: default.toml, full onboarding, usage statistics, interactive test
  workflow, or the original profile prompts.

## wshobson/agents

- Repository: https://github.com/wshobson/agents
- Copyright: Copyright (c) 2024 Seth Hobson
- License: MIT
- Relevant upstream files:
  - plugins/agent-teams/agents/team-implementer.md
  - plugins/agent-teams/agents/team-lead.md
  - plugins/content-marketing/agents/search-specialist.md
- Adapted ideas: strict file ownership, immutable interface contracts, scoped
  team size, model tiering, primary-source research, and contradiction tracking.
- Not copied: the marketplace, large agent roster, preset teams, Claude Agent
  Teams command protocol, or comprehensive multi-domain review prompts.

## msitarzewski/agency-agents

- Repository: https://github.com/msitarzewski/agency-agents
- Copyright: Copyright (c) 2025 AgentLand Contributors
- License: MIT
- Relevant upstream file:
  - engineering/engineering-minimal-change-engineer.md
- Adapted ideas: smallest defensible diff, no opportunistic refactor, no scope
  creep, report rather than fix out-of-scope issues, and stop on ambiguity.
- Not copied: persona, memory, role-play prose, long examples, success metrics,
  communication style, or the full agent catalog.

## obra/superpowers

- Repository: https://github.com/obra/superpowers
- Copyright: Copyright (c) 2025 Jesse Vincent
- License: MIT
- Relevant upstream files:
  - skills/writing-plans/SKILL.md
  - skills/subagent-driven-development/SKILL.md
  - skills/subagent-driven-development/implementer-prompt.md
  - skills/dispatching-parallel-agents/SKILL.md
- Adapted ideas: task right-sizing, file and interface planning, self-contained
  dispatch, fresh implementation context, compaction-safe ledger state, model
  tiering, same-shape batching, and final integration review.
- Not copied: mandatory TDD, worktrees, per-task commits, long-lived
  docs/superpowers artifacts, multi-round fix loops, or the full lifecycle.

## MIT license for the listed upstream works

Each listed upstream work is made available under the following MIT terms, with
its copyright statement shown above:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The applicable copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
