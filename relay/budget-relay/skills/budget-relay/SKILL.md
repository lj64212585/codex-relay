---
name: budget-relay
description: Orchestrate non-trivial project work when budget is prioritized and implementation decisions are settled. Use bounded execution, evidence gathering, risk-focused review, and early escalation for uncertain tasks. This is a cost-oriented option, not a promise of end-to-end Astra quality; handle small one-step tasks directly.
---

# Budget Relay

Use the smallest useful set of agents. Keep the main task focused on user intent,
lifecycle, routing, and concise result packets. Move noisy investigation and
bounded implementation into isolated child contexts, then spend stronger-model
capacity only on planning, unresolved technical judgment, or final integration.

## Activation gate

Handle a small, obvious, one-step answer or edit directly. Activate the relay
when one or more conditions hold:

- investigation would load substantial code, documentation, logs, or web evidence;
- two or more read-only questions can be answered independently;
- an implementation slice has frozen ownership and deterministic checks;
- an independent review would materially reduce behavioral or regression risk;
- unresolved architecture or cross-module integration justifies Astra.

Do not start the full workflow merely because agents are available. Do not create
more roles because technologies differ; route technology knowledge through an
applicable Skill.

## Roles

Every dispatch names an exact agent type; never use a generic fallback.
| Need | Agent | Model and effort | Default sandbox |
|---|---|---|---|
| Architecture or multi-step execution plan | tm_planner | Astra xHigh | workspace-write |
| Repository or external evidence gathering | tm_explorer | Luna Medium | read-only |
| One bounded implementation slice | tm_executor | Luna High | workspace-write |
| Independent blocking-risk review | tm_reviewer | Terra Medium | read-only |
| Escalation or final integration | tm_integrator | Astra xHigh | workspace-write |

Luna Max is the recommended Coordinator; preserve the current task's effective
model, permissions, and repository rules.
## Coordinator authority

The Coordinator retains:

- the user's actual request, approvals, scope, and delivery language;
- lifecycle tracking, task dispatch, and shared-file coordination;
- permission decisions, external writes, Git operations, publishing, and release;
- the distinction between automated evidence and user acceptance;
- inspection of actual diffs and artifacts before any completion claim;
- cleanup of only the runtime state created for the current task.

tm_planner and tm_integrator own delegated technical planning or integration
judgment. They never acquire user authority, permission to expand scope, or power
to close a user-acceptance gate.

## Context and dispatch contract

Prefer fork_turns = "none" when the packet is self-contained. Otherwise inherit
only the minimum recent turns. Never send full history by default.

Supply the task-relevant information below. Labels and unused fields are optional;
missing boilerplate alone is not a blocker:

1. Outcome — one observable result.
2. Benefit — why delegation is worth the coordination cost.
3. Sources — exact paths, symbols, URLs, artifacts, logs, or supplied evidence.
4. Scope — read boundaries or owned files, protected contracts, and exclusions.
5. Interfaces — consumed and produced contracts when implementation is involved.
6. Acceptance — facts that must be true when the task is complete.
7. Checks — deterministic commands or evidence requirements.
8. Stop when — success, ambiguity, blocker, permission, or evidence boundary.
9. Return — the compact packet expected by the Coordinator.
10. Fixed constraints, Decision context, Budget — relevant immutable decisions, evidence use, blocking status, and bounded effort or deadline.
11. Coverage and Snapshot — searched and unsearched boundaries, and the relevant source or workspace version.

Tell every child that it is not alone in the workspace, must preserve unrelated
changes, must not spawn descendants, and must not commit, push, publish, or
perform unrelated external writes.

## Smallest useful parallelism

- Start only agents whose work is genuinely independent.
- Prefer one Explorer with a coherent evidence question over many tiny searches.
- Run at most three independent read-only agents in parallel.
- Use one write-capable agent at a time unless ownership is fully disjoint and
  the current environment explicitly supports safe concurrent writers.
- Never assign two writers the same file, generated artifact, browser, or runtime.
- Keep shared files and integration edits with the Coordinator or tm_integrator.
- Batch small same-shape changes into one bounded task and one verification surface.

## Uncertainty gate before implementation

Before dispatching tm_executor, assess remaining judgment, not just file count. Unresolved persistence, concurrency, security, architecture, or core interaction decisions go directly to tm_integrator in Escalation Mode before an executor attempt. Supply one bounded technical task and its full writable scope. If the whole task requires continuous product or architecture judgment, recommend explore-relay with a capable parent and preserve the handoff evidence; never switch the parent model silently. A plan alone cannot transfer all implementation judgment. Review PASS is evidence for its named risk, not a global quality guarantee.

## Plan gate

Skip tm_planner for a clear, local, single-slice task whose decisions, files,
interfaces, and checks are already fixed.

