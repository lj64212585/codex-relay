# Implementation handoff

Use a concise packet with the information the task needs. Field names and empty placeholders are optional.

## Dispatch

Include the observable outcome, relevant sources and fixed constraints, read boundaries or writable ownership, and acceptance checks or evidence. Add dependencies, protected interfaces, a real budget, or stop conditions when they affect the work.

A writer needs enough source context to start, exact owned files or directories, preserved behavior, and an independently checkable result. Inspect narrowly relevant dependencies and choose ordinary implementation details within this contract. Escalate a material contract or ownership gap; do not block over missing boilerplate.

Tell every child it shares the workspace, must preserve and adapt to others' changes, and must not spawn descendants, mutate Git, publish, or perform unrelated external writes.

Example: "Apply the provided field-name mapping in src/export and tests/export. Preserve serialized values and public APIs. You own those directories; another worker owns src/import. Run the export regression checks and report the actual diff and results. Escalate any mapping that changes semantics."

## Review additions

Supply the named unresolved risk, acceptance contract, actual diff or artifact, relevant source context, and checks already performed. Include failures and unavailable checks. A reviewer can inspect a partial implementation if its limits are explicit; review is not conditional on a completely green test suite.

## Result

Return `COMPLETED`, `BLOCKED`, or `INCONCLUSIVE` with the outcome, direct evidence, changed files or none, actual check results, and material remaining risk. Include coverage and snapshot information sufficient to qualify negative findings and detect stale evidence. Give a next action when work remains.

A code reviewer leads with evidenced defects ordered by severity, each with location, impact, and a correction direction. If none are found, state the reviewed scope and residual risk. An acceptance reviewer returns `PASS`, `FAIL`, or `NOT_EVALUATED` for each assigned criterion; a missing evidence class stays unevaluated.

## Checkpoints and ownership transfer

At a checkpoint, report current activity, evidence or artifacts, changes including none, blocker, and next action. Continue unless cancelled or a real stop condition is met.

Preserve partial work after interruption. Confirm the child stopped, inspect its actual diff, and explicitly transfer owned resources before another writer or the parent takes over. If stopping is unconfirmed, keep those resources isolated and continue independent work.

Inspect ambiguous transport outcomes before retrying. A follow-up should add evidence, correct the request, or address a specific defect. Repeated unchanged failures and contract conflicts return to the parent; they do not trigger an automatic replacement or model escalation.
