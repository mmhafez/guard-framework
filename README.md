# GUARD Framework

**Deep, behavior-preserving analysis and optimization of AI-built repositories — driven by you, executed as a verified, reversible plan.**

GUARD (Ground truth → Uncover → Arbitrate → Roadmap → Deliver) turns any AI coding agent into a disciplined, behavior-preserving code analyst and optimizer. It exists to solve one problem: **repositories produced by AI agents accumulate duplication, dead code, and structural drift fast — but the same agent that could clean it up can't be trusted to do it unsupervised.**

GUARD's answer is a gated pipeline (P0–P6) where **you drive**, **every change is verified to a named rung of proof**, and **every claim is labeled by how it's known.**

> Behavior is the product. A green check is a claim, not a proof. And the user — not the agent — decides what gets touched.

---

## Why GUARD?

- **AI-built code degrades measurably.** GitClear found blocks of 5+ duplicated lines up **~8× during 2024**, with copy/pasted lines overtaking refactored lines for the first time — and its 2026 follow-up (623M analyzed changes) shows duplication at an all-time high (+81% since 2023) while refactored "moved" code collapsed to **3.8%** of changes.
- **AI review can't be trusted alone.** Even the best pipelines report **5–15% false-positive rates**, and "the suite passed" is routinely evidence of nothing (a typecheck can exit 0 while blind to every file).
- **The fix isn't a better prompt — it's a governing protocol.** GUARD layers deterministic tools, LLM judgment, verification, and your authority into a pipeline that can't be bypassed by a confident-sounding agent — and as of v2.1, the framework's own rules are mechanised: a config schema, artifact templates, a run-state file, and a linter that fails on an empty subject.

## The core idea: the Verification Ladder

Every safety gate in GUARD routes through one rung. **"Green" is only the bottom rung that counts.**

| Rung | Name | Established by | Required for |
|------|------|----------------|--------------|
| **V0** | Claim | nothing — a claim is not evidence | nothing |
| **V1** | Ran | command executed, exit 0 | *(never sufficient alone)* |
| **V2** | Present & non-empty | the check's subject exists and is non-trivial | T0 |
| **V3** | Falsification-survivor | tried hard to disprove a negative claim; failed | T1 |
| **V4** | Mutation-proven | revert/break → the **named** test goes RED | T2 |
| **V5** | Anchored | a measurement from the world, not a report about one | T3 |

This kills the three ways "verified" cleanups silently break things:

- **Satisfiable by absence** — a check that can't distinguish "absent" from "correct" (e.g. `git status | wc -l` → `0` on failure reads as "clean").
- **A check that cannot fail** — a test that passes when the behavior it names is deleted.
- **A report about a measurement** — a chain of green reports where no loop touches the ground.

## The pipeline

```
Wizard I (W1 W2 W4 W6) ─▶ P0 Baseline ─▶ P1 Scan ─▶ P2 Triage ─▶ [GATE A]
 intent · scope · nets · delivery                                     │
                                                                      ▼
 P6 Close-out ◀── P5 Execution ◀── [GATE B] ◀── P4 Plan ◀── P3 Wizard II (W3 W5)
                                                             appetite · autonomy
```

The wizard is split on one principle — **facts first, judgment after evidence**: trigger, scope, believed safety net, and delivery mode are asked *before* P0 (the phases consume them); change appetite and autonomy are asked at P3, while you're looking at the triaged findings. Run state lives in `GUARD-RUN.md` — a fresh session resumes from it, and an unrecorded gate was not passed.

| Phase | What happens | Your control point |
|-------|--------------|--------------------|
| **0 · Baseline Lock** | Wizard I, then build/tests verified, characterization tests + golden masters capture current behavior, metrics snapshot, **net proven to catch** | Wizard I |
| **1 · Deep Scan** | dual-track: deterministic tools + LLM semantic review, scoped, generated/vendored code excluded | — |
| **2 · Evidence Triage** | confidence class + risk tier per finding; **falsify every negative claim** | **Gate A** |
| **3 · Wizard II** | appetite + autonomy against the evidence → final `guard.config.json` (schema-validated) | you drive |
| **4 · Plan Synthesis** | dependency-ordered task cards with verify commands + rollback + proof-rung; **machine-linted** | **Gate B** |
| **5 · Guarded Execution** | one task → verify → atomic commit; auto-revert on failure | per-task/batch |
| **6 · Verify & Close-out** | **anchored** equivalence proof + metrics delta + residual register | sign-off |

