# DELTA.md — close-out report (P6). State deltas, not prose; label every claim.

## (a) Equivalence evidence — what was proven, at what RUNG

| Claim | Evidence | Rung reached | Label |
|---|---|---|---|
| Build + full suite green on integration result | exit codes | V1+V2 | VERIFIED |
| Golden masters unchanged | byte-diff, non-empty GM set confirmed | V2 (V4 where gate-proven) | VERIFIED |
| Net still catches (spot revert-mutations) | named tests went RED | V4 | VERIFIED |
| Deployed service serves new SHA / real request returns expected shape — or offline consumer-smoke anchor | direct probe output | V5 | ANCHORED / UNANCHORED / UNKNOWN |

UNKNOWN blocks close-out. An unanchored close-out says so in the first line.

## (b) Metrics — baseline vs final vs target (same tools, same commands)

| Metric | Baseline | Final | Δ | Target | Label |
|---|---|---|---|---|---|
| Duplicated blocks/lines % | | | | | VERIFIED |
| Dead files / exports / deps | | | | | VERIFIED |
| Cyclomatic p95 / max | | | | | VERIFIED |
| Coverage / mutation score (scoped) | | | | | VERIFIED |
| Bundle size / build time | | | | | VERIFIED |

## (c) Residual register

| Item | Kind (deferred finding / T3 behind flag / temporary GM / out of scope) | Owner | Exit date |
|---|---|---|---|
| | | | |

## (d) What was NOT proven, and where residual risk lives

- <paths with no net; claims still STATED; anchors not reachable; scope walls>

## Lessons minted this run (→ GUARD-LESSONS.md)

- GL-nn: <lesson> — <the failure that bought it> — MECHANISED / DOCTRINE / OUTSTANDING
