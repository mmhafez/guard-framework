# GUARD Framework

**Deep, behavior-preserving analysis and optimization of AI-built repositories — driven by you, executed as a verified, reversible plan.**

GUARD (Ground truth → Uncover → Arbitrate → Roadmap → Deliver) turns any AI coding agent into a disciplined, behavior-preserving code analyst and optimizer. It exists to solve one problem: **repositories produced by AI agents accumulate duplication, dead code, and structural drift fast — but the same agent that could clean it up can't be trusted to do it unsupervised.**

GUARD's answer is a six-phase pipeline where **you drive**, **every change is verified to a named rung of proof**, and **every claim is labeled by how it's known.**

> Behavior is the product. A green check is a claim, not a proof. And the user — not the agent — decides what gets touched.

---

## Why GUARD?

- **AI-built code degrades measurably.** GitClear's analysis of 211M changed lines found an **~8× rise in duplicated code blocks** in 2024, with copy/pasted lines overtaking refactored lines for the first time.
- **AI review can't be trusted alone.** It carries a structural **5–15% false-positive rate**, and "the suite passed" is routinely evidence of nothing (a typecheck can exit 0 while blind to every file).
- **The fix isn't a better prompt — it's a governing protocol.** GUARD layers deterministic tools, LLM judgment, verification, and your authority into a pipeline that can't be bypassed by a confident-sounding agent.

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
P0 Baseline Lock ─▶ P1 Deep Scan ─▶ P2 Evidence Triage ─▶ [GATE A: approve findings]
     │                                                            │
     │                                                            ▼
P6 Close-out ◀─ P5 Guarded Execution ◀─ P4 Plan Synthesis ◀─ P3 User Wizard
     │                                        ▲
     └──────────────[GATE B: approve plan]────┘
```

| Phase | What happens | Your control point |
|-------|--------------|--------------------|
| **0 · Baseline Lock** | build/tests verified, characterization tests + golden masters capture current behavior, metrics snapshot, **net proven to catch** | — |
| **1 · Deep Scan** | dual-track: deterministic tools + LLM semantic review (cleanliness / redundancy / optimization) | — |
| **2 · Evidence Triage** | confidence class + risk tier per finding; **falsify every negative claim** | **Gate A** |
| **3 · User Wizard** | 6 questions compile into `guard.config.json` | you drive |
| **4 · Plan Synthesis** | dependency-ordered task cards with verify commands + rollback + proof-rung | **Gate B** |
| **5 · Guarded Execution** | one task → verify → atomic commit; auto-revert on failure | per-task/batch |
| **6 · Verify & Close-out** | **anchored** equivalence proof + metrics delta + residual register | sign-off |

## Install

GUARD is a portable instruction skill — no MCP server, no API key, no network access required. Just `SKILL.md` + `references/`.

**Option A — download the packaged skill** from the latest [Release](../../releases) (`guard-framework.skill`), and drop it into your agent's skill directory.

**Option B — build it from source:**

```bash
git clone https://github.com/mmhafez/guard-framework.git
cd guard-framework
bash build-skill.sh        # produces guard-framework.skill
```

**Option C — use it in place:** clone the repo and point your agent at `SKILL.md`, or paste the [Constitution](references/constitution.md) into your repo's `AGENTS.md` and drive the phases with the [prompts](references/prompts.md).

## Quick start

1. Paste the **GUARD Constitution** into the agent's rules.
2. **Run P0** (Baseline Lock) — expect 30–90 min of net-building on an untested repo, *including proving the net catches* (one revert-mutation per module).
3. **Run P1–P2** — review triaged findings at **Gate A**; read the **falsification records** on anything marked "dead" or "duplicate."
4. **Run P3** — choose the **Balanced** profile unless you have a reason otherwise.
5. **Run P4** — review `PLAN.md` at **Gate B**; confirm every T1+ card names a proof-rung.
6. **Run P5** per task; **Run P6** — read `DELTA.md`, confirm equivalence is **anchored**, approve the residual register.

## Repository layout

```
guard-framework/
├── SKILL.md                      # the skill entry point
├── build-skill.sh                # builds guard-framework.skill from source
├── agents/openai.yaml            # agent interface metadata
├── references/                   # load-on-demand reference docs (the skill body)
│   ├── constitution.md           #   standing rules to paste into a repo
│   ├── verification-ladder.md    #   the V0-V5 rungs + three pathologies
│   ├── anchors.md                #   measurement vs. report; UNKNOWN blocks
│   ├── falsification.md          #   disproving negative claims + lifecycle lens
│   ├── ai-failure-modes.md       #   the patterns generated code repeats
│   ├── prompts.md                #   the P0-P6 master prompt suite
│   ├── wizard.md                 #   the six questions and profiles
│   ├── plan-format.md            #   PLAN.md + task-card schema
│   ├── execution-rules.md        #   per-task protocol + hardening rules
│   ├── lessons-ledger.md         #   how to record numbered field lessons
│   └── multi-agent.md            #   optional independent-reviewer mode
└── docs/
    ├── GUARD-Framework.md        # the full framework playbook (v2.0)
    └── generate_figures.py       # regenerates the diagrams into docs/figures/
```

The packaged `guard-framework.skill` and the figure PNGs are attached to the
[latest release](../../releases) rather than committed, keeping the source tree
text-only and diff-friendly. Regenerate either locally: `bash build-skill.sh`
and `python3 docs/generate_figures.py`.

## What GUARD does NOT do

- Add features or change behavior you didn't explicitly approve.
- Debug a failing test or broken build.
- Run unattended past the two gates — **you are the operating authority.**
- Replace your linters/formatters/typecheckers — it's the judgment and safety layer above them.

## Full documentation

The complete framework — design rationale, per-phase procedures, the Master Prompt Suite, risk-communication guide, metrics & anti-gaming, the field-lessons ledger, failure modes, and the optional multi-agent execution mode — lives in **[`docs/GUARD-Framework.md`](docs/GUARD-Framework.md)**.

## License

[MIT](LICENSE)
