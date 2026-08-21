# Sol-led Relay dispatch and result contracts

Read this reference when preparing a child task or normalizing a returned result.

## Dispatch packet

Every subagent receives all seven fields:

1. `Outcome` — one observable result, not a broad activity.
2. `Benefit` — why isolation or delegation is worth the coordination cost.
3. `Sources` — exact paths, symbols, URLs, logs, artifacts, or supplied evidence.
4. `Scope` — owned files or read boundaries, preserved contracts, and explicit out-of-scope work.
5. `Checks` — deterministic commands, evidence requirements, or review dimensions.
6. `Stop when` — success, ambiguity, blocker, budget, or evidence boundary.
7. `Return` — the result packet and required citations or file references.

Also state:

- the child is not alone in the workspace and must preserve unrelated work;
- it may not spawn descendants;
- it may not commit, push, publish, build remotely, or perform unrelated external actions;
- it must stop rather than invent a missing product, architecture, permission, or scope decision.

For a write-capable child, name the exact sources needed before editing. Once those sources establish the implementation path, it starts the owned-file change instead of widening discovery. If a missing fact materially prevents writing, it returns `BLOCKED` with the fact and partial evidence rather than continuing open-ended exploration.

## Checkpoint request

A checkpoint request asks a running child to report at its next safe boundary without cancelling its task. Return:

- `Phase` — current bounded activity;
- `Evidence` — useful facts or artifacts already established;
- `Changes` — files or artifacts produced so far, including `none`;
- `Blocker` — current blocker or `none`;
- `Next` — the next bounded action and whether a terminal packet is ready.

The child continues after the checkpoint unless the parent records an allowed cancellation reason defined by the Skill or a terminal stop condition has been reached. The parent uses checkpoints to steer scope and preserve partial value, not as a reason to interrupt a live child.

## Reviewer additions

A reviewer also receives:

- `Unresolved risk` — the precise risk the independent review should reduce;
- `Evidence` — task contract, actual diff or artifact, and relevant source context;
- `Checks already passed` — successful checks that should not be repeated broadly;
- `Do not repeat` — completed exploration, irrelevant directories, and settled decisions.

## Common result packet

Return compactly:

- `Status`: `COMPLETED`, `BLOCKED`, or `INCONCLUSIVE`;
- `Outcome`: what was established or produced;
- `Evidence`: direct file/line, symbol, URL, artifact, or command-output references;
- `Changes`: exact files or interfaces touched, or `none`;
- `Checks`: commands/evidence inspected and their real results;
- `Risks`: remaining uncertainty, regression surface, or missing evidence;
- `Handoff`: the smallest useful next action for the parent.

Do not return raw search dumps, entire logs, broad file listings, or a chronological diary when a distilled evidence map is sufficient.

No file change does not mean no usable result. Inspect reported evidence, diagnostics, and artifacts before classifying the return. `INTERRUPTED` is an orchestration event rather than a common result status; do not translate it into a retryable failure.

## Reviewer verdicts

`code_reviewer` returns findings ordered by severity. Each finding contains location, defect, impact, evidence, minimal correction direction, and verification needed. If there are no findings, say so explicitly and list residual untested risk.

`verification_reviewer` evaluates every acceptance criterion independently and returns `PASS`, `FAIL`, or `NOT_EVALUATED` for each. Missing browser, device, Preview, runtime, licensing, or user-acceptance evidence remains `NOT_EVALUATED`; never infer it from static checks.
