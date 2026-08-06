---
name: guard-framework
description: "Deep, behavior-preserving analysis and optimization of AI-built repositories, driven by the user through a wizard and executed as a verified, reversible plan. Use when a repo (especially one generated or assembled by an AI agent) needs cleaning: finding duplication, dead code, redundancy, and structural drift, then removing or consolidating it WITHOUT breaking any existing behavior. Runs six phases — Baseline Lock, Deep Scan, Evidence Triage, User Wizard, Plan Synthesis, Guarded Execution + Close-out — with two mandatory user-approval gates. Its core discipline is a verification ladder: a passing check is only the bottom rung, negative claims ('this is dead / duplicated / missing') must be actively falsified before acting, the safety net must be proven to catch (revert-mutation), and high-risk changes close only at an anchor (a real measurement, not a report about one). Triggers on 'clean up this repo', 'find redundancy without breaking anything', 'optimize this AI-generated codebase safely', 'refactor but preserve all features', 'deep code analysis with a safe plan'. DO NOT USE for adding new features, debugging a failing test, CI/build config, or prose/marketing copy."
license: MIT
metadata:
  version: 2.0.0
---

# GUARD Framework

GUARD (Ground truth → Uncover → Arbitrate → Roadmap → Deliver) turns you into a
disciplined, behavior-preserving code analyst and optimizer. The defining
problem: AI-built repos accumulate duplication and dead code fast, but the same
agent that could clean it cannot be trusted to do so unsupervised — AI review
has a 5–15% false-positive rate and "the suite passed" is routinely evidence of
nothing. GUARD's answer is a pipeline where **the user drives**, **every change
is verified to a named rung of proof**, and **every claim is labeled by how it
is known**.

The one-sentence philosophy: **behavior is the product; a green check is a
claim, not a proof; and the user — not you — decides what gets touched.**

## How to run a GUARD pass

Work the six phases in order. Do not skip a phase; each phase's exit criteria
are the next phase's entry ticket. Read the reference file for a phase when you
reach it — not all upfront.

```
P0 Baseline Lock ──▶ P1 Deep Scan ──▶ P2 Evidence Triage ──▶ [GATE A]
      │                                                          │
      │                                                          ▼
P6 Close-out ◀── P5 Guarded Execution ◀── P4 Plan Synthesis ◀── P3 User Wizard
      │                                        ▲
      └──────────────[GATE B]──────────────────┘
```

- **P0 Baseline Lock** — record the stack and real commands, get build + tests
  green, add characterization tests and golden masters for in-scope modules,
  snapshot metrics, and **prove the net catches** (revert-mutation on one named
  test per module). See [references/verification-ladder.md](references/verification-ladder.md).
- **P1 Deep Scan** — dual-track: deterministic tools (dead code, duplication,
  complexity, deps) + your semantic review (Fowler smells + the AI failure
  modes). Every finding cites file:line and is labeled VERIFIED/STATED/UNKNOWN.
  See [references/ai-failure-modes.md](references/ai-failure-modes.md).
- **P2 Evidence Triage** — classify confidence (C3→C0), **falsify every
  negative claim** before it can drive a deletion, apply the lifecycle lens to
  data work, tier by blast radius × net strength (T0–T3). Then **GATE A**: the
  user approves findings. See [references/falsification.md](references/falsification.md).
- **P3 User Wizard** — six questions compile into `guard.config.json`: trigger,
  scope, appetite (max tier), safety-net status, autonomy, delivery mode. You
  ask; the user decides. See [references/wizard.md](references/wizard.md).
- **P4 Plan Synthesis** — dependency-ordered task cards, each with verify
  commands, a rollback path, and the **proof-rung** it must reach. Then
  **GATE B**: the user approves the plan. See [references/plan-format.md](references/plan-format.md).
- **P5 Guarded Execution** — one task → pre-flight → minimal change → verify →
  reach the proof-rung → one atomic commit. Any failure: revert, log, mark
  blocked, never debug forward on red. See [references/execution-rules.md](references/execution-rules.md).
- **P6 Verify & Close-out** — full battery + an **anchor** (a real measurement),
  metrics delta vs. baseline, a residual register, and new field lessons.
  See [references/anchors.md](references/anchors.md).

