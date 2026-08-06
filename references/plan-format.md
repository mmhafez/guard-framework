# PLAN.md format and task-card schema

Read at Phase 4. The plan is the deliverable: dependency-ordered, agent-
executable, human-readable. Ordering follows Mikado logic — prerequisites first,
leaf tasks first, low-tier high-value work front-loaded.

## Skeleton

```markdown
# PLAN.md — GUARD execution plan (v2)
## 0. Run summary
- Trigger (W1): …  Scope (W2): …  Profile (W3): …  Autonomy (W5): …
- Baseline: tag guard-baseline-DATE, build ✅, tests N ✅, duplication X%
- Net proof: <module> characterization net mutation-proven (V4) DATE
- Approved findings: N (T0:· T1:· T2:· T3:-deferred)
- Expected end state: duplication ≤ Y%, −Z LOC, zero behavior change

## 1. Global invariants
- After EVERY task: build green, suite green, golden masters unchanged
- One concern per commit; structure and behavior changes never mix
- Any verification failure → revert to last green, log, STOP and report
- Every claim labeled VERIFIED / STATED / UNKNOWN; UNKNOWN blocks
- No negative claim acted on without a falsification record

## 2. Task cards (execute in order)
### TASK-007 [T2] Consolidate duplicate currency formatters
- Finding: F-012 (C2: jscpd + LLM agree) — src/utils/money.ts vs src/billing/format.ts
- Falsification: read both; differ in ROUNDING → NOT clean duplicates
- Change: extract one parameterized formatCurrency(amount, {rounding})
- Touches: 4 files (listed)   Blast radius: cross-module (utils ↔ billing)
- Proof-rung: V4 (falsification recorded; revert-mutation below); per-change approval (T2)
- Verify: npm run build && npm test -- --grep "money|billing" && npm run gm:check
- Mutation-proof: revert rounding param → test_money_rounds_half_up goes RED → restore
- Rollback: git revert HEAD (single atomic commit)
- Acceptance: jscpd block F-012 gone; suite N/N green; GM diff reviewed & clean —
  any GM diff moving a monetary value → STOP for explicit user decision
```

## Task-card schema — every field mandatory

| Field | If omitted |
|---|---|
| Task ID + tier | protocol routing and approval cadence break |
| Finding ref + confidence | change is untraceable to evidence — an orphan edit |
| **Falsification record** (negative claims; else write "n/a — positive claim") | a wrong "dead/duplicate" claim deletes live code |
| Exact change description | vague instructions drift into scope leaks |
| File allow-list | agent "helpfully" fixes adjacent code |
| **Proof-rung (V2–V5)** | "works" becomes unfalsifiable |
| Verify commands | "done" is an opinion (copy verbatim from BASELINE.md) |
| **Mutation-proof / anchor** (V4/V5) | the net is assumed, never proven |
| Rollback path | a failed task becomes debugging on a broken tree |
| Acceptance criteria | "done" is the agent's opinion, not a checkable state |

## Machine check

Every card is machine-checked before Gate B:
`python3 scripts/guard_lint.py plan PLAN.md`. The linter fails on any card
missing a mandatory field — and fails on a plan with **zero** task cards,
because a check with no subject is not a check.

## Gate B

Present the plan with a one-page plain-language risk brief: what changes, in
what order, what could go wrong at each tier, the expected measurable end state,
and what the agent does autonomously vs. ask about. Record the decision in
`GUARD-RUN.md`. **Only after the user approves (Gate B) may any application
line be modified.**
