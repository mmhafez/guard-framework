# The GUARD Framework
## A User-Driven, Zero-Breakage Framework for Deep Analysis and Optimization of AI-Built Repositories

**Version 2.0 — August 2026**
*Strengthened with field-hardened mechanisms absorbed from two operational skill packages: a multi-engine orchestration ledger (~150 numbered lessons, each bought by a real failure) and a spec-vs-build auditor's falsification discipline.*

---

## Executive Summary

**GUARD** (Ground truth → Uncover → Arbitrate → Roadmap → Deliver) is a six-phase operating framework that turns any AI coding agent into a disciplined, behavior-preserving code analyst and optimizer. It targets a specific, measurable problem: repositories produced by AI agents accumulate duplication, dead code, and structural drift faster than human-written ones — GitClear's analysis of **211 million changed lines** recorded an **eightfold rise in duplicated code blocks** in 2024, with copy/pasted lines overtaking refactored lines for the first time [^54^][^60^] — yet the same agents that could clean this up cannot be trusted to do it unsupervised, because AI code review carries a structural **5–15% false-positive rate** and fluent-but-wrong output is the norm, with developer trust in AI accuracy falling to **33%** in 2025 [^27^][^58^].

Version 1.0 built the skeleton: lock the baseline, scan on dual tracks, triage by evidence, let the user drive through a wizard, execute in verified atomic steps. **Version 2.0 hardens the skeleton's load-bearing joints**, because v1's gates shared one quiet flaw — they treated "the checks ran green" as proof of safety. Field experience says otherwise: a gate can be green while a typecheck is blind to every JSX prop, while a "dead" function is called through a plugin registry, while a test passes against a function that returns a canned success. The v2.0 upgrades close exactly these holes.

| # | Commitment | Mechanism (v2 additions in **bold**) |
|---|---|---|
| 1 | Nothing changes until behavior is locked | Phase 0 baseline + characterization tests + golden masters + **mutation-proof that the net actually catches** |
| 2 | No finding is acted on without evidence | Dual-track scan, confidence scoring, **a falsification pass that tries to disprove every negative claim** |
| 3 | The user owns every consequential decision | Six-question wizard → `guard.config.json`; two approval gates; **every claim labeled VERIFIED / STATED / UNKNOWN** |
| 4 | Every change is small, verified, reversible | Risk tiers T0–T3, atomic commits, auto-revert, **a verification ladder (V0–V5) matched to tier — "green" is only V1** |
| 5 | Claims terminate at the world, not at a report | **Anchors: a measurement, never a report about a measurement; UNKNOWN blocks rather than inventing an answer** |
| 6 | The framework learns from its own failures | **A numbered field-lessons ledger; a recurring defect class is recorded as a failure of the framework, not the agent** |
| 7 | Output is a plan an agent executes verbatim | `guard.config.json` + `PLAN.md` task cards with verify commands, rollback, and **the proof-rung each task must reach** |

The first half of this document is the operating playbook (§1–§10). The second half is the execution machinery: the complete **Master Prompt Suite** (§12), the **risk-communication** guide (§13), **metrics and anti-gaming** (§14), the **field-lessons ledger** (§15), **failure modes** (§16), an **optional multi-agent execution mode** for high-risk work (§17), and a quick-start (§18).

---

## 1. Why AI-Built Repositories Need a Dedicated Framework

### 1.1 The pathology is measurable, not hypothetical

Code produced with AI assistance degrades along specific, measurable axes. GitClear's longitudinal research across 211 million changed lines (2020–2024) found that in 2024 **copy/pasted lines exceeded moved (refactored) lines for the first time in history**, and the frequency of commits containing a duplicated five-or-more-line block rose roughly **tenfold versus two years earlier** [^54^][^60^]. Refactored code as a share of all changes collapsed from 25% in 2021 to **under 10% by 2025** [^58^]. Duplicated code is not cosmetic: cloned blocks carry **15–50% more defects**, because a fix applied to one copy routinely misses its siblings [^50^]. Microsoft's churn research adds the second axis: files in the **top 10% of churn contain five times more defects** [^37^]. And an analysis of 153 million lines concluded that AI-generated output "resembles that of a developer unfamiliar with the projects they are altering," corroding DRY-ness because the assistant cannot reliably reuse existing code [^62^].

![Commits containing a duplicated code block rose ~10× in two years](figures/fig1-duplication-surge.png)

