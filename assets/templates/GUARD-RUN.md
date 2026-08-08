# GUARD-RUN.md — run state (keep current as you work, never at session end)

- Run ID: guard-YYYY-MM-DD-a
- Phase: P0-wizard-I
  <!-- one of: P0-wizard-I | P0 | P1 | P2 | gate-A | P3 | P4 | gate-B | P5 | P6 | closed -->
- Baseline tag: (set at P0)
- Config: guard.config.json (status: provisional | final)
- Started: YYYY-MM-DD HH:MM
- Last updated: YYYY-MM-DD HH:MM

## Wizard answers

| Q | Asked at | Answer | Notes |
|---|---|---|---|
| W1 trigger | Wizard I | | |
| W2 scope | Wizard I | | |
| W4 net (believed) | Wizard I | | verified net recorded at P0 below |
| W6 delivery | Wizard I | | |
| W3 appetite | P3 | | |
| W5 autonomy | P3 | | |

## Net status (verified at P0 vs W4 belief)

| Module | Believed (W4) | Verified (P0 proof) | Discrepancy → Gate A? |
|---|---|---|---|
| | | | |

## Gate A decisions (one row per finding — an unrecorded gate was not passed)

| Finding | accept / defer / reject | User note |
|---|---|---|
| F-001 | | |

- Gate A: (pending | approved YYYY-MM-DD HH:MM)

## Gate B

- Gate B: (pending | approved YYYY-MM-DD HH:MM, plan SHA/tree-hash: )

## P5 task ledger

| Task | Status (pending/green/blocked/reverted) | Commit | Rung reached |
|---|---|---|---|
| | | | |

## Resume instructions for a fresh session

Read this file, `guard.config.json`, and `BASELINE.md` first. Resume from the
phase above. Never re-run completed phases, never re-ask answered wizard
questions, never treat an unrecorded gate as passed.
