# Adjacent implementation routes

## Evidence

Use `code_explorer` for repository facts and `docs_researcher` for current external contracts. Use `runtime_investigator` for a bounded runtime hypothesis, and `runtime_investigator_deep` for named cross-system or materially contradictory evidence. Newly discovered evidence may justify reframing the task; being inconclusive alone does not justify a stronger-model retry.

Investigators stay read-only, identify counter-evidence, and return material gaps. The parent reconciles evidence and owns high-impact causal and architectural decisions.

## Writes

Use `mechanical_executor` for an exact semantic-preserving transformation, `minimal_fixer` for a supported local root cause, and `bounded_executor` for a settled feature slice with ownership, interfaces, and acceptance criteria.

A bounded outcome leaves room for ordinary implementation choices. It does not transfer unresolved product or architecture judgment. Keep complex state, persistence, concurrency, security, and core interaction with the parent when continuous judgment is required. File count alone does not decide the route.

Parallel writers need disjoint files, stable interfaces, and separate generated outputs and runtime resources. Otherwise serialize them. Shared integration files have one owner.

## Review

Use `code_reviewer` for defects in an actual diff or implementation, and `verification_reviewer` for acceptance claims versus evidence. Review can help diagnose a failed check or partial implementation when its state is explicit. Reviewers inspect relevant dependencies as needed to establish a finding, without turning the task into a repository-wide audit.

Neither reviewer edits files, changes requirements, or closes final acceptance. A scoped PASS does not prove unreviewed behavior.

## Direct work

Keep trivial work, tightly coupled changes, unresolved decisions, and final visual or interactive judgment in the parent. Delegation should reduce task cost or improve evidence and delivery, rather than require the parent to specify every line before work starts.