## Install

GUARD is a portable instruction skill — no MCP server, no API key, no network access required.

**Option A — build the packaged skill** (one command, validates then produces `guard-framework.skill`):

```bash
git clone https://github.com/mmhafez/guard-framework.git
cd guard-framework
bash build-skill.sh        # validates frontmatter, sync, templates; produces guard-framework.skill
```

Then drop `guard-framework.skill` into your agent's skill directory (or upload it in the Claude app under Settings → Capabilities → Skills).

**Option B — use it in place:** clone the repo and point your agent at `SKILL.md`, or paste the [Constitution](references/constitution.md) into your repo's `AGENTS.md` and drive the phases with the [prompts](references/prompts.md).

## Quick start

1. Paste the **GUARD Constitution** into the agent's rules; copy `assets/templates/GUARD-RUN.md` into the repo.
2. **Run P0** — it opens with Wizard I (trigger, scope, believed net, delivery). Expect 30–90 min of net-building on an untested repo, *including proving the net catches* (one revert-mutation per module). Small repo, low appetite? Take the express path.
3. **Run P1–P2** — review triaged findings at **Gate A**; read the **falsification records** on anything marked "dead" or "duplicate"; decisions are recorded per finding in `GUARD-RUN.md`.
4. **Run P3** — answer appetite + autonomy (choose **Balanced** unless you have a reason otherwise).
5. **Run P4** — review `PLAN.md` at **Gate B**; `guard_lint.py plan` has already checked every card names its proof-rung.
6. **Run P5** per task; **Run P6** — read `DELTA.md`, confirm equivalence is **anchored**, approve the residual register.

## Repository layout

```
guard-framework/
├── SKILL.md                        # the skill entry point
├── build-skill.sh                  # validates + builds guard-framework.skill
├── agents/openai.yaml              # cross-agent interface metadata (OpenAI skill convention)
├── scripts/
│   └── guard_lint.py               # mechanised checks: config · plan · findings · run-state · sync
├── assets/templates/               # copy-ready run artifacts
│   ├── GUARD-RUN.md                #   run state + gate decisions (resumability)
│   ├── BASELINE.md · FINDINGS.triaged.md · PLAN.md · DELTA.md · GUARD-LESSONS.md
│   └── guard.config.example.json
├── references/                     # load-on-demand reference docs (the skill body)
│   ├── constitution.md             #   standing rules to paste into a repo
│   ├── verification-ladder.md      #   the V0-V5 rungs + three pathologies
│   ├── anchors.md                  #   measurement vs. report; offline anchors; UNKNOWN blocks
│   ├── falsification.md            #   disproving negative claims + lifecycle lens
│   ├── ai-failure-modes.md         #   the patterns generated code repeats
│   ├── prompts.md                  #   the P0-P6 master prompt suite (single source of truth)
│   ├── wizard.md                   #   the six questions, the split, profiles, sizing
│   ├── plan-format.md              #   PLAN.md + task-card schema
│   ├── execution-rules.md          #   per-task protocol + hardening rules
│   ├── lessons-ledger.md           #   numbered field lessons + mechanisation register
│   ├── multi-agent.md              #   optional independent-reviewer mode
│   └── guard.config.schema.json    #   the config contract
└── docs/
    ├── GUARD-Framework.md          # the full framework playbook (v2.1, diagrams render on GitHub)
    └── generate_figures.py         # optional PNG export of the diagrams (docs/figures/, gitignored)
```

The packaged `guard-framework.skill` is a build artifact, kept out of the source tree. The playbook's diagrams are Mermaid — they render natively on GitHub and stay text-only and diff-friendly; `generate_figures.py` exports PNG versions for print if you want them.

## What GUARD does NOT do

- Add features or change behavior you didn't explicitly approve.
- Debug a failing test or broken build.
- Run unattended past the two gates — **you are the operating authority.**
- Replace your linters/formatters/typecheckers — it's the judgment and safety layer above them.

## Full documentation

The complete framework — design rationale, per-phase procedures, the Master Prompt Suite, risk-communication guide, metrics & anti-gaming, the field-lessons ledger, failure modes, and the optional multi-agent execution mode — lives in **[`docs/GUARD-Framework.md`](docs/GUARD-Framework.md)**.

## License

[MIT](LICENSE)
