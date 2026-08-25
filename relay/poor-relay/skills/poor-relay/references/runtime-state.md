# Poor Relay runtime state

Read this reference when creating or recovering state.md for a planned or
long-running Poor Relay task.

The ledger is a compact recovery aid, not project documentation. Record terminal
evidence rather than conversation history.

~~~text
# Runtime State

task_id: <unique id>
status: ACTIVE | BLOCKED | COMPLETE
plan: .codex-team/runtime/<task-id>/plan.md
updated: <ISO-8601 timestamp>

## Task 1 — <name>

status: PENDING | RUNNING | COMPLETE | BLOCKED | ESCALATED
executor: NOT_RUN | PASS | FAIL | BLOCKED
checks:
- <command or criterion>: NOT_RUN | PASS | FAIL | NOT_EVALUATED
review: NOT_REQUIRED | NOT_RUN | PASS | FAIL
retry: 0 | 1
escalation: NONE | REQUIRED | COMPLETE
evidence:
- <path, artifact, or compact conclusion>
next:
- <one bounded next action>
~~~

Rules:

- Update the ledger only after a dispatch, terminal child result, review verdict,
  escalation decision, or meaningful blocker.
- Before recovery, compare the ledger with the actual files, diff, and artifacts.
  The ledger is evidence, not authority.
- Never mark browser, device, runtime, visual, licensing, release, or user
  acceptance PASS based on a different evidence class.
- Do not put secrets, full logs, raw research, or large diffs in state.md.
- Never stage or commit the runtime directory.
- On genuine overall completion, delete only this task's runtime directory.
- If blocked or interrupted, keep the ledger for the same task to resume.
