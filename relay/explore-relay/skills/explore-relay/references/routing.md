# Adjacent exploration routes

Repository ownership, callers, configuration, and data flow belong to `explore_code`. Current external contracts belong to `explore_docs`; preserve the requested product and version and open the primary source. Split a code-versus-docs question only when the evidence can be collected independently.

Use `explore_runtime` for a falsifiable question about logs, traces, failures, or process state. Use `explore_runtime_deep` when evidence spans named systems or materially conflicts. The parent may reframe a previous investigation if new evidence establishes this need; a bare inconclusive result is not a reason to send the same question to Terra.

If reproduction requires writing files, building artifacts, changing configuration, or mutating external state, the Explorer returns the needed action to the parent. A permission declaration does not make a diagnostic non-mutating.

The package has no Executor, Reviewer, or Integrator. Explorers can compare candidate explanations and supply counter-evidence; the parent makes implementation, causal, and acceptance decisions. Read the critical path when judgment requires it, and avoid duplicating the broad search.
