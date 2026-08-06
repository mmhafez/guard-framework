# Master Prompt Suite (P0–P6)

Paste-ready phase prompts that drive any coding agent through the pipeline.
Fill `{slots}` per repo. The two hard gates are Gate A (end of P2) and Gate B
(end of P4); P3 is the configuration control point between them. This file is
the single source of truth for the suite — the copy in
`docs/GUARD-Framework.md` §12 must match it verbatim (checked by
`scripts/guard_lint.py sync`).

## P0 — Baseline Lock (opens with Wizard I)

```text
GUARD PHASE 0 — BASELINE LOCK. Modify no application code.
0. WIZARD I — ask me, in order, before anything else:
   W1 TRIGGER: routine hygiene / pre-release hardening / performance pain /
      post-incident cleanup?
   W2 SCOPE: whole repo / specific modules (which?) / hotspot list only?
      (Large repo or monorepo → recommend hotspot-first with staged expansion.)
   W4 SAFETY NET (your belief, per in-scope module): tests+golden masters /
      tests only / typecheck only / nothing?
   W6 DELIVERY: PR per task / PR per phase / single integration branch /
      direct commits to main?
   Write the provisional guard.config.json ("status": "provisional") and
   create GUARD-RUN.md from the template. Record every answer there.
1. Detect the stack (per package/workspace in a monorepo); record exact
   install/build/test/lint/start commands with real outputs in BASELINE.md.
2. Run build and full suite. On any failure, STOP and report with options; do
   not fix silently. Label each result VERIFIED with its exit code.
3. For the W2 scope, add characterization tests capturing CURRENT behavior
   (edge cases inferred from code, not docs). For output-producing modules,
   add golden masters. Scrub secrets/PII before committing.
4. PROVE THE NET: for each in-scope module, pick one characterization test,
   temporarily break the behavior, watch THAT named test go red, restore.
   Record each proof. Record verified net_status per module beside the W4
   belief — a discrepancy is a finding for Gate A.
5. Snapshot metrics (duplication, dead code, complexity, coverage, deps) with
   exact commands. Confirm each check acts on a non-empty subject.
Commit "chore(guard): baseline lock" (to the W6 delivery base), tag
guard-baseline-{DATE}. Update GUARD-RUN.md (phase: P0 done).
Report per module: green/red, net coverage, net-proof status, escalation zones.
```

## P1 — Deep Scan

```text
GUARD PHASE 1 — DEEP SCAN. Read-only. Scope: the W2 allow-list only.
First enumerate generated/vendored paths (build output, codegen, stubs,
vendored libs, migrations, minified files); record them in scope.deny and
exclude them from both tracks.
Run BOTH tracks into FINDINGS.raw.json:
TRACK 1 (deterministic): dead-code (knip/equivalent), duplication (jscpd ≥50
tokens/5 lines), complexity, dependency health, linters/typecheckers.
TRACK 2 (semantic): Fowler's smells plus the AI failure modes — swallowed-
failure catch-alls, impossible-case guards, premature abstraction, comment
pollution, duplication over reuse, hallucinated APIs, intent-less naming,
hardcoded success. Plus: near-duplicate utilities with different signatures,
speculative abstractions, inconsistent error idioms, phantom deps, comment/code
drift.
For EVERY Track-2 finding: quote code, cite file:lines, name the smell, propose
the MINIMAL refactoring, state what breaks if your reading is wrong, label the
claim VERIFIED/STATED/UNKNOWN. Flag every dynamic-usage pattern DYNAMIC-ZONE
(they get a dedicated register section in FINDINGS.triaged.md).
Summarize counts per lens (cleanliness/redundancy/optimization) per module.
Update GUARD-RUN.md (phase: P1 done).
```

## P2 — Evidence Triage + Gate A

```text
GUARD PHASE 2 — TRIAGE. Read-only.
For each finding in FINDINGS.raw.json:
1. Confidence: C3 (tool-verified, fix non-behavioral), C2 (two independent
   signals agree), C1 (single signal + you ran a confirming probe — show it),
   C0 (unverified hypothesis — report only, never plan code from it).
2. FALSIFY every negative claim before it can drive a change:
   - "dead/no callers": grep symbol AND string name; dynamic imports, DI
     registries, framework magic, plugin discovery, config wiring, templates.
   - "duplicate": read both fully; diff constants, rounding, error handling,
     null semantics. If they differ, the fix is PARAMETERIZE, never delete.
   - "unused dep": check scripts, build plugins, config refs, CLI, peer/optional.
   - "missing check": search alternate layers (DB, gateway, middleware, codegen).
   - "unreachable branch": enumerate the state space incl. failure, cancel,
     empty, and reload paths before believing no input reaches it.
   Record each falsification attempt and its outcome.
3. LIFECYCLE LENS: if a finding touches a data lifecycle, enumerate states and
   transitions including failure/cancel/empty/reload; route it to T3.
4. Tier from blast radius × net strength → T0/T1/T2/T3 with a minimum
   proof-rung (V2/V3/V4/V5). Data shape, external contracts, auth, and money
   logic are ALWAYS T3. Partial-net modules escalate one tier; no-net modules
   are frozen except net-building.
5. Reject or defer with reasons anything that fails falsification.
Write FINDINGS.triaged.md from the template (id, location, smell, confidence,
tier, proof-rung, falsification record, benefit, effort, evidence + the
DYNAMIC-ZONE register), lint it (guard_lint.py findings), then STOP and ask me
to approve / defer / reject each finding — this is GATE A. Record every
decision per finding ID in GUARD-RUN.md. Modify nothing until I approve.
```

