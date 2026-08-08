# The User Wizard

Six questions per run, compiled into `guard.config.json` — the machine-readable
contract the agent obeys (schema: [guard.config.schema.json](guard.config.schema.json)).
Questions are about intent and tolerance, not technique. The agent asks; the
user decides.

## The split: facts first, judgment after evidence

The six questions are asked in two parts, because four of them are facts the
pipeline consumes from Phase 0 onward, and two are risk judgments that are
better made while looking at triaged findings than cold.

**Wizard I — before P0** (answers write the *provisional* config,
`"status": "provisional"`):

| # | Question | Options | Controls |
|---|---|---|---|
| W1 | Why this run, why now? | routine hygiene · pre-release hardening · performance pain · post-incident | finding prioritization weights (P1/P2/P4) |
| W2 | What may be touched? | whole repo · named modules · hotspot list only | hard path allow-list; P0 net-building scope; P1 scan scope |
| W4 | What do you believe proves behavior today? | tests+GM · tests only · typecheck only · nothing | where P0 must build net first; per-module tier escalation |
| W6 | How should changes land? | PR per task · per phase · single integration branch · direct to main | git topology, commit granularity, the delivery base P5 branches from |

W4 records the user's *belief*; P0 then verifies the net that actually exists
and records both. A discrepancy (believed "tests", found "tests that catch
nothing") is itself a finding, reported at Gate A.

**Wizard II — at P3, after Gate A** (answers finalize the config,
`"status": "final"`):

| # | Question | Options | Controls |
|---|---|---|---|
| W3 | Change appetite? | Conservative (T0–T1) · Balanced (+T2) · Accelerated (+T3) | highest tier the plan may contain; proof-rung ceiling |
| W5 | Where are the brakes? | approve every task · every batch · plan-only + report | autonomy / pause cadence |

Asking W3/W5 here is deliberate: the user chooses appetite while looking at the
actual triaged findings and the verified net status — not against imagined risk.

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

If a module in scope has **no** verification net (believed at W4, verified at
P0), the only changes allowed there are Phase-0 net-building until the net
exists — and the net must be **mutation-proven (V4)** before T2+ work. The user
chooses *where* the net is built first, never *whether* it exists. A partial
net (typecheck only, or tests never watched failing) escalates findings in
that module one tier.

## Sizing the run (asked alongside W2)

- **Small repo (roughly <5k LOC) and appetite ≤T1:** offer the express path —
  collapse P1+P2 into one findings pass and present Gate A plus the plan as a
  single approval. Falsification of negative claims, exit-code judging, atomic
  commits, and revert-on-red still apply in full.
- **Large repo / monorepo:** scan hotspot-first (churn × complexity shortlist)
  with staged expansion; keep one `BASELINE.md` section and one verify-command
  set per package/workspace; scope globs follow workspace boundaries; any
  cross-package edit is T2 minimum.
- **Generated/vendored code** (build output, codegen, protobuf/client stubs,
  vendored libs, migrations, minified files) is enumerated at P1 entry and
  recorded in `scope.deny` — it is expected to look duplicated and dead, and
  scanning it produces noise, not findings.

## guard.config.json shape

Contract: [guard.config.schema.json](guard.config.schema.json) — validate with
`python3 scripts/guard_lint.py config guard.config.json`. Example:

```json
{
  "status": "final",
  "trigger": "routine-hygiene",
  "scope": { "allow": ["src/**"], "deny": ["src/legacy/**", "src/generated/**"] },
  "max_tier": "T2",
  "proof_rung_ceiling": "V4",
  "approval_cadence": "per-t2-change",
  "delivery": "pr-per-task",
  "delivery_base": "main",
  "frozen_modules": ["src/billing"],
  "net_status": { "src/utils": "tests+gm", "src/billing": "none" }
}
```

Field semantics worth stating: `scope.deny` paths are never scanned and never
touched; `frozen_modules` are scanned — findings there are reported at Gate A —
but no change to them may be planned. `net_status` records the **verified**
(post-P0) net per module, not the W4 belief.
