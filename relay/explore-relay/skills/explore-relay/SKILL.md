---
name: explore-relay
description: "Delegate substantial code, documentation, or runtime investigation to read-only specialists while the parent implements and verifies. Use for context-heavy or independent exploration questions; handle trivial lookups directly."
---

# Explore Relay

Use isolated exploration to keep the parent focused on the user's outcome. The recommended parent is GPT-6 Astra; preserve the active model and reasoning settings. This skill delegates evidence gathering only. All edits, implementation, review verdicts, integration, and delivery stay with the parent.

## Working agreement

Follow the user's goal, scope, and existing authorization through completion. User instructions take precedence over this skill's workflow defaults, within host permissions and repository requirements. Resolve routine choices from context; ask only when missing input materially changes correctness, scope, or authority, and continue independent authorized work.

Delegate a substantial, self-contained investigation when it saves context or enables useful parallel work. Keep a quick lookup or a question tightly coupled to the next edit local. Use the host's available concurrency and tool surface; if a named profile is unavailable, do the work in the parent rather than substituting a different role or stopping the task.

## Routes

| Question | Exact agent_type | Configured model / effort |
| --- | --- | --- |
| Repository symbols, ownership, call paths, dependencies, data flow | `explore_code` | Luna / max |
| Current official documentation, APIs, versions, upstream contracts | `explore_docs` | Luna / max |
| A bounded runtime hypothesis, log, trace, or test failure | `explore_runtime` | Luna / max |
| Cross-system or materially conflicting runtime evidence | `explore_runtime_deep` | Terra / max |

Every profile requests `sandbox_mode = "read-only"`. Children may inspect evidence and run in-scope non-mutating diagnostics; they cannot edit, build artifacts, mutate external state, or close acceptance gates. Route by the evidence now available: a deep investigation needs a concrete cross-system question, including one newly established by an earlier report. An inconclusive answer alone does not justify model escalation.

Use [routing.md](references/routing.md) only for adjacent-role ambiguity.

## Delegate and continue

Give the child the question, why its answer matters, relevant sources and fixed constraints, read boundaries, and the evidence needed to finish. Use [contracts.md](references/contracts.md) for conditional packet and lifecycle details; field labels are optional.

Name the exact `agent_type`. Prefer `fork_turns = "none"` with a self-contained packet; include additional relevant context only when needed. Do not copy full history by habit. Tell children they share the workspace, must preserve others' work, and must not spawn descendants.

Run independent questions in parallel within host limits and any user budget. Give each interactive browser or runtime resource one owner. While children work, advance a different part of the task instead of repeating their searches.

A timeout or lack of file output does not establish failure. Check actual activity and request a checkpoint when progress is unclear. Stop obsolete, completed, budget-exhausted, or user-cancelled work deliberately, preserving partial evidence. Before takeover or resource reuse, confirm termination; keep resources isolated if stopping is unconfirmed. Inspect uncertain spawn outcomes before retrying so two children cannot own the same work.

After a terminal result, choose a targeted follow-up when new evidence offers a useful next check; otherwise resolve the question locally or report the concrete evidence boundary. Do not repeat the same unsuccessful request or create an automatic model escalation chain.

## Use the evidence and finish

Check cited sources, searched scope, and source freshness before relying on a report. A negative finding applies only to the searched area. Refresh stale decision-critical evidence; avoid recreating the child's entire investigation. Read critical paths sufficiently to own architecture, persistence, concurrency, security, and interaction decisions.

Complete the authorized implementation and required verification in the parent. Reuse successful checks on unchanged relevant state. Add or broaden tests when the changed behavior or unresolved risk needs them; visual and interaction claims require matching evidence when those gates apply.

Report the result, meaningful validation, and remaining uncertainty concisely. A child report is evidence, not a completion guarantee. If a skill instruction blocks progress, identify the exact file and instruction and explain the unresolved conflict.

For package maintenance, read [evaluation.md](references/evaluation.md). Static profile validation does not establish runtime discovery or effective sandbox enforcement.
