---
name: implementation-relay
description: "Delegate substantial investigation, settled implementation slices, and focused review to project specialists while the parent owns decisions and integration. Use when independent work improves delivery; handle small local tasks directly."
---

# Implementation Relay

Keep the parent responsible for the user's outcome, technical decisions, integration, and final acceptance. The recommended parent is GPT-6 Astra; preserve the active model and reasoning settings. Use the existing Luna / Terra profiles for bounded work.

## Working agreement

Carry the authorized task through implementation and relevant verification. User instructions take precedence over this skill's workflow defaults, within host permissions and repository requirements. Infer routine details from context. Ask only when missing input materially changes correctness, scope, or authority; continue independent work while that decision is pending.

Delegate when context isolation, independent implementation, or a fresh review improves delivery. Keep tightly coupled work local. Use the smallest useful set of roles, with parallel independent work when host capacity permits; no fixed exploration, execution, and review pipeline is required.

## Routes

| Need | Exact agent_type | Configured model / effort | Sandbox default |
| --- | --- | --- | --- |
| Repository facts and call paths | `code_explorer` | Luna / max | read-only |
| Current official docs, APIs, versions | `docs_researcher` | Luna / max | read-only |
| Bounded runtime hypothesis or failure evidence | `runtime_investigator` | Luna / max | read-only |
| Cross-system or conflicting runtime evidence | `runtime_investigator_deep` | Terra / max | read-only |
| Exact repetitive transformation | `mechanical_executor` | Luna / max | workspace-write |
| Confirmed local root-cause fix | `minimal_fixer` | Luna / max | workspace-write |
| Settled feature slice with owned files and acceptance criteria | `bounded_executor` | Luna / max | workspace-write |
| Concrete correctness or regression risk in a diff | `code_reviewer` | Terra / max | read-only |
| Acceptance claims against actual evidence | `verification_reviewer` | Terra / max | read-only |

Use [routing.md](references/routing.md) only to resolve adjacent-role ambiguity. A deep investigation requires actual cross-system or contradictory evidence, including newly discovered evidence; an inconclusive result alone is insufficient. If the required profile is unavailable, continue in the parent without inventing an equivalent role.

## Keep judgment where it is needed

Delegate writes when behavior, interfaces, ownership, and acceptance are settled and the child can verify its result. Allow routine implementation choices within that contract. Small file count is not evidence of low uncertainty: complex state, persistence, concurrency, security, and core interaction requiring continuing judgment remain with the parent. Exploration can still supply independent evidence.

The parent owns unresolved product and architecture decisions, shared interfaces, risk acceptance, visual and interactive judgment, and final integration. Children report material contract conflicts with useful partial work; they do not silently simplify requirements. Git mutations, publishing, external delivery, and user-acceptance decisions remain with the parent.

## Dispatch and ownership

State the outcome, relevant sources and constraints, read or write scope, acceptance evidence, and any real budget or stop boundary. Use [contracts.md](references/contracts.md) for examples and role-specific additions; do not turn missing field labels into blockers.

Name the exact `agent_type`. Prefer `fork_turns = "none"` when the packet is self-contained; supply further relevant context when needed instead of copying full history by default. Tell children they are not alone, must preserve and adapt to others' changes, and must not spawn descendants.

Parallelize independent work within host limits and user budgets. Writers may run concurrently only with disjoint files, stable interfaces, and independent generated outputs and runtime resources. Serialize shared-file changes, shared build outputs, or coupled interfaces. The parent follows the same ownership boundaries while children run.

## Steer, recover, and integrate

Wait without duplicating delegated work; continue useful independent work. A timeout, silence, or no diff yet is not proof of failure. Request a concise checkpoint when progress is unclear. Preserve partial results when work completes, becomes obsolete, hits a real budget or scope boundary, or is cancelled.

Confirm termination before takeover, inspect any writer's actual diff, and transfer ownership explicitly. If stopping is unconfirmed, isolate those resources. Inspect uncertain spawn or transport outcomes before retrying; never create a duplicate live writer.

Let a writer correct directly related check failures within its scope while it is making evidence-backed progress. A repeated unchanged failure, material contract conflict, or exhausted budget returns to the parent. After a terminal report, the parent may send a targeted follow-up with new evidence or take over. Do not repeat identical failed tasks or automatically escalate through model tiers.

Request independent review for a concrete residual risk. A useful diff or artifact is sufficient to start review: report failed or unavailable checks honestly, and do not require all tests to pass before a reviewer can help. Provide the acceptance contract, actual change, relevant context, and checks already performed.

## Verify and deliver

Inspect the real diff, artifacts, and relevant evidence before accepting a child's result. Qualify negative findings by coverage, check source freshness, and refresh only stale or incomplete decision-critical paths. Retain enough direct understanding to own high-impact decisions without repeating broad discovery.

Run checks proportionate to the changed behavior and complete required repository or user gates. Reuse successful checks on unchanged relevant state; broaden verification for a concrete new risk, change, or failure. Do not add tests that only restate a harmless edit. UI, interaction, device, or human acceptance requires its own evidence when applicable.

Finish the authorized task and explain the outcome, meaningful checks, and remaining limitations in concise language. Review PASS covers the reviewed risk; it does not establish global acceptance. If a skill instruction blocks progress, identify the exact file and instruction and explain the conflict.

For package maintenance, read [evaluation.md](references/evaluation.md). A declared sandbox is a requested default; effective discovery, tools, and enforcement require runtime evidence.
