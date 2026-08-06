# The User Wizard

Six questions, asked once per run, compile into `guard.config.json` — the
machine-readable contract the agent obeys. Questions are about intent and
tolerance, not technique. The agent asks; the user decides.

## The six questions

| # | Question | Options | Controls |
|---|---|---|---|
| W1 | Why this run, why now? | routine hygiene · pre-release hardening · performance pain · post-incident | finding prioritization weights |
| W2 | What may be touched? | whole repo · named modules · hotspot list only | hard path allow-list |
| W3 | Change appetite? | Conservative (T0–T1) · Balanced (+T2) · Accelerated (+T3) | highest tier the plan may contain |
| W4 | What proves behavior today? | tests+GM · tests only · typecheck only · nothing | Phase-0 extension; per-module tier escalation |
| W5 | Where are the brakes? | approve every task · every batch · plan-only + report | autonomy / pause cadence |
| W6 | How should changes land? | PR per task · per phase · single branch · direct to main | git topology, commit granularity |

## Profiles as defaults

Most users should pick a profile and override single answers, not answer cold.

| Setting | 🛡 Conservative | ⚖ Balanced (default) | 🚀 Accelerated |
|---|---|---|---|
| Allowed tiers | T0–T1 | T0–T2 | T0–T3 |
| Min proof-rung ceiling | V3 | V4 | V5 |
| Approval cadence | every batch | every T2 + batch summaries | plan + T3 stage sign-offs |
| Safety-net requirement | characterization for T1+ | same (non-negotiable) | same (non-negotiable) |
| Risky-change rollout | n/a (T3 excluded) | flags where feasible | flags + staged canary |
| Best for | prod apps, thin tests, first run | most teams/repos | well-tested, hardening sprint |

## The hard rule no profile overrides

If W4 reveals an in-scope module has **no** verification net, the only changes
allowed there are Phase-0 net-building until the net exists — and the net must
be **mutation-proven (V4)** before T2+ work. The user chooses *where* the net is
built first, never *whether* it exists.

## guard.config.json shape

```json
{
  "trigger": "routine-hygiene",
  "scope": { "allow": ["src/**"], "deny": ["src/legacy/**"] },
  "max_tier": "T2",
  "proof_rung_ceiling": "V4",
  "approval_cadence": "per-t2-change",
  "delivery": "pr-per-task",
  "frozen_modules": ["src/billing"],
  "net_status": { "src/utils": "tests+gm", "src/billing": "none" }
}
```
