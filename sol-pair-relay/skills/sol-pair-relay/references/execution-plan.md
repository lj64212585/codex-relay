# Sol Pair Relay temporary execution plan

Read this reference only when tm_planner is dispatched. The plan is a compact
contract between two fresh Sol contexts, not project documentation and not a
place to pre-write ordinary implementation code.

~~~text
# Temporary Execution Plan

Goal:
<one observable project outcome>

Fixed Decisions:
- <user or repository decision that may not drift>

Evidence Basis:
- <exact source, symbol, artifact, or compressed finding>

Writable Scope:
- <exact file or bounded path owned by the executor>

May Read:
- <exact source or bounded area>

Protected Paths and Contracts:
- <path, interface, behavior, or unrelated work that must not change>

Interfaces and Invariants:
- consumes: <symbol, schema, file format, or none>
- produces: <symbol, schema, file format, or none>
- preserves: <compatibility or behavioral invariant>

## Step 1 — <bounded outcome>

Owns:
- <exact writable path from Writable Scope>

Requires:
- <dependency, source, or prior step>

Implementation Constraints:
- <non-obvious fixed choice>

Acceptance Evidence:
- <observable fact and matching evidence class>

Checks:
- <exact deterministic command or inspection>

Risk:
low | normal | high

Stop When:
- <success, ambiguity, conflict, permission boundary, or missing evidence>

## Acceptance Matrix

| Criterion | Required evidence | Pass condition | Owner |
|---|---|---|---|
| <technical criterion> | <test, diff, artifact, or inspection> | <exact fact> | executor |
| <user/external gate> | <matching real interaction> | <exact fact> | coordinator/user |

Final Checks:
- <exact command or inspection covering the integrated result>

Residual Gates:
- <gate that cannot be closed by technical execution, or none>
~~~

Repeat the step block only for dependencies with distinct outcomes or checks.
Combine small same-shape changes that share one interface and verification
surface. One tm_executor owns the complete writable scope; do not split files
between competing writers.

Return only:

~~~text
PLAN_READY
plan: <path>
steps: <count>
high_risk: [<step ids>]
unresolved_gates: [<gate or none>]
~~~