Beyond duplication, generated code repeats a recognizable set of semantic failure modes that linters cannot see: broad catch-all handlers that swallow failures, defensive guards for impossible cases, premature abstraction, hallucinated APIs and packages, hardcoded "success" returns, and plausible-but-wrong logic that compiles and reads correctly while encoding a subtly wrong boundary or null semantic [^27^]. Spracklen et al. measured that **~20% of package references recommended by LLMs are fabricated** across 16 models [^27^]. These are the defects a cleanup framework must both avoid introducing and actively surface — and they are precisely why "let the AI that made the mess clean it up" needs a governing protocol rather than a prompt.

### 1.2 The cleaner cannot be trusted to clean unsupervised

AI code review produces false positives at a structural **5–15% rate**; 66% of developers cite "almost right, but not quite" as their top frustration, and trust in AI accuracy fell to **33%** in 2025 [^27^][^58^]. The credible mitigations are consistent: retrieval grounding, guardrails, and verification layers cut hallucinations dramatically (a Stanford study reports **96%** reduction), and hybrid static-analysis-plus-LLM pipelines reach precision figures neither approach achieves alone [^27^]. The architecture that works is **layered** — deterministic analysis first, LLM judgment second, verification third, human authority last [^27^][^31^]. GUARD institutionalizes that layering as an enforceable pipeline, then v2.0 adds the missing ingredient the layering alone does not provide: a way to tell a *real* verification from a *plausible-looking* one.

### 1.3 Refactoring science already solved "don't break it" — for humans

The safety half of GUARD adapts two decades of discipline. Michael Feathers defines legacy code as **code without tests** and prescribes: find change points, find test points, break dependencies, cover with **characterization tests** that capture what code *actually* does, and only then refactor — never outside test-covered code [^6^][^9^]. For changes too large for one safe step, the industry converged on the **Strangler Fig**, **Branch by Abstraction**, **Parallel Run**, and **expand-and-contract** patterns [^1^][^3^][^66^], and on the **Mikado Method** — attempt the change, record what breaks as prerequisites, **revert everything**, work the leaves first, staying always-green [^64^][^65^]. GUARD's contribution is wiring these human disciplines into an agent-executable protocol with explicit user control points, then hardening the verification layer so that "green" actually means safe.

---

## 2. Design Principles

Eight principles govern every phase; §12 embeds them verbatim into the agent's standing instructions.

**P1 — Behavior preservation outranks cleanliness.** A finding is actionable only if fixing it provably preserves observable behavior. When specification and actual behavior disagree, actual behavior wins, because that is what users depend on [^6^].

**P2 — Evidence before action, and falsification before trust.** Every finding carries an evidence class, and every *negative* claim (this is dead, this has no callers, this is missing) must survive an explicit attempt to disprove it before it can drive a deletion. This is the discipline that kills false-positive removals — the single most dangerous action in any cleanup.

**P3 — The user is the operating authority.** Scope, risk appetite, autonomy, and every elevated-risk change are decided by the user through the wizard and two hard gates, mirroring the spec-driven consensus that gated checkpoints prevent "house of cards" code [^25^][^29^].

**P4 — Small batches, always green.** One task, one concern, one atomic commit. On any verification failure the agent reverts to the last green state instead of debugging forward [^64^][^72^].

**P5 — A claim is labeled by how it is known.** Every statement the framework makes about the code is tagged **VERIFIED** (established by running something), **STATED** (asserted from reading, not yet run), or **UNKNOWN** (the environment could not determine it). UNKNOWN is a real verdict and it **blocks**; collapsing it into a confident-sounding answer is how gates get passed on nothing.

**P6 — Verification has a ladder, and "green" is the bottom rung that counts.** A command that ran (V1) is not evidence the check works (V2–V4) or that the world changed (V5). Each risk tier has a minimum rung (§4.4). The most dangerous sentence in software is "the suite passed."

**P7 — Claims terminate at anchors.** A report about a measurement is not a measurement. Where it matters, verification must touch the world directly — the deployed alias serves the new SHA, the endpoint binds a port, the named test goes red when the change is reverted — not just consume another green report.

**P8 — The framework degrades gracefully and learns.** No tests, no build, no CI → GUARD shifts weight into Phase 0 rather than refusing [^6^]. And every failure the framework itself causes is recorded as a numbered lesson; a lesson class that recurs is a defect in the framework, not the operator (§15).

