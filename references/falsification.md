# Falsification and the Lifecycle Lens

Read at Phase 2. This is the highest-value safety discipline in the framework:
before any negative claim drives a change, actively try to disprove it.

The negative claims a cleanup produces are exactly the ones that destroy repos
when wrong: "this is dead," "this has no callers," "these blocks are identical,"
"this check is missing." For each, run the specific falsification move and
record the attempt.

## The falsification moves

| Negative claim | The move (run it, record it) |
|---|---|
| "This function is dead" | grep the symbol **and** its string name; check dynamic imports, DI registries, framework magic exports, plugin discovery, reflection, config-driven wiring, template references. Look for it being *constructed* (factory strings), not just called. |
| "These blocks are duplicates" | read both in full; diff **constants, rounding, error handling, null semantics**. Token detectors normalize literals — "identical" may differ in one constant that matters. If they differ: *parameterize*, never *delete one copy*. |
| "This dependency is unused" | check package scripts, build plugins, config-file references, CLI invocations, peer/optional roles — not just `import` lines. Confirm with a clean install + production build, not only a test run. |
| "This validation/check is missing" | search alternate layers: DB schema constraints, API gateway, middleware, generated code, different naming. A "missing" check may live where you didn't look. |
| "This branch is unreachable" | enumerate the state space; prove no input reaches it — including failure, cancel, empty, and reload paths, where unreachable-looking code turns out to be load-bearing. |

A claim that survives falsification earns the right to be planned. A weakened
claim is downgraded or annotated, and the report says so.

**A false CLEAN verdict is more dangerous than a false finding.** A false
finding self-corrects — someone tries the fix and finds nothing. A false "this
is safe" is permanent because nobody revisits a boundary marked safe. So apply
the falsification pass, selectively, to findings that declare something *safe*.

## The lifecycle lens

When a finding touches a **data lifecycle** — records created, transformed,
deleted, reloaded — a diff-shaped review structurally cannot find the worst
defects, because they live in branches the diff does not contain. The canonical
field case: four distinct data-loss defects on one batch across three review
rounds, all past green CI, all one shape — **a state transition whose losing
branch was never walked** (regeneration destroying records on success, the *fix*
destroying records on failure/cancel, two records sharing an id after
normalization, deleting the last row resurrecting deleted rows because
`length > 0 ? canonical : legacy` gave "explicitly emptied" and "never
populated" the same representation).

The rule: for any lifecycle-touching change, **enumerate the states, enumerate
the transitions — including failure, cancellation, empty, and reload — and
require a written answer for each.** When a representation cannot distinguish
two outcomes the user can produce, no call-site care fixes it; make the illegal
state unrepresentable. Lifecycle findings route to T3 regardless of diff size.
