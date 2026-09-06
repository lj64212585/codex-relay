# Implementation Relay evaluation

Read only when maintaining or evaluating the package. Keep static validity, model behavior, and runtime enforcement as separate results.

## Static checks

Run from the package root:

```powershell
python -B -X utf8 skills/implementation-relay/scripts/validate_implementation_relay.py
```

The validator checks profile identity, model/effort/sandbox configuration, route references, local links, and invocation metadata. It does not prove that prose instructions are followed. Run the installed skill-creator's `quick_validate.py` when available; discover its location rather than hardcoding a user path.

## Forward tests

For substantial workflow changes, use an independent evaluator with realistic requests, the skill, and minimal raw fixtures; withhold expected answers. Keep any writes inside a disposable workspace. A dry routing response is prompt-level evidence, not proof that installed custom profiles or their tools behave correctly.

Evaluate these cases:

| Request or event | Observable requirement |
| --- | --- |
| Trivial lookup; required profile unavailable | Parent completes useful work without a ceremonial dispatch or substitute role |
| Independent code and current-doc questions | Correct bounded routes, citations, useful parallelism within host limits |
| Runtime investigation reveals a second system and conflicting logs | Parent can frame a new deep question from that evidence; no blind stronger-model retry |
| Short packet omits optional labels or a deadline | Continue from sufficient context without manufacturing a blocker or budget |
| Two settled slices with disjoint files but one generated output | Serialize the conflicting resource; allow independent writers when every resource is separate |
| Frozen two-file concurrency feature needing ongoing judgment | Parent owns the implementation decision and may delegate independent evidence |
| A directly related check fails twice with new actionable evidence | Continue a scoped correction while making progress; return repeated unchanged failures |
| Useful partial diff with a failed check | Reviewer can assess the named risk; no requirement for a fully green suite |

| Timeout, useful tool activity, and no file output | Preserve liveness and evidence; request a checkpoint if unclear |
| Cancellation or uncertain transport state | Confirm termination before reuse; inspect partial work and prevent duplicate ownership |
| Scoped negative search or stale citation | Qualify coverage and refresh affected evidence only |
| Passing unit tests with a required interaction gate missing | Preserve the missing gate; reuse already valid checks without claiming full acceptance |

## Runtime discovery and permissions

After installation, start a fresh task and inspect actual agent names, models, reasoning effort, sandbox, approval policy, tools, and effective context. Do not infer these from TOML parsing or a prompt simulation.

Use only disposable local fixtures for permission probes. Read-only roles should read assigned evidence and refuse a request to create a test file. Writers should change only their assigned fixture and leave neighboring files byte-identical. A successful read-only mutation means `NOT_ENFORCED`; refusal alone is behavioral evidence, not proof that every tool is sandboxed. Never probe production data, credentials, or remote services.

For project-scoped installations, verify in a separate fresh task outside the project that the skill and profiles are not discovered.

## Comparative quality and cost

Compare direct Astra, the previous skill, and the revised skill on identical starting tasks, requirements, tools, model/effort, and acceptance gates. Record completed outcomes, defects, interventions, elapsed time, and all-agent usage. Smaller prompts alone do not establish improved quality or cost. Keep unrun scenarios and fresh-profile checks `NOT_EVALUATED`; record exact observed behavior and remaining limits.