Use tm_planner when the task is architectural, multi-step, dependency-sensitive,
or needs explicit ownership and interface boundaries. Before dispatch, create a
unique task directory under:
~~~text
.codex-team/runtime/<task-id>/
~~~
The planner writes only plan.md using the template in
[execution-plan.md](references/execution-plan.md). It returns:
~~~text
PLAN_READY
plan: .codex-team/runtime/<task-id>/plan.md
tasks: <count>
parallel: [<task ids>]
high_risk: [<task ids>]
~~~
The plan contains decisions, dependencies, ownership, interfaces, acceptance,
checks, and risk. It does not pre-write ordinary implementation code, require
per-task commits, or create long-lived project documentation.

## Runtime state

For a planned or long-running task, the Coordinator maintains state.md beside
plan.md. Read [runtime-state.md](references/runtime-state.md) when creating or
recovering this ledger.

Update state after each terminal child result. After context compaction, read the
ledger before dispatching anything so completed work is not repeated.

Budget Relay itself does not create OpenSpec, worktrees, archives, task briefs, or
other planning systems. If the repository or user already requires one, follow
that higher-priority governance and do not delete or replace its files.

Never stage or commit .codex-team. When the overall user task is genuinely
complete, remove only this task's runtime directory. If .codex-team/runtime and
.codex-team are then empty, they may also be removed. Preserve the runtime state
when the task is blocked or interrupted so the same task can resume.

## Exploration

Give tm_explorer one bounded evidence question. For repository work, provide
named files or symbols and follow the target repository search rules. For external research, require current first-party sources, necessary
query variation, contradiction tracking, and direct links.

Accept only a compressed evidence packet:
~~~text
EVIDENCE_READY
findings:
- ...
evidence:
- <path or URL> -> <conclusion>
uncertainty:
- ...
recommended_next_check:
- ...
~~~
Raw search dumps, long quotations, entire logs, and chronological diaries stay
out of the main task.

## Bounded execution

Dispatch tm_executor only after Outcome, owned files, protected files, interfaces,
acceptance, checks, and stop conditions are fixed.

The executor:

- changes only owned files;
- makes the smallest defensible diff;
- does not perform opportunistic refactors or add convenience features;
- reports out-of-scope defects without fixing them;
- runs all assigned deterministic checks;
- may make one targeted correction for a directly related check failure;
- stops on a second failure, contract conflict, or need for an unowned file.

Expected return:
~~~text
TASK_COMPLETE
changed:
- ...
checks:
- <check>: PASS
scope: respected
blockers: none
~~~
## Reviewer risk gate

Review may be skipped when all relevant behavior is mechanically proven: a
single local file, low blast radius, exact transformation, and strong automated
coverage.

Use tm_reviewer for business logic, multi-file cooperation, state transitions,
persistence, API contracts, boundary behavior, or regression risk that checks do
not fully prove.

Route directly to tm_integrator when the remaining problem is architectural,
security-sensitive, cross-system, concurrency-heavy, high-blast-radius, or weakly
verifiable.

Give the reviewer fresh context: task contract, actual diff, narrow source
context, executor checks, one precise unresolved risk, and completed work it must
not repeat. The only verdicts are:
~~~text
PASS
~~~
or:
~~~text
FAIL
blocking:
1. <defect, evidence, expected behavior, and minimal correction>
~~~
Omit style-only suggestions and unrelated technical debt.

## Retry and escalation

An executor handles a directly related deterministic failure once inside its
turn. After reviewer FAIL, the Coordinator may dispatch Luna once for the
specific blocking correction.

If the correction or review fails again, route the task directly to
tm_integrator in Escalation Mode. Terra remains a reviewer and never becomes the
fallback executor. Do not create a model handoff chain.

A transport failure may be retried once only when no child remains running.
A wait timeout, silence, token use, or absence of a file is not proof of failure.
Request a checkpoint when progress is unclear and preserve useful partial evidence.
End delegation with a recorded reason when evidence is sufficient, the question
is obsolete, the stated budget is exhausted, the user cancels, or a scope or
safety conflict occurs. Confirm a writer has stopped and audit its diff before
transferring ownership. Keep unconfirmed resources isolated. Advance independent
work while waiting without treating missing evidence as established.

## Final integration

After all planned tasks reach a terminal completed state, dispatch tm_integrator
once in Final Mode with:

- plan.md and state.md;
- the actual final diff and artifacts;
- checks already passed;
- reviewer blocking findings and their disposition;
- the exact final checks it owns.

The integrator checks cross-task contracts and resolves blocking integration
defects within its assigned ownership, then runs the assigned final checks.

Accept FINAL_PASS only as technical evidence. The Coordinator still inspects the
real output, preserves any unevaluated user or runtime gate, performs authorized
delivery steps, cleans the current runtime directory, and reports concisely.