---

## 3. Framework Overview

GUARD runs as a one-way pipeline with two mandatory user gates and one verification loop. No phase may be skipped; each phase's exit criteria are the next phase's entry ticket.

![The GUARD pipeline: six phases, two user gates, one verification loop](figures/fig2-guard-pipeline.png)

| Phase | Name | Core question | Key artifacts | Gate / proof |
|---|---|---|---|---|
| 0 | **Baseline Lock** | "What does the system do today, and how would we know if it stopped?" | `BASELINE.md`, characterization tests, golden masters, metrics, clean tag | **Net is mutation-proven** |
| 1 | **Deep Scan** | "Where is the code unclean, redundant, or suboptimal?" | `FINDINGS.raw.json` (tools + LLM, dual-track) | — |
| 2 | **Evidence Triage** | "Which findings are real, and how dangerous is each fix?" | `FINDINGS.triaged.md`, confidence + tier + **falsification result** | **Gate A** |
| 3 | **User Wizard** | "What does the user want, under what constraints?" | `guard.config.json` | — |
| 4 | **Plan Synthesis** | "In what order, verified how, does each change land?" | `PLAN.md` task cards, **each with a required proof-rung** | **Gate B** |
| 5 | **Guarded Execution** | "Did this one change preserve behavior? Prove it." | Atomic commits, per-task logs, `EXECUTION.log` | Per-task/batch (W5) |
| 6 | **Verify & Close-out** | "Is the whole provably equivalent — and measurably better?" | `DELTA.md` with **anchored equivalence evidence** | User sign-off |

The pipeline is linear up to Gate B and iterative after it: execution loops task-by-task through verification, and any mismatch routes back to re-triage rather than being force-fit [^29^][^32^]. The v2.0 difference from a naive gated workflow is that every gate's definition of "passing" is specified as a rung on the verification ladder, not as the word "green."

---

## 4. The Verification Ladder (new in v2.0)

This is the conceptual heart of the v2.0 upgrade, and it is the single most important thing the absorbed field record teaches. Every safety gate in software eventually reduces to a check that returns green. The field lesson — learned across container restarts, phantom test failures, and a production deploy that served the wrong SHA — is that **a green signal is truthful about itself and can be worthless as evidence for the thing it is cited for.** A typecheck exiting 0 is truthful *about the typecheck having run*; it says nothing about whether the typecheck could see the code (a missing `@types/react` makes it blind to every JSX prop while still exiting 0). A "no dead callers" report is truthful about the grep having run; it says nothing about the plugin registry that calls the function by name at runtime.

The fix is to stop treating verification as binary and start treating it as a ladder of increasing strength, where each rung answers a harder question than the one below.

![The Verification Ladder: from a bare claim (V0) to an anchored measurement (V5)](figures/fig6-verification-ladder.png)

### 4.1 The six rungs

| Rung | Name | The question it answers | How it is established |
|---|---|---|---|
| **V0** | Claim | "The agent says so." | Nothing. A claim is not evidence; it is the *starting point* for verification. |
| **V1** | Ran | "Did the check execute and exit 0?" | Run the command; capture its real exit code and output. |
| **V2** | Present & non-empty | "Did the check actually have a subject?" | Prove the check is not *satisfiable by absence*: the file exists, the tree is non-void, the route is routed, the input is non-empty. |
| **V3** | Falsification-survivor | "Did we try hard to disprove it and fail?" | For a negative claim, actively search for the counterexample (dynamic refs, alternate names, generated code, another layer). |
| **V4** | Mutation-proven | "Would the net *catch* this if it were wrong?" | Revert or deliberately break the change; watch the **named** test go **red**; restore. |
| **V5** | Anchored | "Does a measurement from the world confirm it?" | Touch reality directly: the deployed alias, a bound port, a real request's response shape, a DB object present by marker count. |

### 4.2 The three pathologies the ladder kills

**Satisfiable by absence (defeated by V2).** A check that cannot distinguish "absent" from "correct" is not a check. `git status | wc -l` returning `0` reads as "clean tree" but is identical when `git status` *failed*. A verifier printing a green tick on a 404 is indistinguishable from the endpoint existing. A tenant-isolation script that only fails when *both* tenants are empty "proves" isolation while testing nothing. The rule: **every check asserts its own preconditions before it asserts its subject** — non-empty inputs, the route actually routed, both sides of a comparison non-trivial. And **test for the answer you want, never against the one you don't**: `state == "clean"` is safe; `state != "dirty"` is satisfiable by absence (an absent field, an error envelope, and a null all satisfy it).

