# Poor Relay execution plan

Read this reference only when tm_planner is needed.

The planner creates one plan for the current task. Keep implementation detail at
the contract level: name exact files, interfaces, invariants, acceptance, and
checks, but do not pre-write ordinary implementation code.

~~~text
# Execution Plan

Goal:
<one observable project outcome>

Fixed Decisions:
- <decision already settled by the user or repository>

Global Constraints:
- <permission, compatibility, governance, and must-preserve boundary>

Task Graph:
1 -> 2
1 -> 3
2,3 -> 4

## Task 1 — <bounded outcome>

Outcome:
<observable result>

Depends on:
- <task id or none>

Owns:
- <exact writable path>

May Read:
- <exact source or bounded area>

Must Not Change:
- <shared or unrelated path and preserved contract>

Interfaces:
- consumes: <symbol, schema, file format, or none>
- produces: <symbol, schema, file format, or none>

Implementation Constraints:
- <non-obvious invariant or fixed choice>

Acceptance:
- <testable fact>

Checks:
- <exact command or evidence>

Risk:
low | normal | high

Review:
skip | terra | sol
reason: <risk that determines the gate>
~~~

Task right-sizing rule: one task is the smallest unit with its own meaningful
verification loop that a reviewer could independently accept or reject. Combine
small same-shape changes when they share one contract and verification surface.

The planner must identify shared files explicitly. Shared or integration files
are not assigned to competing executors.

Return only:

~~~text
PLAN_READY
plan: <path>
tasks: <count>
parallel: [<task ids>]
high_risk: [<task ids>]
~~~