## P3 — User Wizard II

```text
GUARD PHASE 3 — WIZARD II. With the Gate-A-approved findings in front of us:
W3 APPETITE: Conservative (T0–T1) / Balanced (+T2, per-change approval) /
   Accelerated (+T3, staged sign-off)?  [recommend Balanced]
W5 AUTONOMY: approve every task / every batch / plan-only then run with
   final report?
Then finalize guard.config.json ("status": "final") with all six answers as
enforceable constraints: path allow-list + deny-list, max tier, proof-rung
ceiling, approval cadence, delivery mode + base, frozen modules, verified
net_status. Validate it (guard_lint.py config), show me a plain-language
summary of what each choice means in practice, and update GUARD-RUN.md.
```

## P4 — Plan Synthesis + Gate B

```text
GUARD PHASE 4 — PLAN. Read-only.
From Gate-A-approved findings + guard.config.json, write PLAN.md:
1. RUN SUMMARY: baseline, approved findings by tier, expected measurable end
   state, explicit non-goals, net-proof status.
2. GLOBAL INVARIANTS: after every task — build green, suite green, GMs
   unchanged; one concern per commit; failure → revert + stop; claims labeled;
   no negative claim acted on without a falsification record.
3. TASK CARDS in dependency order (prereqs first, leaves first, T0/T1 quick
   wins front-loaded). Each card MUST have: id, tier, finding ref + confidence,
   falsification record (or "n/a — positive claim"), exact change, file
   allow-list, PROOF-RUNG with the specific revert-mutation or anchor, verbatim
   verify commands from BASELINE.md, rollback path, acceptance criteria — and
   for T2/T3 the extra protocol steps (golden-master diff review / flag +
   staged rollout with Off = old behavior).
4. Respect guard.config.json absolutely — nothing out of scope, nothing above
   max tier (overflow → "deferred" section).
Lint the plan (guard_lint.py plan PLAN.md) — an unlintable card is not a card.
Present a one-page plain-language risk brief. STOP for GATE B; record the
decision in GUARD-RUN.md. No application code changes until I approve.
```

## P5 — Guarded Execution

```text
GUARD PHASE 5 — EXECUTE task {TASK_ID} from PLAN.md.
Protocol, in order, logging to EXECUTION.log (timestamp | task | step | result):
1. Branch {BRANCH_NAME} from the latest green delivery base (per W6).
2. PRE-FLIGHT: run the card's verify commands; confirm they act on a non-empty
   subject and exit by code, not output text. If red or vacuous, STOP — report.
3. Implement exactly the card. Touch only its file allow-list.
4. Run verify commands. Diff golden masters. Run characterization tests.
   100% green required.
5. PROOF-RUNG: reach the card's rung — falsification record (V3), or revert the
   change and watch the NAMED test go red then restore (V4), or the anchor
   probe (V5). Done at the rung, not at "green".
6. Commit ONE atomic commit: "refactor({scope}): {change} [GUARD {TASK_ID}]".
7. Report per autonomy setting, with claim labels.
ON ANY FAILURE: revert immediately (never debug forward), log hypothesis, mark
blocked in GUARD-RUN.md, continue to next independent task or stop per
autonomy. Never weaken a gate to pass it; never run a suite concurrently with
another.
```

## P6 — Verify & Close-out

```text
GUARD PHASE 6 — CLOSE-OUT.
1. Run the FULL battery on the integration result: build, entire suite, all
   golden masters, typecheck, plus a smoke pass of primary flows if it runs.
2. ANCHOR the result where it matters: confirm the deployed service serves the
   new SHA, a real request returns the expected shape — a measurement, not a
   report. For a library/CLI that never deploys, use the offline anchor recipe
   (anchors.md): gate-anchor + a real invocation of the built artifact from a
   scratch consumer. Record ANCHORED / UNANCHORED / UNKNOWN; UNKNOWN blocks.
3. Re-measure every BASELINE.md metric with the same tools/commands.
4. Write DELTA.md from the template: (a) equivalence evidence with the RUNG
   each reached; (b) metrics baseline vs final vs target, each labeled
   VERIFIED/STATED/UNKNOWN; (c) residual register — deferred findings, T3 items
   behind flags with exit dates, temporary golden masters to retire,
   out-of-scope items; (d) what was NOT proven and where residual risk lives.
5. Mint any new field lessons from failures this run caused; close GUARD-RUN.md.
State deltas, not prose. Label every claim.
```