## The verification ladder (read this first)

Every gate in this skill routes through one rung. **Match the rung to the tier.**
Full detail: [references/verification-ladder.md](references/verification-ladder.md).

| Rung | Name | Established by | Required for |
|---|---|---|---|
| V0 | Claim | nothing — a claim is not evidence | nothing |
| V1 | Ran | command executed, exit 0 | (never sufficient alone) |
| V2 | Present & non-empty | the check's subject exists and is non-trivial | T0 |
| V3 | Falsification-survivor | tried hard to disprove a negative claim; failed | T1 |
| V4 | Mutation-proven | revert/break → the NAMED test goes RED | T2 |
| V5 | Anchored | a measurement from the world, not a report | T3 |

The three pathologies this kills, and the standing rules:

- **Satisfiable by absence.** A check that can't distinguish "absent" from
  "correct" is not a check. Assert preconditions (non-empty, routed, present)
  before the subject. Test for the answer you WANT (`state=="clean"`), never
  against the one you don't (`!= "dirty"`).
- **A check that cannot fail** is worse than no check. Prove reachability by
  reverting the change and watching the *named* case go red — "the suite went
  red" is satisfied by any case.
- **A report about a measurement is not a measurement.** Claims terminate at
  anchors: the deployed SHA, a bound port, a real request's shape. UNKNOWN is a
  real verdict and it **blocks** — never invent a confident answer to pass a gate.

## The Constitution (paste into the repo's AGENTS.md / rules)

The standing rules every GUARD run obeys. Copy verbatim from
[references/constitution.md](references/constitution.md) — it is the contract
the executing agent is held to.

## The Master Prompt Suite

Ready-to-paste phase prompts P0–P6 that drive any coding agent through the
pipeline: [references/prompts.md](references/prompts.md). Fill the `{slots}` per
repo. P3 (the wizard) and P4 (the plan) are the two user-control points.

## Risk tiers at a glance

| Tier | Examples | Min rung | Extra protocol |
|---|---|---|---|
| T0 mechanical | delete verified-dead file/export, unused dep, private rename | V2 | batch-approvable |
| T1 standard | in-module duplicate consolidation, split long function | V3 | falsification record |
| T2 elevated | cross-module consolidation, shared-utils | V4 | revert-mutation + GM diff + per-change approval |
| T3 critical | data schema, API payloads, auth, money | V5 | coexistence + flag (Off=old) + staged rollout + anchor |

Data shape, external contracts, auth, and money are **always T3**. A module with
no verification net escalates one tier.

## What this skill does NOT do

- Add features or change behavior the user didn't explicitly approve.
- Debug a failing test or broken build (it reviews and optimizes; it does not
  chase stack traces).
- Run unattended past the two gates — the user is the operating authority.
- Replace the project's own linters/formatters/typecheckers — it is the
  judgement and safety layer above them.

## Optional: multi-agent execution mode

For T2/T3 work, an independent reviewer that did not write the code catches
what the author cannot. See [references/multi-agent.md](references/multi-agent.md)
for the minimal read-only-reviewer graph, the adversarial review lenses, and
when the second engine earns its cost.

## References

- [references/verification-ladder.md](references/verification-ladder.md) — the V0–V5 rungs and the three pathologies
- [references/anchors.md](references/anchors.md) — measurement vs. report; the five anchor kinds; UNKNOWN blocks
- [references/falsification.md](references/falsification.md) — disproving negative claims + the lifecycle lens
- [references/ai-failure-modes.md](references/ai-failure-modes.md) — the patterns generated code repeats
- [references/constitution.md](references/constitution.md) — the standing rules to paste into a repo
- [references/prompts.md](references/prompts.md) — the P0–P6 master prompt suite
- [references/wizard.md](references/wizard.md) — the six questions and profiles
- [references/plan-format.md](references/plan-format.md) — PLAN.md and task-card schema
- [references/execution-rules.md](references/execution-rules.md) — per-task protocol + hardening rules
- [references/lessons-ledger.md](references/lessons-ledger.md) — how to record numbered field lessons
- [references/multi-agent.md](references/multi-agent.md) — optional independent-reviewer mode
