# Sol Explore Relay dispatch and result contracts

Read this reference when preparing an Explorer task or normalizing its result.

## Dispatch packet

Every Explorer receives:

1. `Outcome` — one observable answer, not a broad activity.
2. `Context benefit` — why isolating this exploration is worth the packet and coordination cost.
3. `Question` — the exact repository, documentation, or runtime question or falsifiable hypothesis.
4. `Sources` — exact paths, symbols, URLs, logs, artifacts, or supplied output.
5. `Scope` — read boundaries, preserved state, and explicit exclusions.
6. `Allowed checks` — only the non-mutating commands or evidence operations within scope.
7. `Stop when` — answer established, ambiguity found, evidence boundary reached, or scope would expand.
8. `Return` — the required compact result and citation format.

Also state that the child:

- is not alone in the workspace and must preserve unrelated work;
- must stay read-only and may not become an implementer or reviewer;
- may not spawn descendants, commit, push, publish, build remotely, or perform external writes;
- must stop rather than invent a missing product, architecture, permission, or scope decision.

## Checkpoint request

A checkpoint asks a running Explorer to report at its next safe boundary without cancelling:

- `Phase` — current bounded investigation;
- `Evidence` — useful facts or references already established;
- `Changes` — always `none`; report any unexpected mutation immediately;
- `Blocker` — current blocker or `none`;
- `Next` — the next bounded check and whether a terminal packet is ready.

The child continues after the checkpoint unless parent Sol records an allowed cancellation reason or a terminal stop condition has been reached.

## Result packet

Return:

- `Status`: `COMPLETED`, `BLOCKED`, or `INCONCLUSIVE`;
- `Answer`: the direct answer or hypothesis verdict;
- `Evidence`: exact file and line, symbol, URL, artifact, or command-output references;
- `Conflicts`: counter-evidence or `none`;
- `Unknowns`: material gaps or `none`;
- `Changes`: `none`;
- `Handoff`: the smallest parent-owned decision, implementation, or check.

Do not return raw search dumps, entire logs, broad listings, or a chronological diary when a compact evidence map is sufficient.

`INTERRUPTED` is an orchestration event, not a result status, and never authorizes an automatic retry. No file output is expected from an Explorer; judge the returned evidence, not file creation.
