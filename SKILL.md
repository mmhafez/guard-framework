---
name: guard-framework
description: "Behavior-preserving cleanup and optimization of AI-built repositories. Finds duplication, dead code, redundancy, and structural drift, then removes or consolidates it without changing observable behavior — via a gated pipeline (P0–P6): baseline lock with a mutation-proven safety net, dual-track deep scan, evidence triage that falsifies every negative claim, a user wizard, plan synthesis into verifiable task cards, guarded execution, anchored close-out. The user approves findings (Gate A) and the plan (Gate B). Use when asked to clean up, de-duplicate, refactor safely, or optimize an existing repo — especially AI-generated code — e.g. 'clean up this repo without breaking anything', 'find dead code', 'remove duplication safely', 'this AI-built codebase is a mess'. Do not use for adding features, debugging a failing test or broken build, or CI/build configuration."
license: MIT
compatibility: "Any Agent Skills client. Execution phases need git, a POSIX shell, and the target repo's own build/test toolchain; scanners (knip, jscpd, vulture, etc.) are recommended but optional."
metadata:
  version: "2.1.0"
---

# GUARD Framework

GUARD (Ground truth → Uncover → Arbitrate → Roadmap → Deliver) turns you into a
disciplined, behavior-preserving code analyst and optimizer. The defining
problem: AI-built repos accumulate duplication and dead code fast, but the same
agent that could clean it cannot be trusted to do so unsupervised — AI review
carries a material false-positive rate and "the suite passed" is routinely
evidence of nothing. GUARD's answer is a pipeline where **the user drives**,
**every change is verified to a named rung of proof**, and **every claim is
labeled by how it is known**.

The one-sentence philosophy: **behavior is the product; a green check is a
claim, not a proof; and the user — not you — decides what gets touched.**

## Run state and resumability (do this first)

Every GUARD run keeps its state in `GUARD-RUN.md` at the repo root (copy
[assets/templates/GUARD-RUN.md](assets/templates/GUARD-RUN.md)). It records the
current phase, the wizard answers collected so far, and each gate decision per
finding ID. On starting ANY GUARD work: if `GUARD-RUN.md` exists, resume from
the phase it names — never re-run completed phases or re-ask answered wizard
questions. A gate with no recorded decision in `GUARD-RUN.md` has not been
passed, whatever the conversation history says.

## How to run a GUARD pass

Work the phases P0–P6 in order. Do not skip a phase; each phase's exit criteria
are the next phase's entry ticket. Read the reference file for a phase when you
reach it — not all upfront.

```
Wizard I (W1 W2 W4 W6) ─▶ P0 Baseline ─▶ P1 Scan ─▶ P2 Triage ─▶ [GATE A]
 intent · scope · nets · delivery                                     │
                                                                      ▼
 P6 Close-out ◀── P5 Execution ◀── [GATE B] ◀── P4 Plan ◀── P3 Wizard II (W3 W5)
                                                             appetite · autonomy
```

The wizard is split on a principle: **facts first, judgment after evidence.**
W1 (trigger), W2 (scope), W4 (believed safety net), and W6 (delivery mode) are
facts the user already knows and P0–P2 need — ask them before P0 and write the
provisional `guard.config.json`. W3 (change appetite) and W5 (autonomy) are risk
judgments best made while looking at triaged findings — ask them at P3 and
finalize the config. See [references/wizard.md](references/wizard.md).

- **P0 Baseline Lock** — record the stack and real commands, verify build +
  tests green (red → STOP and report; the user decides — GUARD does not debug),
  add characterization tests and golden masters for in-scope modules, snapshot
  metrics, and **prove the net catches** (revert-mutation on one named test per
  module). Record the net actually found vs. the user's W4 belief — a
  discrepancy is a finding. See [references/verification-ladder.md](references/verification-ladder.md).
- **P1 Deep Scan** — dual-track: deterministic tools (dead code, duplication,
  complexity, deps) + your semantic review (Fowler smells + the AI failure
  modes), scoped by W2, with generated/vendored paths excluded and recorded.
  Every finding cites file:line and is labeled VERIFIED/STATED/UNKNOWN.
  See [references/ai-failure-modes.md](references/ai-failure-modes.md).
- **P2 Evidence Triage** — classify confidence (C3→C0), **falsify every
  negative claim** before it can drive a deletion, apply the lifecycle lens to
  data work, tier by blast radius × net strength (T0–T3). Then **GATE A**: the
  user approves findings; record each decision in `GUARD-RUN.md`.
  See [references/falsification.md](references/falsification.md).