**A check that cannot fail (defeated by V4).** A test that passes when the behavior it names is deleted is worse than no test, because it reports a capability that does not exist. The proof of reachability is a **revert-mutation**: revert the change (or introduce the defect), run, and watch the *specific named case* go red, then restore. Naming the case matters — "the suite went red" is satisfied by *any* case failing, and a mutation run can go red on the wrong case while the case under test stays green. This is the same discipline as mutation testing (Stryker, mutmut), but applied surgically and cheaply to the exact change at hand rather than as a whole-repo score [^48^][^51^].

**A report about a measurement (defeated by V5).** The gate reads the suite; the suite reads fixtures; the review reads the diff; the monitor reads a status file. Every loop can watch another loop while **no loop touches the ground** — a circular graph that is internally consistent and verifies nothing. The correction is the **anchor**: a measurement that cannot be argued with because it came from the world rather than from a dashboard.

![Circular verification vs. anchored verification](figures/fig5-anchors.png)

### 4.3 Anchors, and the third verdict

An anchor is the terminal node of a claim — the point where the chain of "X reports Y" ends in a direct observation of the world. The five canonical anchors, each one the ghost of a real near-miss:

| Anchor kind | The claim it grounds | The direct probe (not a report) |
|---|---|---|
| `deploy` | "the fix shipped" | read the production alias; confirm it serves the **new SHA**, not the previous merge's |
| `runtime` | "the feature is live" | enumerate the deployed modes and confirm the feature on the mode production *actually runs* (not only the inline path) |
| `endpoint` | "the service is ready" | make a **real request** and assert the response carries the expected key — not "the control plane says ready" while nothing bound a port |
| `gate` | "the check is real" | break the subject, watch the gate fail, restore — proving the gate can see its defect class |
| `status` | "the PRs merged" | query for the answer you want (`state == 'closed'`), never the absence of the unwanted one |

Anchors have **three outcomes, never two**: `ANCHORED`, `UNANCHORED`, and **`UNKNOWN`**. The third is the whole point. A negative test against a possibly-absent field converts "there is no answer here" into a definite answer, and the definite answer it invents is the one that lets a gate be passed. UNKNOWN must be said out loud and must **block** — because a check that could not tell is not a pass. Finally: **the anchor set is frozen.** An optimizing loop's strongest temptation is to weaken an anchor to make everything green; loosening an anchor to unblock a delivery is not a shortcut, it is the failure.

### 4.4 Mapping rungs to risk tiers

The ladder is not decorative — it sets the *minimum* proof each tier of change must reach before it counts as done. This is the routing table that replaces "be careful."

| Tier | Change examples | Minimum rung to close | What that means in practice |
|---|---|---|---|
| **T0** mechanical-safe | delete tool-verified dead file, remove unused dep, rename private symbol | **V2** | build+typecheck+suite green, *and* the deletion target proven non-empty / the dep proven actually present first |
| **T1** standard | consolidate in-module duplicates, split a long function | **V3** | every "these are duplicates / this is unreachable" claim survives a falsification probe; characterization tests green |
| **T2** elevated | cross-module consolidation, shared-util changes | **V4** | revert-mutation: the named boundary test goes red when the change is reverted; golden-master diff reviewed |
| **T3** critical | data schema, API payloads, auth, money | **V5** | coexistence + flag (Off=old) + staged rollout, closed only by an anchor (deploy/runtime/endpoint), never by a status report |

Two rules sit above the table. **Budget the work, never the verification**: a brief that says "the typecheck is slow, run it at most once at the end" will be obeyed exactly, and has shipped unverified fixes — narrow a check's *scope*, never its *count*. And **a failed command must never read as a benign value**: `|| echo 0` turns a failed count into "nothing to do," so the semantic class — any command whose failure and whose negative answer are the same value — must be swept, not just the syntax last fixed.

---

## 5. Phase 0 — Baseline Lock (upgraded)

### 5.1 Purpose and non-negotiables

