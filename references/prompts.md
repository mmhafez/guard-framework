# Master Prompt Suite (P0–P6)

Paste-ready phase prompts that drive any coding agent through the pipeline.
Fill `{slots}` per repo. P3 and P4 are the two user-control points.

## P0 — Baseline Lock

```text
GUARD PHASE 0 — BASELINE LOCK. Modify no application code.
1. Detect the stack; record exact install/build/test/lint/start commands with
   real outputs in BASELINE.md.
2. Run build and full suite. On any failure, STOP and report with options; do
   not fix silently. Label each result VERIFIED with its exit code.
3. For {SCOPE_DIRS}, add characterization tests capturing CURRENT behavior
   (edge cases inferred from code, not docs). For {OUTPUT_MODULES}, add golden
   masters. Scrub secrets/PII before committing.
4. PROVE THE NET: for each in-scope module, pick one characterization test,
   temporarily break the behavior, watch THAT named test go red, restore.
   Record each proof. A net never watched failing is not yet trusted.
5. Snapshot metrics (duplication, dead code, complexity, coverage, deps) with
   exact commands. Confirm each check acts on a non-empty subject.
Commit "chore(guard): baseline lock", tag guard-baseline-{DATE}.
Report per module: green/red, net coverage, net-proof status, escalation zones.
```

## P1 — Deep Scan

```text
GUARD PHASE 1 — DEEP SCAN. Read-only.
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
claim VERIFIED/STATED/UNKNOWN. Flag every dynamic-usage pattern DYNAMIC-ZONE.
Summarize counts per lens (cleanliness/redundancy/optimization) per module.
```

## P2 — Evidence Triage + Gate A

```text
GUARD PHASE 2 — TRIAGE. Read-only.
For each finding in FINDINGS.raw.json:
1. Confidence: C3 (tool-verified, fix non-behavioral), C2 (two independent
   signals agree), C1 (single signal + you ran a confirming probe), C0
   (unverified — report only, never plan code from it).
2. FALSIFY every negative claim before it can drive a change:
   - "dead/no callers": grep symbol AND string name; dynamic imports, DI
     registries, framework magic, plugin discovery, config wiring, templates.
   - "duplicate": read both fully; diff constants, rounding, error handling,
     null semantics. If they differ → PARAMETERIZE, never delete.
   - "unused dep": scripts, build plugins, config refs, CLI, peer/optional.
   - "missing check": alternate layers (DB, gateway, middleware, codegen).
   Record each falsification attempt and outcome.
3. LIFECYCLE LENS: if a finding touches a data lifecycle, enumerate states and
   transitions incl. failure/cancel/empty/reload; route to T3.
4. Tier from blast radius × net strength → T0/T1/T2/T3 with a minimum
   proof-rung (V2/V3/V4/V5). Data/contracts/auth/money ALWAYS T3. No-net
   modules escalate one tier.
5. Reject/defer with reasons anything failing falsification.
Write FINDINGS.triaged.md (id, location, smell, confidence, falsification
record, tier, proof-rung, benefit, effort, evidence). STOP for GATE A.
```

## P3 — User Wizard

```text
GUARD PHASE 3 — WIZARD. Ask me these six questions, in order; do not proceed
until all six are answered.
W1 TRIGGER: routine hygiene / pre-release hardening / performance pain /
   post-incident cleanup?
W2 SCOPE: whole repo / specific modules (which?) / hotspot list only?
W3 APPETITE: Conservative (T0–T1) / Balanced (+T2, per-change approval) /
   Accelerated (+T3, staged sign-off)?  [recommend Balanced]
W4 SAFETY NET: per in-scope module — tests+golden masters / tests only /
   typecheck only / nothing? ("nothing" modules get net-building FIRST and are
   otherwise frozen.)
W5 AUTONOMY: approve every task / every batch / plan-only then run + report?
W6 DELIVERY: PR per task / PR per phase / single integration branch / direct?
Then write guard.config.json (path allow-list, max tier, proof-rung ceiling,
approval cadence, delivery mode, frozen modules) and show me a plain-language
summary of what each choice means.
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
   falsification record (if negative), exact change, file allow-list,
   PROOF-RUNG with the specific revert-mutation or anchor, verbatim verify
   commands from BASELINE.md, rollback path, acceptance criteria.
4. Respect guard.config.json absolutely — nothing out of scope, nothing above
   max tier (overflow → "deferred" section).
Present a one-page plain-language risk brief. STOP for GATE B. No application
code changes until I approve.
```

## P5 — Guarded Execution

```text
GUARD PHASE 5 — EXECUTE task {TASK_ID} from PLAN.md.
Protocol, in order, logging to EXECUTION.log:
1. Branch {BRANCH_NAME} from latest green main.
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
blocked, continue to next independent task or stop per autonomy. Never weaken a
gate to pass it; never run a suite concurrently with another.
```

## P6 — Verify & Close-out

```text
GUARD PHASE 6 — CLOSE-OUT.
1. Run the FULL battery on the integration result: build, entire suite, all
   golden masters, typecheck, plus a smoke pass of primary flows if it runs.
2. ANCHOR the result where it matters: confirm the deployed service serves the
   new SHA, a real request returns the expected shape — a measurement, not a
   report. Record ANCHORED / UNANCHORED / UNKNOWN; UNKNOWN blocks.
3. Re-measure every BASELINE.md metric with the same tools/commands.
4. Write DELTA.md: (a) equivalence evidence with the RUNG each reached; (b)
   metrics baseline vs final vs target, each labeled; (c) residual register —
   deferred findings, T3 items behind flags with exit dates, temporary golden
   masters to retire, out-of-scope items; (d) what was NOT proven and where
   residual risk lives.
5. Mint any new field lessons from failures this run caused.
State deltas, not prose. Label every claim.
```
