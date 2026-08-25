---
name: sol-pair-relay
description: Orchestrate non-trivial implementation from a Luna or Terra parent conversation by sending bounded exploration to Luna Max, temporary planning to one fresh Sol Max, and execution plus technical acceptance to a second fresh Sol Max. Use when implementation quality matters but one Sol context should not absorb research, planning, coding, and verification together; handle small one-step work directly.
---

# Sol Pair Relay

Keep the user conversation, authority, and lifecycle in a Luna or Terra parent
task. Move noisy evidence gathering into Luna Max, then isolate the two expensive
technical phases: one fresh Sol Max writes a temporary plan and a different fresh
Sol Max implements and technically accepts that plan.

## Activation gate

Handle a small, obvious, one-step answer or edit directly. Activate this relay
for a non-trivial change when all of these are useful:

- investigation can be compressed before planning;
- explicit scope, dependencies, interfaces, or checks should be frozen first;
- implementation benefits from a fresh Sol context that did not carry research
  or planning dialogue;
- one executor can own the approved writable surface and final technical checks.

For an activated mutation task, the planner and executor are mandatory and must
be different child agents. Exploration is optional. Do not create the pipeline
merely because profiles are available, and do not use it for read-only answers
that the parent can provide directly.

## Roles

Every dispatch names an exact agent type; never use a generic fallback.

| Need | Agent | Model and effort | Default sandbox |
|---|---|---|---|
| Bounded repository, docs, API, log, or runtime evidence | tm_explorer | Luna Max | read-only |
| Temporary implementation plan | tm_planner | Sol Max | workspace-write |
| End-to-end implementation and technical acceptance | tm_executor | Sol Max | workspace-write |

A Luna Max or Terra Max main task is the recommended Coordinator. The relay does
not replace the current parent model, create a second Coordinator, or transfer
the user conversation to a child.

## Coordinator authority

The Coordinator retains:

- the user's actual request, approvals, fixed decisions, and delivery language;
- lifecycle tracking, packet construction, and the decision to activate or stop;
- permission decisions, external writes, Git operations, publishing, and release;
- shared-workspace coordination and protection of unrelated changes;
- inspection of the actual diff and evidence before presenting the result;
- user, device, visual, browser, external-system, and other non-technical gates;
- cleanup of only the temporary runtime directory created for this task.

The planner owns delegated technical planning. The executor owns implementation
and technical acceptance inside the approved plan. Neither acquires permission
to expand scope or substitute for user acceptance.

## Fresh-context invariant

Never send one child both planning and implementation. Use a separate
tm_planner and tm_executor, and prefer fork_turns = "none" with self-contained
packets. Do not send the executor the planner transcript or raw Explorer output.
The durable handoff is the approved plan.md plus only decision-critical evidence.

Each Sol context should receive only what its phase needs:

- planner: goal, fixed decisions, compressed evidence, named sources, boundaries,
  acceptance needs, and the plan path;
- executor: approved plan, fixed decisions, decision-critical evidence, current
  workspace facts, writable/protected scope, and final checks.

Repository and user instructions always outrank the temporary plan. If they
conflict, stop and return the contradiction instead of silently repairing the
contract.

## Dispatch contract

Every child packet includes:

1. Outcome — one observable result for this phase.
2. Benefit — why isolated context is worth the dispatch.
3. Sources — exact paths, symbols, URLs, artifacts, logs, or supplied evidence.
4. Scope — read boundaries, owned files, protected paths, and exclusions.
5. Fixed decisions — user and repository choices that may not drift.
6. Interfaces — consumed and produced contracts when implementation is involved.
7. Acceptance — facts and evidence required for this phase.
8. Checks — deterministic commands or evidence requirements.
9. Stop when — success, ambiguity, blocker, permission, or evidence boundary.
10. Return — the compact packet expected by the Coordinator.

Tell every child that it is not alone in the workspace, must preserve unrelated
changes, must not spawn descendants, and must not commit, push, publish, or
perform unrelated external writes.

## Exploration

Use tm_explorer only when research would otherwise pollute a Sol context. Give it
one bounded evidence question. For repository work, require CodeGraph first when
a .codegraph index exists. For external research, require current primary sources,
contradiction tracking, and direct links.

At most three independent read-only Explorer instances may run in parallel. The
Coordinator compresses their outputs before planning and keeps raw dumps out of
both Sol packets. Accept only:

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

## Temporary plan gate

Before dispatching tm_planner, the Coordinator creates one unique directory:

~~~text
.codex-team/runtime/<task-id>/
~~~

The planner writes only plan.md using
[execution-plan.md](references/execution-plan.md). The plan freezes scope,
interfaces, sequence, acceptance, checks, and stop conditions for one executor;
it does not pre-write ordinary implementation code or create long-lived project
documentation.

Accept only:

~~~text
PLAN_READY
plan: .codex-team/runtime/<task-id>/plan.md
steps: <count>
high_risk: [<step ids>]
unresolved_gates: [<gate or none>]
~~~

The Coordinator reads the plan against the original request and current repo
rules before execution. A plan may be revised once before implementation when
new evidence exposes a concrete contract defect. Once implementation begins,
do not silently re-plan around a blocker.

## Execution and technical acceptance

Dispatch exactly one fresh tm_executor after approving the plan. Never run the
planner and executor concurrently. The executor owns the complete approved
writable surface and follows the plan in dependency order.

The executor must:

- read the plan first and stop on any packet, governance, or workspace conflict;
- make the smallest defensible diff inside owned files;
- preserve protected files, fixed decisions, and interfaces;
- run every named check and inspect the actual final diff and artifacts;
- evaluate every acceptance row with the matching evidence class;
- make at most one targeted correction for a directly caused check failure;
- return unknown user or external gates to the Coordinator without claiming them.

Accept only:

~~~text
EXECUTION_PASS
changed:
- ...
checks:
- <check>: PASS
acceptance:
- <criterion>: PASS | NOT_EVALUATED
scope: respected
residual_gates:
- <gate or none>
~~~

Any repeated failure, unowned-file requirement, contract conflict, missing
authority, or unverifiable technical criterion returns BLOCKED with the exact
evidence and smallest next decision. There is no automatic Reviewer, Integrator,
fallback Agent, or model handoff chain.

## Completion and cleanup

EXECUTION_PASS is technical evidence, not the final user-facing claim. The
Coordinator compares the plan, actual files, diff, artifacts, command results,
and residual gates. It performs only separately authorized Git or external
delivery actions and reports unevaluated acceptance honestly.

Never stage or commit .codex-team. On genuine overall completion, remove only
this task's runtime directory. If .codex-team/runtime and .codex-team are then
empty, they may also be removed. Preserve the plan when blocked or interrupted
so the same user task can resume without recreating decisions.