The Baseline Lock answers Feathers' question — "if I change this, how do I know I didn't break anything?" — before any optimization is proposed [^9^]. Its output is a frozen reference point: a git tag, a green build, a behavior-capturing test layer, and a metrics snapshot. Nothing downstream may proceed against a red or unknown baseline, because a failing baseline makes verification meaningless — the agent can no longer distinguish "I broke it" from "it was already broken."

v2.0 adds one hard requirement that v1 only implied: **the safety net must be proven to catch, not just to exist.** A suite that passes is V1. Before any T2+ work, the net covering that code must reach V4 — revert-mutation proof that a named test goes red when the behavior is broken. A net that has never been watched failing is an assumption, not a safety net.

The phase runs four workstreams in order. **Environment discovery** — record install/build/test/lint/start commands with their real outputs in `BASELINE.md`. **Stability check** — build and existing tests must pass; failures are documented and the user decides whether to fix first or characterize around them. **Behavior capture** — characterization tests and golden masters for in-scope modules [^53^][^56^]. **Metrics snapshot** — duplication, complexity, dead code, coverage, dependency inventory, so Phase 6 can prove improvement numerically [^37^].

### 5.2 The behavior-capture toolkit (with proof obligations)

| Instrument | Best for | Strength | Known limit | Proof obligation (v2) |
|---|---|---|---|---|
| Characterization tests | logic-heavy functions | pinpoints *which* behavior changed | labor-intensive | each must fail when its behavior is broken (spot-mutate one) [^9^] |
| Golden master / approval | reports, serializers, HTML, JSON | whole-output equivalence in one diff | fossilizes detail if never retired [^56^] | prove the harness detects a deliberate output change [^53^] |
| API contract tests | HTTP/RPC boundaries | guards the consumer-visible surface | says nothing about internals | assert preconditions (route routed, payload non-empty) |
| Property-based tests | parsers, pure logic | explores input space | properties inferred from behavior | seed must reproduce a found failure |
| Type check / build | everything, always | cheapest regression signal | types ≠ behavior | confirm the checker can see the files (no silent skip) |
| Mutation score (scoped) | critical paths pre-T2+ | proves the net bites | compute-costly; run scoped [^48^] | report the score band, not a vibe [^51^] |

Golden masters must be **scrubbed of secrets and PII before commit** [^56^]. Coverage alone is not evidence of a working net — it measures which lines execute, not whether tests would fail if those lines were wrong; a suite can report 100% coverage while surviving mutants prove it asserts nothing [^48^]. For any module slated for T2/T3, run a scoped mutation check and treat a score under ~60% as "net too weak — strengthen tests first" [^48^][^49^].

**The v2 gate-proof addition:** for each module entering scope, pick one representative characterization test and *prove* it — temporarily break the behavior, watch the named test go red, restore. Record the proof in `BASELINE.md` next to the metric. This converts the net from V1 to V4 before it is ever relied on.

### 5.3 Metrics to snapshot

| Metric | JS/TS tool | Python tool | Healthy target | Why |
|---|---|---|---|---|
| Duplicated lines/blocks % | jscpd (≥50 tokens, ≥5 lines) [^21^] | jscpd / PMD CPD [^15^] | < 3–5% | #1 AI-era pathology [^60^] |
| Dead files/exports/deps | Knip [^16^] | vulture, autoflake, pylint [^37^] | 0 unresolved | bundle size, misdirection [^24^] |
| Cyclomatic complexity (max, p95) | ESLint `complexity` [^41^] | radon [^37^] | ≤ 10/function (NIST); warn 15, gate 25 [^41^] | path count = test burden |
| Maintainability index | SonarQube | radon MI | ≥ 20 green; < 10 red [^37^] | find red-zone outliers |
| Cognitive complexity | SonarQube/SonarLint [^41^] | — | trending down | human load better than CC [^47^] |
| Coverage (line/branch) | Vitest/Istanbul | coverage.py [^37^] | context floor | necessary, not sufficient [^48^] |
| Mutation score (critical) | Stryker | mutmut [^51^] | 75–85% solid, 90%+ excellent [^48^] | proof the net bites |
| Dependency health | npm outdated, Knip [^20^] | pip-audit, pipdeptree | none unused/unlisted | phantom/missing deps [^20^] |
| Churn (90 days) | git log | git log | watch top 10% | top-decile churn ≈ 5× defects [^37^] |

**Exit criteria (Phase 0):** clean tagged commit; build green; tests green or user-waived; net in place for in-scope modules **and at least one net element per module mutation-proven**; `BASELINE.md` committed with commands, metric values, and the net-proof records.

