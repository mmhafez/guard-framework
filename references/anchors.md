# Anchors

The most important verification idea in the framework. Read at Phase 6 and
whenever closing a T2/T3 change.

Build the full verification graph — gates, reviews, monitors — and a harder
failure appears: every node consumes another node's report. The gate reads the
suite; the suite reads fixtures; the monitor reads a status file. **No loop
touches the ground.** That network is internally consistent and verifies
nothing. It fails exactly as a single unchecked loop fails, only later and with
more green lights on the way down.

Topology cannot fix this, because topology caused it. The graph needs **anchors**:
measurements that cannot be argued with because they came from the world rather
than from a dashboard. Ask of any evidence: *is this a measurement, or a report
about a measurement?*

## The five anchor kinds

Each is the ghost of a real near-miss. The probe is direct — not a status read.

| Anchor | The claim it grounds | The direct probe |
|---|---|---|
| `deploy` | "the fix shipped" | read the production alias; confirm it serves the **new SHA**, not the previous merge's |
| `runtime` | "the feature is live" | enumerate deployed modes; confirm the feature on the mode production *actually runs* |
| `endpoint` | "the service is ready" | make a **real request**; assert the response carries the expected key — not "control plane says ready" while nothing bound a port |
| `gate` | "the check is real" | break the subject, watch the gate fail, restore — proving the gate sees its defect class |
| `status` | "the PRs merged" | query for the answer you want (`state == 'closed'`), never the absence of the unwanted one |

## Three rules

1. **Three outcomes, never two.** `ANCHORED`, `UNANCHORED`, and `UNKNOWN`.
   Collapsing the third is the whole defect: a negative test against a
   possibly-absent field converts "no answer here" into a definite answer, and
   the definite answer it invents is the one that lets a gate pass. Say UNKNOWN
   out loud and let it **block**.
2. **Test for the answer you want, not against the one you don't.**
   `state == 'closed'` is safe; `state != 'open'` is satisfiable by absence.
3. **The anchor set is frozen.** An optimizing loop's strongest temptation is to
   weaken an anchor to make everything green. Loosening an anchor to unblock a
   delivery is not a shortcut — it is the failure.

## The standing tell

Every near-miss is one missing anchor wearing a different costume: a merge with
no production deploy, a feature live only on the mode production doesn't run, a
provider reporting ready while nothing bound a port, a typecheck exiting 0 while
blind to every prop, a poller reporting open PRs as merged. In all five the
green signal was **truthful about itself and worthless as evidence for the thing
it was cited for.**
