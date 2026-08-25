---
name: sol-led-relay
description: "Automatically orchestrate specialized project subagents for non-trivial project work while the parent Sol agent retains decisions and integration. Use implicitly for substantial 代码探索、外部文档或 API 调研、日志与运行证据分析、明确范围的机械修改或 Bug 修复、bounded feature implementation、独立代码审查、或验收证据核对. Do not use for trivial one-step answers or edits, casual conversation, or work that cannot be decomposed safely."
---

# Sol-led Relay

Keep the parent agent focused on requirements, decisions, integration, and the final answer. Delegate only the bounded work whose context, independence, or separate review creates a real benefit.

## Activation

This skill is implicitly invocable. When it activates, first decide whether delegation is actually useful. Complete a small, obvious, one-step task directly even when the prompt matched the description.

Delegate when one or more of these is true:

- investigation would load substantial code, documentation, logs, or runtime output;
- two or more read-only questions can be answered independently;
- an implementation slice has frozen scope, owned files, and deterministic checks;
- independent review materially reduces correctness or acceptance risk.

Do not delegate merely to follow a pipeline. Do not create an architect subagent.

## Parent-only responsibilities

The parent retains:

- unresolved product, architecture, security, permission, scope, or cross-system decisions;
- task decomposition, interface ownership, shared-file coordination, and risk acceptance;
- visual quality, gameplay feel, device, browser, Preview, and user-acceptance judgments;
- final integration, authoritative validation, delivery claims, Git operations, Maker builds, publishing, and external writes;
- takeover after an investigator returns inconclusive or an executor exhausts its bounded correction.

Subagents may gather evidence or implement a frozen slice, but they cannot close these gates.

## Route to the smallest useful set

| Need | Agent | Model | Default permission |
|---|---|---|---|
| Trace repository code, symbols, dependencies, or call paths | `code_explorer` | Luna Max | read-only |
| Verify external documentation, APIs, versions, or standards | `docs_researcher` | Luna Max | read-only |
| Inspect one bounded runtime, log, test-failure, or reproduction question | `runtime_investigator` | Luna Max | read-only |
| Investigate an initially cross-system problem or already contradictory evidence | `runtime_investigator_deep` | Terra Max | read-only |
| Apply an exact rename, mapping, formatting, or repetitive transformation | `mechanical_executor` | Luna Max | workspace-write |
| Fix a confirmed local root cause with the smallest defensible diff | `minimal_fixer` | Luna Max | workspace-write |
| Implement one frozen feature slice with owned files and acceptance checks | `bounded_executor` | Luna Max | workspace-write |
| Review correctness, regression, security, and missing tests | `code_reviewer` | Terra Max | read-only |
| Audit acceptance criteria and claimed evidence | `verification_reviewer` | Terra Max | read-only |

`runtime_investigator_deep` is not a fallback for an inconclusive Luna pass. Use it only when the task is cross-system or the supplied evidence already conflicts. If `runtime_investigator` returns inconclusive after one pass, return the question to the parent without retrying or model escalation.

For detailed boundaries, read [routing.md](references/routing.md) only when choosing between adjacent roles.

## Dispatch protocol

Before spawning, prepare the complete packet defined in [contracts.md](references/contracts.md). Every dispatch must name the exact `agent_type`; never omit it or use `default`.

Use bounded context:

- prefer `fork_turns = "none"` when the packet and named sources are self-contained;
- otherwise fork only the minimum recent turns needed;
- never use full-history inheritance for these model-specific roles;
- provide exact paths, symbols, URLs, logs, artifacts, or command outputs instead of making the child rediscover scope.

Tell every child it is not alone in the workspace, must preserve unrelated changes, and must not spawn descendants.

## Concurrency and ownership

- Run at most three independent read-only agents in parallel.
- Use only one write-capable agent at a time.
- Assign each writer explicit file or directory ownership.
- Never give two agents the same writable file, generated artifact, interactive browser, or runtime session.
- Shared files and integration edits remain with the parent.
- Wait for every requested result before synthesizing across them.

## Liveness, waiting, and interruption

- A wait timeout is only a polling observation. It does not mean the child failed, stopped, or may be replaced.
- Treat recent commentary, reasoning, successful tool calls, new evidence, or file changes as liveness. A writer can be live before its first file change.
- If progress is unclear or slow, send the running child a checkpoint request for its current phase, evidence or artifacts, changes including `none`, blocker, and next action. Keep waiting while it remains live; the checkpoint preserves partial value without ending the task.
- Do not call `interrupt_agent` merely because time elapsed, tokens were used, waits timed out, or no file exists yet. None of those facts proves a hang.
- If a checkpoint is not acknowledged and no activity follows, treat it as a suspected infrastructure hang: record the partial-result audit, keep the child intact, and surface the blocking condition to the user. Silence never authorizes retry, takeover, or interruption by itself.
- Interrupt only for user cancellation or override, a recorded parent cancellation required by a newly discovered safety, scope, or dependency conflict, unsafe or out-of-scope mutation, or the child's explicit stop request. Record the allowed reason.
- Before an allowed interruption, preserve the thread's usable evidence and artifacts. `INTERRUPTED` is an orchestration event, not a child result, and never authorizes automatic retry.
- The parent may take over only after a terminal result (`COMPLETED`, `BLOCKED`, or `INCONCLUSIVE`) or an allowed interruption whose partial-result audit has been recorded.

## Failure and review flow

- Inspect any usable artifact or partial result before retrying a transport or tool failure.
- Retry a transient spawn or transport failure at most once, and only when no child remains running. Do not retry a completed but inconclusive investigation or a manually interrupted child.
- An executor may make one targeted correction only when its required deterministic check exposes a directly related defect. A second failure returns to the parent.
- Review only after the executor reports the required checks and the parent confirms the real diff or artifact exists.
- Give reviewers fresh, bounded evidence. Include checks already passed and tell them not to repeat broad validation.
- Ask a reviewer reaching its stop condition for a partial verdict rather than spawning a replacement automatically.
- Never route a failed Luna executor to a Terra executor. The parent decides the next action.

## Accepting results

Treat subagent reports as evidence, not authority. The parent must inspect the actual relevant files, diff, artifacts, and validation output before accepting a result or claiming completion.

For read-only roles, `sandbox_mode = "read-only"` is a requested default, not proof of effective isolation. If permission assurance matters, follow the runtime probes in [evaluation.md](references/evaluation.md). A successful write or mutation probe means `NOT_ENFORCED`; do not describe the role as technically read-only.

When maintaining or evaluating this skill, read [evaluation.md](references/evaluation.md). Do not load it for ordinary routed work.