---

## 6. Phase 1 — Deep Scan (Uncover)

### 6.1 Three lenses, two tracks

The scan examines the repo through three lenses — **cleanliness** (structure, naming, complexity, consistency), **redundancy** (duplicates, dead code, overlapping abstractions), **optimization** (inefficient patterns, bundle/runtime waste, dependency bloat) — each executed as two independent tracks. **Track 1** is deterministic tooling. **Track 2** is the LLM's semantic review for smells tools cannot express. Track separation is what makes triage possible: agreement is the strongest confidence signal, disagreement routes to verification, not the delete key [^27^][^31^].

The smell vocabulary for Track 2 is Fowler's catalog — **Bloaters**, **Change Preventers**, **Dispensables**, **Couplers**, **Obfuscators** [^5^][^7^] — plus the **AI-specific failure modes** that generated code repeats systematically: swallowed-failure catch-alls, defensive guards for impossible cases, premature abstraction, comment pollution, duplication over reuse, hallucinated APIs, intent-less naming, and hardcoded "declares success" returns [^27^]. For AI-built repos add five targeted probes: near-duplicate utilities with subtly different signatures (the GitClear signature [^54^][^60^]); unused speculative abstractions; inconsistent error-handling idioms across modules written in different sessions; phantom dependencies from abandoned spikes [^12^]; and comment/code drift where docstrings describe an older implementation.

### 6.2 Tooling matrix

| Lens | JS/TS | Python | JVM | Go | Cross-language |
|---|---|---|---|---|---|
| Dead code | **Knip** [^16^][^20^] | vulture, pylint, autoflake [^37^] | PMD, ProGuard | `deadcode`, staticcheck | SonarQube [^15^] |
| Duplication | **jscpd** v5 [^21^][^22^] | jscpd, pylint | PMD CPD [^15^] | jscpd, dupl | SonarQube CPD [^17^] |
| Complexity | ESLint, SonarJS | radon, xenon [^37^] | MetricsReloaded | gocyclo | SonarQube [^41^] |
| Dependency health | Knip [^20^], npm-check | pipdeptree, pip-audit [^37^] | versions plugin | `go mod tidy -diff` | OWASP dep-check |
| Type/lint | `tsc --noEmit`, eslint | mypy/pyright, ruff [^37^] | ErrorProne | `go vet` | MegaLinter [^21^] |
| Security smoke | npm audit, eslint-security | bandit [^37^] | SpotBugs | gosec | Semgrep |

Two known false-positive modes must be handled in triage, because they are the classic ways dead-code removal breaks apps. Static detectors miss **dynamic usage** — dynamic imports, string-based DI, framework magic exports, plugin registries [^13^][^19^]. Token-based duplication detectors normalize literals and identifiers, so they report *similar* code as identical — two blocks calling the same helper with different constants may be flagged as duplicates even when merging them is wrong [^23^]. Both are why GUARD never lets a raw tool report flow into a plan, and both get a dedicated falsification move in Phase 2.

### 6.3 Anti-hallucination protocol for the LLM track

The LLM track follows the layered defense that reduces hallucination impact: deterministic analysis grounds the review, the LLM generates hypotheses with structured output, every hypothesis queues for verification [^27^]. The agent must: (a) cite file, line range, and quoted code for every finding — no citation, no finding; (b) label each with the smell name so triage can check consistency; (c) propose the *minimal* catalog refactoring, never an open-ended rewrite; (d) state what could break if its reading is wrong. v2.0 adds: (e) **every claim is labeled VERIFIED, STATED, or UNKNOWN at birth**, and a STATED claim about the code is a hypothesis queued for a probe, never a conclusion. Findings failing these requirements are discarded at scan time.

**Exit criteria (Phase 1):** `FINDINGS.raw.json` holds the union of tool reports (tool, rule, location, severity) and LLM findings (smell, quote, minimal fix, self-risk, claim-label); counts per lens per module summarized; no code modified.

---

## 7. Phase 2 — Evidence Triage (Arbitrate, upgraded)

### 7.1 Confidence classification

Raw findings are worthless until triaged — dumping 400 lint warnings and 60 LLM observations on a user is how alert fatigue starts, and false positives are why developers abandon AI tools [^27^][^31^]. Triage assigns every finding a **confidence class** and a **risk tier**, and it is where most false positives die.