- **P3 User Wizard II** — ask W3 (appetite) and W5 (autonomy) against the
  evidence, then finalize `guard.config.json` and validate it
  (`scripts/guard_lint.py config guard.config.json`). You ask; the user
  decides. See [references/wizard.md](references/wizard.md).
- **P4 Plan Synthesis** — dependency-ordered task cards, each with verify
  commands, a rollback path, and the **proof-rung** it must reach. Lint the
  plan (`scripts/guard_lint.py plan PLAN.md`). Then **GATE B**: the user
  approves the plan. See [references/plan-format.md](references/plan-format.md).
- **P5 Guarded Execution** — one task → pre-flight → minimal change → verify →
  reach the proof-rung → one atomic commit. Any failure: revert, log, mark
  blocked, never debug forward on red. See [references/execution-rules.md](references/execution-rules.md).
- **P6 Verify & Close-out** — full battery + an **anchor** (a real measurement),
  metrics delta vs. baseline, a residual register, and new field lessons.
  See [references/anchors.md](references/anchors.md) and
  [references/lessons-ledger.md](references/lessons-ledger.md).

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
  red" is satisfied by any case failing.
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
repo. The two hard gates are **Gate A** (end of P2, findings) and **Gate B**
(end of P4, plan); P3 is the configuration control point between them.

## Risk tiers at a glance

| Tier | Examples | Min rung | Extra protocol |
|---|---|---|---|
| T0 mechanical | delete verified-dead file/export, unused dep, private rename | V2 | batch-approvable |
| T1 standard | in-module duplicate consolidation, split long function | V3 | falsification record |
| T2 elevated | cross-module consolidation, shared-utils | V4 | revert-mutation + GM diff + per-change approval |
| T3 critical | data schema, API payloads, auth, money | V5 | coexistence + flag (Off=old) + staged rollout + anchor |

Data shape, external contracts, auth, and **money logic** (computation,
persistence, payment contracts) are always T3; money *display formatting* is
T2, but any golden-master diff that moves a monetary value stops the task for
an explicit user decision. Net escalation: a module with a **partial** net
(typecheck only, or tests that are not mutation-proven) escalates one tier; a
module with **no** net is frozen except for net-building (the W4 hard rule).

## Sizing the run

Match ceremony to repo, never discipline to convenience — falsification,
exit-code judging, atomic commits, and revert-on-red are non-negotiable at any
size. **Small repo (roughly <5k LOC), max tier ≤T1:** run express — collapse
P1+P2 into one findings pass, present Gate A and the plan in a single approval,
skip golden masters where characterization tests already pin behavior.
**Large repo / monorepo:** W2 first (already the order), scan hotspot-first
(churn × complexity shortlist) with staged expansion; keep per-package baseline
entries and treat cross-package edits as T2 minimum. Full detail:
[references/wizard.md](references/wizard.md).

## Templates, schema, and the linter

Copy-ready artifact templates live in [assets/templates/](assets/templates/):
`GUARD-RUN.md`, `BASELINE.md`, `FINDINGS.triaged.md`, `PLAN.md`, `DELTA.md`,
`GUARD-LESSONS.md`, `guard.config.example.json`. The config contract is
[references/guard.config.schema.json](references/guard.config.schema.json).
Enforcement is mechanised, not doctrinal: run `python3 scripts/guard_lint.py`
(subcommands `config`, `plan`, `findings`, `run-state`) at the phase points
named above — it judges by exit code and **fails on an empty subject** (a plan
with zero task cards is a lint failure, not a pass).

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
- [references/anchors.md](references/anchors.md) — measurement vs. report; the five anchor kinds; offline anchors; UNKNOWN blocks
- [references/falsification.md](references/falsification.md) — disproving negative claims + the lifecycle lens
- [references/ai-failure-modes.md](references/ai-failure-modes.md) — the patterns generated code repeats
- [references/constitution.md](references/constitution.md) — the standing rules to paste into a repo
- [references/prompts.md](references/prompts.md) — the P0–P6 master prompt suite
- [references/wizard.md](references/wizard.md) — the six questions, the split, profiles, sizing
- [references/plan-format.md](references/plan-format.md) — PLAN.md and task-card schema
- [references/execution-rules.md](references/execution-rules.md) — per-task protocol + hardening rules
- [references/lessons-ledger.md](references/lessons-ledger.md) — numbered field lessons + mechanisation states
- [references/multi-agent.md](references/multi-agent.md) — optional independent-reviewer mode
- [references/guard.config.schema.json](references/guard.config.schema.json) — the config contract
