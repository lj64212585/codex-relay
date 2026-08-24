---
name: sol-explore-relay
description: "Keep parent Sol as the sole implementation and delivery owner while automatically delegating only bounded read-only exploration. Use implicitly for substantial repository tracing, current external documentation or API research, bounded log or runtime evidence analysis, or initially cross-system contradictory evidence when isolation saves parent context. Do not delegate edits, implementation, review verdicts, validation ownership, Git actions, external mutations, or trivial one-step lookups."
---

# Sol Explore Relay

Keep the user-facing conversation, every mutation, and final technical ownership in parent Sol. Delegate only bounded read-only exploration whose isolated context would otherwise crowd the parent session.

Delegation is an optimization, not a required phase. All edits and implementation stay in parent Sol.

## Activation gate

This skill is implicitly invocable. Before dispatching, compare the likely context saved with the packet and coordination cost.

Delegate only when:

- repository tracing requires substantial source, dependency, ownership, or call-path context;
- current external documentation or API facts require focused primary-source research;
- a bounded log, trace, test-failure, or process-state question can be investigated without mutation;
- a problem begins cross-system or with materially contradictory runtime evidence;
- two or more independent read-only questions can run in parallel without sharing mutable state.

Keep the work direct when it is a trivial lookup, tightly coupled to the next edit, dominated by unresolved decisions, or cheaper to inspect in the parent than to packetize.

## Only these routes may be delegated

| Need | Exact Agent | Model | Permission |
| --- | --- | --- | --- |
| Trace repository code, symbols, dependencies, ownership, or blast radius | `sol_explore_code` | Luna Max | read-only |
| Verify current external docs, APIs, versions, standards, or upstream facts | `sol_explore_docs` | Luna Max | read-only |
| Inspect one bounded log, trace, test failure, or runtime hypothesis | `sol_explore_runtime` | Luna Max | read-only |
| Reconcile a question that starts cross-system or already contradictory | `sol_explore_runtime_deep` | Terra Max | read-only |

`sol_explore_runtime_deep` is not a fallback for an inconclusive Luna pass. If an ordinary runtime investigation is inconclusive, return the question to parent Sol.

Read [routing.md](references/routing.md) only when choosing between adjacent exploration roles.

## Parent Sol owns everything else

The parent alone performs:

- requirement, product, architecture, security, permission, scope, and interface decisions;
- planning, decomposition, implementation, edits, fixes, refactors, and generated-file updates;
- code review verdicts, acceptance audits, deterministic completion checks, and risk acceptance;
- shared-file coordination, integration, visual or interactive judgment, and user communication;
- Git mutations, builds that create artifacts, publishing, deployment, external writes, and final delivery.

An Explorer may inspect existing evidence and run explicitly allowed non-mutating diagnostics. It never becomes an Executor or Reviewer, never edits a file, and never closes a completion gate.

## Dispatch a self-contained question

Before spawning, prepare the packet in [contracts.md](references/contracts.md). Always name the exact `agent_type`; never omit it or use `default`.

Keep child context narrow:

- prefer `fork_turns = "none"` when the packet and named sources are sufficient;
- otherwise fork only the minimum recent turns needed;
- never use full-history inheritance for these roles;
- provide exact paths, symbols, URLs, logs, artifacts, or command output;
- state that the child is not alone, must preserve unrelated work, and must not spawn descendants.

Run at most three independent Explorers in parallel. Never give two children the same interactive browser, runtime session, or other stateful resource.

## Preserve context without lowering confidence

Ask for a compact answer with direct evidence, conflicts, unknowns, and the smallest next check. Do not request raw search dumps, entire logs, or broad file inventories.

Treat the returned packet as evidence, not authority. Verify the decision-critical cited slice or source before acting, but do not repeat the child's broad exploration merely to recreate its context in the parent. Unsupported claims remain unaccepted.

Parent Sol reconciles cross-lane conclusions, makes the implementation decision, changes the files, runs the completion checks, and reports the result.

## Liveness and failure

- A wait timeout is only a polling observation, not proof that a child failed or stopped.
- Recent commentary, reasoning, tool output, or evidence is liveness. If progress is unclear, request the checkpoint defined in [contracts.md] and continue waiting while activity remains.
- Silence alone never authorizes interruption, retry, replacement, or parent takeover. After an unacknowledged checkpoint and repeated inactivity, record the partial evidence, keep the child intact, and surface a suspected infrastructure hang.
- Interrupt only for user cancellation or override, unsafe or out-of-scope mutation, a newly discovered safety or dependency conflict that requires cancellation, or the child's explicit stop request. Record the reason and do not retry automatically.
- Retry a spawn or transport failure at most once, only when no child remains running and no work began.
- Continue in the parent only after a terminal `COMPLETED`, `BLOCKED`, or `INCONCLUSIVE` packet, or an allowed interruption with its partial-result audit recorded.

## Acceptance

Every child returns evidence to parent Sol. The parent decides whether the evidence is sufficient, performs all implementation and verification, and makes only claims supported by the actual files, outputs, and acceptance gates.

When installing, changing, or auditing this package, read [evaluation.md](references/evaluation.md). Do not load it during ordinary routed work.