| Confidence | Definition | Examples | Disposition |
|---|---|---|---|
| **C3 tool-verified, behavior-safe** | Deterministic finding whose fix is provably non-behavioral | unused private variable; unreferenced file with zero import-graph edges and no dynamic-load pattern [^12^][^16^] | T0-eligible |
| **C2 multi-signal corroborated** | two independent signals agree | jscpd duplicate **and** LLM independently proposes same consolidation; Knip dead export **and** typecheck proves no dynamic ref [^20^][^22^] | standard path |
| **C1 single-signal, probe-verified** | one signal, then confirmed by a cheap deterministic probe | LLM claims unreachable → grep confirms zero call sites and zero string refs | standard path |
| **C0 hypothesis, unverified** | semantic judgment no cheap probe confirms | "these abstractions could unify"; "this class does too much" | **report only, never code** [^27^] |

Promotion is strict: a finding rises only by acquiring new deterministic evidence, never by the LLM re-asserting it more confidently. Rejected findings are logged under "Rejected / Not actionable" with the reason, so the user can see what was considered and vetoed.

### 7.2 The falsification pass (new in v2.0)

This is the single highest-value addition in v2.0, absorbed from the spec-auditor's discipline of cross-verifying every negative finding before publishing it. **Before any finding that asserts a negative is allowed to drive a change, the agent must actively try to falsify it** — and record the attempt.

The negative claims that destroy repos when wrong are exactly the ones a cleanup produces: "this code is dead," "this export has no callers," "these two blocks are identical," "this validation is missing." For each, the falsification move is specific:

| Negative claim | The falsification move (must be run and recorded) |
|---|---|
| "This function is dead" | grep the symbol **and** its string name; check dynamic imports, DI registries, framework magic exports, plugin discovery, reflection, config-driven wiring, template references. Look for it being *constructed* (factory strings) not just called. |
| "These blocks are duplicates" | read both in full; diff the **constants, rounding, error handling, null semantics**. Token-detectors normalize literals — "identical" may differ in one constant that matters [^23^]. If they differ, the fix is *parameterize*, never *delete one copy*. |
| "This dependency is unused" | check `package.json` scripts, build plugins, config-file references, CLI invocations, peer/optional roles — not just `import` statements. Confirm with a clean install + production build, not only a test run. |
| "This validation/check is missing" | search alternate layers: DB schema constraints, API gateway, middleware, generated code, a different naming convention. A "missing" check may live where you didn't look. |
| "This branch is unreachable" | enumerate the state space; prove no input reaches it — including failure, cancel, empty, and reload paths, which are exactly where unreachable-looking code turns out to be load-bearing. |

A claim that survives falsification earns the right to be planned. A claim that is weakened is downgraded or annotated, and the report says so. **A false CLEAN verdict is more dangerous than a false finding** — a false finding self-corrects when someone tries the fix and finds nothing; a false "this is safe" is permanent because nobody revisits it. So the falsification pass is also applied, selectively, to findings that declare something *safe*.

### 7.3 The lifecycle lens (new in v2.0)

When a finding touches a **data lifecycle** — records created, transformed, deleted, reloaded — a diff-shaped review structurally cannot find the worst defects, because they live in branches the diff does not contain. Four distinct data-loss defects were once found on a single batch across three review rounds, all past green CI, and they were one shape: **a state transition whose losing branch was never walked** — regeneration destroying records on success, the *fix* destroying records on failure/cancel, two records sharing an id after normalization, and deleting the last row resurrecting deleted rows because `length > 0 ? canonical : legacy` gave "explicitly emptied" and "never populated" the same representation.

The rule: for any lifecycle-touching change, **enumerate the states, enumerate the transitions — including failure, cancellation, empty, and reload — and require a written answer for each.** When a representation cannot distinguish two outcomes the user can produce, no call-site care fixes it; the illegal state must be made unrepresentable. Lifecycle findings route to the critical lane (T3) regardless of how small the diff looks.

### 7.4 Risk tiering: the protocol router

Every surviving finding is routed to a **change protocol** by two axes — blast radius and verification strength at the touch point — now expressed as the minimum proof-rung from §4.4.

![Protocol Tier Matrix: blast radius × verification strength → change protocol](figures/fig3-risk-tier-matrix.png)

