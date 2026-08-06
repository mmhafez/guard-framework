# FINDINGS.triaged.md — evidence-triaged findings for Gate A (P2)

Lint: `python3 scripts/guard_lint.py findings FINDINGS.triaged.md`
If the scan truly found nothing, write `NO-FINDINGS: <per-lens zero counts>` —
an empty report must say so out loud.

## Findings

| Id | Location | Smell | Confidence | Tier | Proof-rung | Falsification record | Benefit | Effort | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | src/x.ts:10-24 | duplicate | C2 (jscpd + LLM) | T1 | V3 | read both; constants identical; callers enumerated | −14 LOC | S | quote + tool output |

Confidence: C3 tool-verified · C2 two signals agree · C1 single signal + probe · C0 hypothesis (report only, never plan code from it).
Every negative claim ("dead", "duplicate", "unused", "missing", "unreachable") carries its falsification record, or it does not drive a change.

## DYNAMIC-ZONE register

Paths/patterns where static analysis is blind (dynamic imports, DI registries,
string-built symbols, plugin discovery, reflection, templates). Findings inside
a zone are capped at C1 and escalate one tier. Write "none flagged" if none.

| Zone | Pattern | Why static analysis is blind |
|---|---|---|
| | | |

## Rejected / not actionable (with reasons — so the user sees what was vetoed)

| Id | Claim | Why rejected (falsification outcome) |
|---|---|---|
| | | |

## Deferred (evidence parked for a future run)

| Id | Reason deferred |
|---|---|
| | |
