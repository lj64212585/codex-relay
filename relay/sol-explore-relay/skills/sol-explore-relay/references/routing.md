# Sol Explore Relay routing boundaries

Read this reference only when two exploration roles appear plausible.

## Repository or external truth

- Use `sol_explore_code` for truth inside the repository: ownership, symbols, callers, dependencies, data flow, configuration sources, and blast radius.
- Use `sol_explore_docs` for truth outside the repository: current official documentation, APIs, version behavior, standards, or upstream sources.

When repository behavior depends on an external contract, split the questions only if they can be answered independently. Parent Sol reconciles the code and documentation evidence.

## Static or runtime evidence

- Use `sol_explore_code` when current source and configuration can answer the question without observing a running system.
- Use `sol_explore_runtime` for one falsifiable question based on existing logs, traces, test output, process state, or a non-mutating diagnostic.
- Use `sol_explore_runtime_deep` only when the dispatch already spans named systems or includes materially contradictory evidence. It is not a second attempt after `sol_explore_runtime`.

If runtime reproduction would build, write, reconfigure, log in, publish, or mutate an external system, stop the Explorer at the evidence boundary. Parent Sol decides and performs any authorized next action.

## Never delegate these roles

There is no Executor, Fixer, Implementer, Reviewer, Integrator, or default catch-all in this package. Planning, editing, code review, acceptance verification, integration, and delivery remain in parent Sol even when exploration supplied the evidence.

Keep a lookup direct when packetizing it would cost as much context as reading it in the parent.
