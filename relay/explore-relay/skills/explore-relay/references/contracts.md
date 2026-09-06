# Exploration handoff

Use a short natural-language packet. Include the information needed to answer reliably; the labels below are conveniences, not a form to complete.

## Dispatch

- **Question and decision context:** the concrete answer the parent needs.
- **Sources and scope:** starting paths, symbols, URLs, or logs; fixed user/repository constraints; read boundaries and allowed non-mutating diagnostics.
- **Done and return:** sufficient evidence, material unknowns, and the next useful check. Add a deadline or effort budget only when one exists.

Tell the child it shares the workspace, must stay read-only and preserve others' work, and must not spawn descendants or mutate Git or external state. A missing optional field is not a blocker. Inspect relevant in-scope dependencies and use routine judgment; return a material scope or authority conflict to the parent.

For example: "Trace how cancellation reaches the worker in src/jobs and tests/jobs. We need to decide whether a late result can still commit. Stay read-only; cite the relevant call path, evidence for and against the race, and uninspected paths."

## Return

Return `COMPLETED`, `BLOCKED`, or `INCONCLUSIVE`, followed by the answer, direct evidence, material conflicts or unknowns, and a next action if needed. Include coverage (searched and unsearched areas) and snapshot (relevant source state, document version/date, or log window). Qualify negative findings. Report changes as none, or disclose an unexpected mutation immediately. Prefer a compact evidence map to raw logs or a search diary.

## Checkpoints and recovery

When asked, report current activity, useful evidence, blocker, and next action at a safe boundary; a checkpoint does not cancel the task. The parent can use it to clarify the question without restarting discovery.

An interruption is a lifecycle event, not a success or failure verdict. Preserve its reason, partial evidence or its absence, stopped status, and resource ownership. A transport error can leave a child alive: inspect the actual state before retrying. Never infer termination from a polling timeout.

After confirmed termination, a follow-up needs a concrete new source, hypothesis, or corrected request. Do not rerun identical inconclusive work. Follow the user's cancellation and budget rather than inventing a retry allowance.
