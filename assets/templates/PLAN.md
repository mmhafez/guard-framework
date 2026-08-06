# PLAN.md — GUARD execution plan

Lint before Gate B: `python3 scripts/guard_lint.py plan PLAN.md`

## 0. Run summary

- Trigger (W1): …  Scope (W2): …  Profile (W3): …  Autonomy (W5): …  Delivery (W6): …
- Baseline: tag guard-baseline-YYYY-MM-DD, build ✅, tests N ✅, duplication X%
- Net proof: <module> characterization net mutation-proven (V4) DATE
- Approved findings: N (T0:· T1:· T2:· T3:·) — per GUARD-RUN.md Gate A record
- Expected end state: duplication ≤ Y%, −Z LOC, zero behavior change
- Non-goals: …

## 1. Global invariants

- After EVERY task: build green, suite green, golden masters unchanged
- One concern per commit; structure and behavior changes never mix
- Any verification failure → revert to last green, log, STOP and report
- Every claim labeled VERIFIED / STATED / UNKNOWN; UNKNOWN blocks
- No negative claim acted on without a falsification record

## 2. Task cards (execute in order)

### TASK-001 [T1] <exact change, one concern>
- Finding: F-00x (confidence) — location(s)
- Falsification: <record for any negative claim, or "n/a — positive claim">
- Change: <exact, minimal>
- Touches: <file allow-list>   Blast radius: <leaf / module-internal / cross-module>
- Proof-rung: <V2 / V3 / V4 / V5> — <the specific proof owed>
- Verify: <commands VERBATIM from BASELINE.md>
- Mutation-proof: <T2+: revert X → named test Y goes RED → restore> (or Anchor: <probe>)
- Rollback: git revert HEAD (single atomic commit)
- Acceptance: <checkable end state, not an opinion>

## 3. Deferred (above max tier or out of scope — parked with evidence)

| Finding | Why deferred |
|---|---|
| | |
