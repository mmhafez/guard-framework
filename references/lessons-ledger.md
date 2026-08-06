# The Field-Lessons Ledger

How the framework learns. Read at Phase 6 and whenever the framework itself
causes a failure.

Every rule in GUARD that looks arbitrary should be traceable to what it cost.
When the framework causes a failure — a false-positive deletion that slipped
through, a gate that passed on nothing, a plan that broke the build — mint it as
a **numbered lesson** in `GUARD-LESSONS.md` (kept in the repo, so a filling
context window costs nothing and the next run starts wiser).

## Three honest states

- **MECHANISED** — a script or emitted contract enforces it; name the mechanism.
- **DOCTRINE** — a standing rule with no cheap mechanism; say so plainly.
- **OUTSTANDING** — a proposed mechanism not yet built; name its owner.

## Governing commitments

- **A lesson appears once and is done.** If a class recurs after being absorbed,
  the recurrence is a failure of *the framework*, not the operator.
- **A lesson can be wrong.** When refuted, rewrite it with the true cause rather
  than deleting it — the mistake's *shape* is the durable part.
- **The ledger outlives the session.**

## Seed lessons (absorbed from the field record, re-expressed for cleanup)

| # | Lesson | State |
|---|---|---|
| GL-01 | A green gate is V1; it proves the check ran, not that the change is safe. Match rung to tier. | DOCTRINE |
| GL-02 | A check that cannot fail is worse than no check. Prove the net catches (revert-mutation). | DOCTRINE |
| GL-03 | "Dead code" is falsifiable. Grep the string name, not just the symbol, before deleting. | DOCTRINE |
| GL-04 | Token-identical blocks can differ in a constant that matters. Read both; parameterize, don't delete. | DOCTRINE |
| GL-05 | A failed command must never read as a benign value (`wc -l` → 0). Judge by exit code. | DOCTRINE |
| GL-06 | UNKNOWN is a verdict and it blocks. Never invent a confident answer to pass a gate. | DOCTRINE |
| GL-07 | A false CLEAN is permanent; a false finding self-corrects. Falsify the "safe" verdicts too. | DOCTRINE |
| GL-08 | Lifecycle defects live in failure/cancel/empty/reload branches a diff can't show. Enumerate transitions. | DOCTRINE |
| GL-09 | Don't weaken a gate to close a hole. Narrow scope, never assertion count. | DOCTRINE |
| GL-10 | Verify merges by content, not ancestry — squash merges break every graph check. | DOCTRINE |

Append new lessons as GL-11, GL-12, … with the failure that bought each.
