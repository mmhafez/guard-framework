# Optional multi-agent execution mode

For most repos a single disciplined agent running the pipeline is enough. But
T2/T3 work — cross-module consolidation, shared-code changes, anything touching
data or contracts — benefits from a property one agent cannot give itself: **an
independent verifier that did not write the code.** This optional mode adds it
without the full roster machinery.

## The principle: nobody grades their own homework

The strongest structural rule available: a reviewer must not share the author's
reasoning lineage — a model reviewing its own output is "a model agreeing with
its own reasoning," which passes silently because there is no disagreement to
notice. The agent that *implements* a T2/T3 change should not be the agent that
*reviews* it. A second model (different family) reviews the scoped diff,
adversarially hunting for failure rather than confirming success.

## The minimal graph

```
plan ──▶ implement ──▶ review ──pass──▶ verify(rung) ──pass──▶ commit
            ▲             │                 │
            └── fix ◀──fail──────────fail───┘
              (bounded rounds, then escalate to user)
```

Three rules make it safe:

- **The reviewer is read-only.** A reviewer that can fix stops judging.
- **Rounds are bounded** (default 3) with a declared exhaustion route (escalate
  to the user). An unbounded fix loop is how budgets burn.
- **The verdict is anchored.** The reviewer's PASS is bound to the exact commit
  SHA it reviewed, so a later change invalidates it; a review of an unmerged
  worktree is never presented as a merged PASS.

## The adversarial review lenses

The reviewer does not skim for style; it hunts four defect classes machine gates
historically miss, and must write a finding for each — **"none found" is a claim
the reviewer owns**, not silence:

1. **Silent success** — a path that reports success while producing nothing (a
   swallowed exception, an export that builds nothing, a button that no-ops).
2. **Code-exists ≠ capability-ships** — for every capability the diff claims,
   name its caller. One grep discharges it; the inverse (claiming no consumer
   when one exists) also fails.
3. **Mocking the layer whose configuration is wrong** — a mock can make a defect
   invisible. Assert the real configuration, negatively (a positive assertion
   passes even when the wrong value is also sent).
4. **Satisfiable by absence** — for each check, what would it do if its subject
   were entirely absent?

Plus the **lifecycle lens** for data work (see falsification.md) and the
**verification doctrine**: a negative test must go red when the fix is reverted;
assert the discriminating detail, not the error class; check each mock's return
shape against the real implementation's return statement.

## When to use it

| Signal | Single agent | Add a reviewer |
|---|---|---|
| Tier | T0–T1 | T2–T3 |
| Blast radius | module-internal | cross-module / data / contract |
| Net strength | mutation-proven | thin or partial |
| Cost of a mistake | a revert | outage, data loss, money |

The bar is real: a second engine costs tokens and coordination, and over-
spawning reviewers for work that never needed them is its own failure. Reach for
it when the cost of being wrong exceeds the cost of the review — which, for the
changes GUARD reserves for T2/T3, is exactly the case.