| Tier | Name | Change examples | Mandatory protocol |
|---|---|---|---|
| **T0** | mechanical-safe | delete verified-dead file/export; remove unused dep; rename private symbol | build+typecheck+suite green → atomic commit; deletion target proven present-and-nonempty (V2); batch-approvable |
| **T1** | standard | consolidate in-module duplicates; simplify conditionals; split long function | T0 **plus** falsification pass on any duplicate/dead claim (V3) and characterization tests at the touch point |
| **T2** | elevated | cross-module consolidation; shared-util changes; component restructure | T1 **plus** revert-mutation proof on the named boundary test (V4), golden-master diff review, scoped mutation spot-check, per-change user approval [^48^] |
| **T3** | critical | data schemas, API payloads, auth, payments, persistence, external contracts | coexistence (strangler/branch-by-abstraction), flag **Off=old**, staged rollout 1→5→25→100%, closed only by an **anchor** (V5) + user sign-off per stage [^2^][^3^][^38^][^40^] |

Two unconditional overrides. Any finding touching data shape, external contracts, auth, or money is **always T3**. Any finding in a module with **no verification net** escalates one tier, because Phase 0's net is the only thing between "refactor" and "uncontrolled behavior change" [^6^][^9^].

### 7.5 Gate A — findings review

Triage closes with **Gate A**: the user reviews `FINDINGS.triaged.md` — findings with confidence, tier, falsification result, effort, expected benefit. The user marks each *accept*, *defer*, or *reject*, or adjusts tiers. Nothing rejected re-enters; deferred items park with their evidence. v2.0 adds one column the user will learn to love: **the falsification record**, so "this is dead" arrives with the proof that someone tried hard to kill that claim and couldn't.

**Exit criteria (Phase 2):** every raw finding classified (C0–C3), tiered (T0–T3) with a minimum proof-rung, falsified where negative, rejected-with-reason, or deferred; lifecycle findings routed to T3; Gate A approval recorded.

---

## 8. Phase 3 — The User Wizard

### 8.1 Design intent

The wizard is where "user control" becomes configuration. Six questions, asked once per run, compile into `guard.config.json` — the machine-readable contract the agent obeys for the rest of the run. The questions are about *intent and tolerance*, not technique [^21^].

![The six-question wizard and how answers compile into the execution contract](figures/fig4-wizard-flow.png)

| # | Question | Options | What it controls |
|---|---|---|---|
| **W1** | Why this run, why now? | routine hygiene · pre-release hardening · performance pain · post-incident | finding prioritization weights |
| **W2** | What may be touched? | whole repo · named modules · hotspot list only (churn × complexity [^37^]) | hard path allow-list |
| **W3** | Change appetite? | Conservative (T0–T1) · Balanced (+T2) · Accelerated (+T3) | highest tier the plan may contain |
| **W4** | What proves behavior today? | tests+GM · tests only · typecheck only · nothing | whether Phase 0 extends first; per-module tier escalation |
| **W5** | Where are the brakes? | approve every task · every batch · plan-only + final report | autonomy level / pause cadence |
| **W6** | How should changes land? | PR per task · per phase · single integration branch · direct to main | git topology, commit granularity [^66^][^72^] |

### 8.2 Profiles as sensible defaults

| Setting | 🛡 Conservative | ⚖ Balanced (default) | 🚀 Accelerated |
|---|---|---|---|
| Allowed tiers | T0–T1 | T0–T2 | T0–T3 |
| Min proof-rung ceiling | V3 | V4 | V5 |
| Approval cadence | every batch | every T2 + batch summaries | plan + T3 stage sign-offs |
| Safety-net requirement | characterization for T1+ | same (non-negotiable) | same (non-negotiable) |
| Risky-change rollout | n/a (T3 excluded) | flags where feasible | flags + staged canary mandatory [^38^][^40^] |
| Best for | production apps, thin tests, first run | most teams/repos | well-tested repos, hardening sprint |

**Hard rule no profile overrides (Feathers):** if W4 reveals an in-scope module has *no* verification net, the only changes allowed there are Phase 0 net-building until the net exists — and the net must be mutation-proven (V4) before T2+ work [^6^][^9^]. A user chooses *where* the net gets built first, never *whether* it exists.

**Exit criteria (Phase 3):** `guard.config.json` committed (scope allow-list, max tier, proof-rung ceiling, approval cadence, delivery mode, frozen modules); user has seen a plain-language summary.

---
