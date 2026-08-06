# The Verification Ladder

Read this at Phase 0 and again at every gate. It is the framework's core idea:
verification is not binary, and "green" is the bottom rung that counts.

A green signal is truthful about itself and can be worthless as evidence for the
thing it is cited for. A typecheck exiting 0 proves the typecheck ran — not that
it could see the code (a missing `@types/react` blinds it to every JSX prop
while still exiting 0). A "no dead callers" report proves the grep ran — not
that a plugin registry doesn't call the function by name at runtime.

## The six rungs

| Rung | Name | The question it answers | How established |
|---|---|---|---|
| V0 | Claim | "the agent says so" | nothing — the starting point, never the end |
| V1 | Ran | "did the check execute and exit 0?" | run it; capture the real exit code |
| V2 | Present & non-empty | "did the check have a subject?" | prove the subject exists, is non-empty, is routed |
| V3 | Falsification-survivor | "did we try to disprove it and fail?" | run the falsification move; record it |
| V4 | Mutation-proven | "would the net catch this if wrong?" | revert/break → named test RED → restore |
| V5 | Anchored | "does the world confirm it?" | a direct measurement: deployed SHA, bound port, real request |

## The three pathologies

**Satisfiable by absence (V2 defeats it).** A check that cannot distinguish
absent from correct is not a check. `git status | wc -l` → `0` reads "clean" but
is identical on failure. A green tick on a 404 is indistinguishable from the
endpoint existing. A tenant-isolation script that fails only when *both* tenants
are empty "proves" isolation while testing nothing. Rules: assert preconditions
(non-empty inputs, route routed, both sides non-trivial) before the subject;
test for the answer you want (`state == "clean"`), never against the one you
don't (`!= "dirty"`, which an absent field satisfies).

**A check that cannot fail (V4 defeats it).** A test that passes when the
behavior it names is deleted is worse than no test — it reports a capability
that does not exist. Proof of reachability is a revert-mutation: revert the
change (or introduce the defect), run, watch the *specific named case* go red,
restore. Name the case: "the suite went red" is satisfied by any case failing,
and a run can go red on the wrong case while the case under test stays green.

**A report about a measurement (V5 defeats it).** The gate reads the suite; the
suite reads fixtures; the review reads the diff; the monitor reads a status
file. Every loop watches another loop and none touches the ground — a circular
graph, internally consistent, verifying nothing. The fix is the anchor (see
[anchors.md](anchors.md)).

## Rung-to-tier routing

| Tier | Change | Min rung |
|---|---|---|
| T0 | delete verified-dead file/export, unused dep, private rename | V2 |
| T1 | in-module duplicate consolidation, split long function | V3 |
| T2 | cross-module consolidation, shared-utils | V4 |
| T3 | data schema, API payloads, auth, money | V5 |

## Two standing rules above the ladder

- **Budget the work, never the verification.** "Run the typecheck at most once
  at the end" gets obeyed exactly and ships unverified fixes. Narrow a check's
  scope, never its count.
- **A failed command must never read as a benign value.** `|| echo 0` turns a
  failed count into "nothing to do." Judge by exit code; sweep the *semantic
  class* — any command whose failure and whose negative answer are the same
  value to the caller.
