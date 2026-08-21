# Sol-led Relay role routing boundaries

Read this reference only when two neighboring roles appear plausible.

## Exploration

- Use `code_explorer` for repository truth: ownership, symbols, callers, dependencies, data flow, and blast radius.
- Use `docs_researcher` for truth outside the repository: official documentation, APIs, version behavior, standards, or upstream sources.
- Use `runtime_investigator` for one bounded observation question based on logs, test output, traces, process state, or reproducible runtime behavior.
- Use `runtime_investigator_deep` only when the task begins cross-system or the evidence supplied to it is already contradictory. It is not a second attempt after Luna.

When a question spans lanes, split only independent evidence questions. The parent reconciles conclusions and owns causal or architectural decisions.

## Execution

- Use `mechanical_executor` only when an exact transformation can be stated without semantic judgment. Unexpected semantics stop the task.
- Use `minimal_fixer` only after the root cause is confirmed and the allowed files are named. If the root cause is still a hypothesis, investigate first.
- Use `bounded_executor` only after interfaces, owned files, acceptance criteria, checks, and out-of-scope work are frozen.

Do not delegate vague requests such as “finish the feature,” “improve the system,” “refactor the subsystem,” or “make the game feel better.”

## Review

- Use `code_reviewer` to find real defects in the actual implementation or diff.
- Use `verification_reviewer` to decide whether completion claims are supported by acceptance evidence.

Neither reviewer fixes code, redefines requirements, merges work, or closes a user-acceptance gate.

## Direct parent work

Keep work with the parent when it is trivial, tightly interactive, dominated by unresolved decisions, high-risk and cross-cutting, dependent on visual or gameplay judgment, or not independently verifiable.
