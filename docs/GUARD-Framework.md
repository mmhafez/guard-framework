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

## 9. Phase 4 — Plan Synthesis (Roadmap, upgraded)

### 9.1 From findings to an executable plan

The plan is synthesized from Gate-A-approved findings, the wizard config, and a **dependency analysis** that orders work so the codebase stays green after every task. Ordering follows Mikado logic: prerequisites first, leaf tasks first, and low-tier high-value work front-loaded — dead-code removal and duplication consolidation typically clear 20–40% of findings in the safest way and shrink the surface riskier tasks must consider [^64^][^65^].

v2.0 adds two fields to every task card that v1 lacked: the **proof-rung** the task must reach before it counts as done, and the **falsification record** for any negative claim it acts on. A task card is no longer complete with "verify: npm test" — it must name the rung (V2/V3/V4/V5) and, for V4/V5, the exact revert-mutation or anchor that closes it.

`PLAN.md` is structured for dual consumption — humans read the summary and risk brief; the executing agent parses task cards [^25^][^28^]:

```markdown
# PLAN.md — GUARD execution plan (v2)
## 0. Run summary
- Trigger (W1): …  Scope (W2): …  Profile (W3): …  Autonomy (W5): …
- Baseline: tag guard-baseline-2026-08-06, build ✅, tests 312 ✅, duplication 7.3%
- Net proof: money.ts characterization net mutation-proven (V4) 2026-08-06
- Approved findings: 41 (T0:22 · T1:13 · T2:5 · T3:1-deferred)
- Expected end state: duplication ≤ 3%, −1,900 LOC, zero behavior change

## 1. Global invariants
- After EVERY task: build green, suite green, golden masters unchanged
- One concern per commit; structure and behavior changes never mix
- Any verification failure → revert to last green, log, STOP and report
- Every claim labeled VERIFIED / STATED / UNKNOWN; UNKNOWN blocks
- No negative claim (dead / no-callers / missing) acted on without a falsification record

## 2. Task cards (execute in order)
### TASK-007 [T1] Consolidate duplicate currency formatters
- Finding: F-012 (C2: jscpd + LLM agree) — src/utils/money.ts vs src/billing/format.ts
- Falsification: read both; they differ in ROUNDING (half-up vs half-even) → NOT clean duplicates
- Change: extract one parameterized formatCurrency(amount, {rounding}) ; re-export from billing
- Touches: 4 files (listed)   Blast radius: module-internal
- Proof-rung: V3 (falsification done) + V4 on the money boundary test
- Verify: npm run build && npm test -- --grep "money|billing" && npm run gm:check
- Mutation-proof: revert rounding param → expect test_money_rounds_half_up to go RED → restore
- Rollback: git revert HEAD (single atomic commit)
- Acceptance: jscpd block F-012 gone; suite 312/312 green; GM diff reviewed & clean
```

### 9.2 Task card schema — every field mandatory

| Field | Purpose if omitted |
|---|---|
| Task ID + tier | protocol routing and approval cadence break |
| Finding reference + confidence | the change is untraceable to evidence — an orphan edit |
| **Falsification record** (for negative claims) | a wrong "dead/duplicate" claim deletes live code |
| Exact change description | vague instructions drift into scope leaks [^64^] |
| File allow-list | agent "helpfully" fixes adjacent code [^64^] |
| **Proof-rung (V2–V5)** | "works" becomes unfalsifiable; rung names the exact proof owed |
| Verify commands | copied verbatim from `BASELINE.md`; without them "done" is an opinion |
| **Mutation-proof / anchor** (V4/V5) | the net is assumed, never proven |
| Rollback path | a failed task becomes debugging on a broken tree — forbidden [^64^] |
| Acceptance criteria | "done" is the agent's opinion instead of a checkable state |

### 9.3 Gate B — plan approval

The plan is presented with a one-page plain-language brief: what changes, in what order, what could go wrong at each tier, the expected measurable end state, and what the agent does autonomously versus ask about. The user approves, edits, or sends back. **Only after Gate B may any application line be modified** [^25^][^29^]. For subtractive work the plan's burden of proof is higher than for feature work, because the goal is to change *nothing observable* — and v2.0 makes that burden explicit per task through the proof-rung.

**Exit criteria (Phase 4):** `PLAN.md` committed; every card complete per schema including proof-rung and falsification record; dependency order validated; Gate B approval recorded.

---

## 10. Phase 5 — Guarded Execution (Deliver, upgraded)

### 10.1 The per-task protocol

Execution is a loop, not an event. For each task card the agent executes this protocol in order, logging each step to `EXECUTION.log`:

| Step | Action | Hard rule |
|---|---|---|
| 1. Branch | task branch/worktree from latest green main | never stack unverified changes |
| 2. Pre-flight | run the card's verify commands **before** editing; confirm they act on a non-empty subject | a red or **vacuously-green** pre-flight means stop — check the check first (V2) |
| 3. Minimal change | implement exactly the card; nothing adjacent | no drive-by edits [^64^] |
| 4. Verify | run verify commands verbatim; diff golden masters; run characterization tests | 100% green; no "mostly passed" |
| 5. **Proof-rung** | reach the card's rung: falsification record (V3), revert-mutation (V4), or anchor (V5) | a task is not done at "green"; it is done at its rung |
| 6. Commit | one atomic commit referencing task + finding IDs | one concern per commit [^72^] |
| 7. Report | result (green/reverted), metrics touched, surprises, **claim labels** | per W5 cadence |

The failure path is as specified as the success path: on any verification failure the agent **reverts immediately**, records the failure and hypothesis, marks the task *blocked*, and either continues to the next independent task or stops per W5. Debugging forward on a broken tree is prohibited [^64^][^65^]. Clustered failures in one area mean the plan's model of that area is wrong — return to re-triage, don't push harder.

### 10.2 Execution hardening rules (new in v2.0)

These are the field lessons that cost the most, encoded as standing execution rules. Each is a trap that produces a confident wrong answer.

- **Never run a suite while another job runs one.** Concurrency has produced dozens of phantom failures against a true value of zero. A quiet gate (no other test/engine process alive) precedes any measurement, and excludes its own shell so it cannot false-positive on itself.
- **A failed command must never read as a benign value.** `git status | wc -l` → `0` on failure reads as "clean"; `|| echo 0` turns a failed count into "nothing to do." Judge checks by **exit code**, and sweep the *semantic class* — any command whose failure and whose negative answer are the same value.
- **A verdict printed beside a number it cannot contradict is decoration.** Never write a fixed string narrating what a number "should" be; interpolate the value and assert on it, letting a non-zero exit speak.
- **Probe the exact invocation before relying on it.** A dispatch or command that returns in seconds *failed*; a working long operation does not return instantly. The first real run of any command is its functional probe.
- **Never `pkill -f` / `pgrep` a name that appears in your own command line.** It matches the caller and either kills the orchestrator or waits on itself forever. Track pids explicitly.
- **Don't weaken a gate to close a hole.** When a check blocks, the fix is to satisfy it or narrow its *scope* — never to remove the assertion, add a skip, or loosen the anchor. Anti-weakening is checked at merge: no vanished test names, no new skip/xfail/only, no dropped assertion count without a numbered justification.
- **Verify by content, not ancestry, across merges.** In a squash-merge repo a merged branch is never an ancestor of main, and "behind main" is true of every live branch minutes after any merge — `git diff` the content, don't trust the graph.

### 10.3 Protocol details by tier

**T0 batches** run semi-automatically with build+typecheck+suite per change. Guards: before deleting an "unused" export, the falsification pass greps dynamic references [^13^][^19^]; dependency removal is verified with a clean install and production build, not just a test run; every deletion target is proven present-and-non-empty first (V2).

**T1 changes** add the falsification gate (V3) plus characterization tests that must pass unchanged. Duplicate consolidation requires a side-by-side behavioral read of both copies before merging — token detectors normalize literals, so "identical" blocks may differ in a constant that matters [^23^]; genuine differences mean *parameterize*, and the card must say so.

**T2 changes** add boundary golden masters reviewed as a first-class artifact [^53^][^56^], and the **revert-mutation proof** (V4): revert the change, watch the named boundary test go red, restore — proving the net catches this specific change. A scoped mutation run on the affected area confirms the net's strength [^48^]. The user approves each T2 change individually with the risk brief (§13).

**T3 changes** never execute as direct edits. They execute as **coexistence** — branch-by-abstraction or a strangler façade, a flag with polarity **Off = old behavior**, staged rollout (1→5→25→100% or internal→beta→all) with metric watches, and a kill switch armed through a ~30-day stabilization window with explicit exit criteria [^38^][^40^]. For high-stakes logic a **parallel run** can precede exposure: the new path executes in shadow, outputs compared to the old, users only ever seeing the old result until equivalence is convincing [^2^][^3^]. Crucially, a T3 change is closed only by an **anchor** (V5) — the deployed alias serving the new SHA, the endpoint answering a real request — never by a status report. Only after full rollout and stabilization does a by-now-trivial T0 task delete the old path.

### 10.4 Worked micro-example

A realistic trace, end to end. **Scan:** jscpd flags two 14-line blocks in `money.ts` and `billing/format.ts`; the LLM independently notes "two currency formatters, one rounds half-up, one half-even." **Triage:** the rounding observation triggers the duplicate falsification move; reading both confirms a **semantic difference** — not clean duplicates. Confidence C2, fix changed from "delete one" to "parameterize with explicit rounding." Tier T2 (cross-module, net present). **Wizard** (Balanced) admits it. **Plan:** TASK-014 with proof-rung V4, golden-master check on billing output, per-change approval. **Execution:** pre-flight green → parameterize → suite green → revert-mutation: removing the rounding param sends `test_money_rounds_half_up` red (net proven, V4) → restore → golden master reveals **one invoice total changed by $0.01** → that diff is the behavior change, caught before commit. The agent stops, reports, and the user decides: preserve legacy rounding (the usual choice — behavior is the asset [^6^]) or accept the delta consciously. That $0.01 is the whole framework in miniature: the net caught what confident reading missed, and the proof-rung is what made the net real.

---

## 11. Phase 6 — Verify & Close-out (upgraded)

### 11.1 The anchored equivalence proof

Close-out answers "perform the same exact function or better" with evidence in `DELTA.md`. v1 assembled this bottom-up from task logs and a final full-suite run. v2.0 insists the equivalence argument be **anchored**, because a close-out that only reads its own green reports is a circular graph. The proof is assembled as: every executed task's verification log (green builds, unchanged golden masters, passing characterization tests, and the proof-rung each reached), **plus** a final full-battery run on the integration result, **plus** — where the app deploys — a direct anchor: the deployed service serving the new SHA, a real request returning the expected shape, primary user flows exercised against the running system.

The report states plainly what was proven and **at what rung** (suite-level, golden-master, mutation-proven, anchored), and — just as important — **what was not proven**: paths with no net, deferred findings, claims still at STATED, and residual risks. A cleanup that ends with an honest list of what it did not prove is complete; one that ends in unanchored green is not.

### 11.2 The metrics delta

Improvement is reported as before/after against the Phase 0 baseline with the same tools and commands [^37^]:

| Metric | Baseline | Final | Δ | Assessment |
|---|---|---|---|---|
| Duplicated blocks / lines % | 7.3% | 2.1% | **−5.2 pts** | target met |
| Dead files / exports / deps | 18 / 64 / 5 | 0 / 2* / 0 | −93% | *2 dynamic-load, kept w/ note |
| Cyclomatic p95 / max | 14 / 31 | 10 / 18 | within NIST ≤10 [^41^] | improved |
| MI red files (<10) | 6 | 1 | −5 | one T3-deferred remains [^37^] |
| Suite / mutation (critical) | 312 ✅ / 58% | 341 ✅ / 74% | net strengthened | 75–85% = solid [^48^] |
| Bundle / build time | 412 kB / 38 s | 351 kB / 31 s | −15% / −18% | dead-code + dep removal |

Every number in the delta carries a claim label. A re-measured metric is VERIFIED. A target met is VERIFIED. Anything the environment could not re-measure is STATED or UNKNOWN and says so — an invented improvement number is the one thing in the report the reader cannot trust.

### 11.3 The residual register

The final required element is the **residual register**: deferred findings (evidence intact for the next run), T3 items still behind flags with stabilization windows and exit dates [^38^], golden masters marked as temporary scaffolding to be replaced by intention-revealing assertions [^56^], any scope boundary leaving known issues untouched, and **the lessons ledger delta** — any new failure the framework caused, minted as a numbered lesson (§15).

**Exit criteria (Phase 6):** equivalence evidence green **and anchored where it matters**; `DELTA.md` committed with claim labels; residual register reviewed and accepted; flags and temporary scaffolding carry explicit retirement dates; new lessons minted.

---

## 12. The Master Prompt Suite (v2.0)

These modules operationalize the framework for any capable coding agent. Paste the **Constitution** into standing instructions (AGENTS.md / rules), then invoke phase prompts P0–P6 in order. Bracketed `{slots}` are filled per repo. The prompts encode the planning-first, file-checkpoint discipline of spec-driven workflows [^25^][^28^][^29^], now with the v2.0 verification ladder built in.

### 12.0 The GUARD Constitution (standing rules)

```text
GUARD CONSTITUTION v2 — non-negotiable operating rules for this repository
1. BEHAVIOR IS THE PRODUCT. Never change observable behavior unless the user
   explicitly approves it. When docs and code disagree, actual behavior wins.
2. NO NET, NO CHANGE. Never modify code whose behavior is not captured by
   tests, golden masters, or type contracts — and a net that has never been
   watched FAIL is an assumption. Prove the net catches before relying on it.
3. LABEL EVERY CLAIM. Tag each statement VERIFIED (you ran something),
   STATED (you read it), or UNKNOWN (you could not tell). UNKNOWN blocks —
   never collapse it into a confident answer.
4. FALSIFY THE NEGATIVE. Before deleting anything as dead, duplicated, or
   missing, actively try to disprove the claim (dynamic refs, alternate
   layers, string construction, constants/rounding diffs) and record it.
5. GREEN IS RUNG ONE. A passing check is V1, not proof. Match the proof-rung
   to the tier: presence (V2), falsification (V3), revert-mutation (V4),
   anchor (V5). "The suite passed" never closes anything above T0.
6. ONE CONCERN PER COMMIT. No drive-by edits outside the task's allow-list.
   Structure and behavior changes never mix in one commit.
7. GREEN OR REVERT. Run verify commands before and after. Any failure:
   revert to last green, log, mark blocked. Never debug forward on red.
8. CHECK THE CHECK. Assert a check's preconditions (non-empty, routed,
   present) before trusting its verdict. Judge by exit code, never by output
   text. A failed command must never read as a benign value.
9. THE USER DECIDES. Follow guard.config.json exactly: scope, max tier,
   proof-rung ceiling, approval cadence. When uncertain — stop and ask.
10. REPORT IN DELTAS. Improvement is numbers vs. BASELINE.md from the same
    tools and commands, each labeled. "Cleaner" is not a metric.
11. RECORD THE LESSON. When this framework itself causes a failure, mint a
    numbered lesson. A recurring class is a defect in the framework, not you.
```

### 12.1 Phase prompts

**P0 — Baseline Lock**

```text
GUARD PHASE 0 — BASELINE LOCK. Modify no application code.
1. Detect the stack; record exact install/build/test/lint/start commands with
   real outputs in BASELINE.md.
2. Run build and full suite. On any failure, STOP and report with options; do
   not fix silently. Label each result VERIFIED with its exit code.
3. For {SCOPE_DIRS}, add characterization tests capturing CURRENT behavior
   (edge cases inferred from code, not docs). For {OUTPUT_MODULES}, add golden
   masters. Scrub secrets/PII before committing.
4. PROVE THE NET: for each in-scope module, pick one characterization test,
   temporarily break the behavior, watch THAT named test go red, restore.
   Record each proof. A net never watched failing is not yet trusted.
5. Snapshot metrics (duplication, dead code, complexity, coverage, deps) with
   exact commands. Confirm each check acts on a non-empty subject.
Commit "chore(guard): baseline lock", tag guard-baseline-{DATE}.
Report per module: green/red, net coverage, net-proof status, escalation zones.
```

**P1 — Deep Scan**

```text
GUARD PHASE 1 — DEEP SCAN. Read-only.
Run BOTH tracks into FINDINGS.raw.json:
TRACK 1 (deterministic): dead-code (knip/equivalent), duplication (jscpd ≥50
tokens/5 lines), complexity, dependency health, linters/typecheckers.
TRACK 2 (semantic): Fowler's smells plus the AI failure modes — swallowed-
failure catch-alls, impossible-case guards, premature abstraction, comment
pollution, duplication over reuse, hallucinated APIs, intent-less naming,
hardcoded success. Plus: near-duplicate utilities with different signatures,
speculative abstractions, inconsistent error idioms, phantom deps, comment/code
drift.
For EVERY Track-2 finding: quote code, cite file:lines, name the smell, propose
the MINIMAL refactoring, state what breaks if your reading is wrong, label the
claim VERIFIED/STATED/UNKNOWN. Flag every dynamic-usage pattern DYNAMIC-ZONE.
Summarize counts per lens (cleanliness/redundancy/optimization) per module.
```

**P2 — Evidence Triage + Gate A**

```text
GUARD PHASE 2 — TRIAGE. Read-only.
For each finding in FINDINGS.raw.json:
1. Confidence: C3 (tool-verified, fix non-behavioral), C2 (two independent
   signals agree), C1 (single signal + you ran a confirming probe — show it),
   C0 (unverified hypothesis — report only, never plan code from it).
2. FALSIFY every negative claim before it can drive a change:
   - "dead/no callers": grep symbol AND string name; check dynamic imports, DI
     registries, framework magic, plugin discovery, config wiring, templates.
   - "duplicate": read both fully; diff constants, rounding, error handling,
     null semantics. If they differ, the fix is PARAMETERIZE, never delete.
   - "unused dep": check scripts, build plugins, config refs, CLI, peer/optional.
   - "missing check": search alternate layers (DB, gateway, middleware, codegen).
   Record each falsification attempt and its outcome.
3. LIFECYCLE LENS: if a finding touches a data lifecycle, enumerate states and
   transitions including failure/cancel/empty/reload; route it to T3.
4. Tier from the matrix: blast radius (leaf / module-internal / cross-module /
   data-or-contract) × verification strength at the touch point (strong /
   partial / none) → T0/T1/T2/T3. Data, external contracts, auth, and payments
   are ALWAYS T3. No-net modules escalate one tier.
5. Reject or defer with reasons anything that fails verification.
Write FINDINGS.triaged.md: a table with id, location, smell, confidence, tier,
expected benefit (LOC, duplication %, complexity), effort estimate, and the
evidence. Then STOP and ask me to approve / defer / reject each finding —
this is GATE A. Modify nothing until I approve.
```

**P3 — User Wizard**

```text
GUARD PHASE 3 — WIZARD. Ask me these six questions, in order, with the listed
options. Do not proceed until all six are answered.
W1 TRIGGER: routine hygiene / pre-release hardening / performance pain /
   post-incident cleanup?
W2 SCOPE: whole repo / specific modules (which?) / hotspot list only?
W3 APPETITE: Conservative (T0–T1) / Balanced (+T2, per-change approval) /
   Accelerated (+T3, staged sign-off)?  [recommend Balanced]
W4 SAFETY NET: per in-scope module — tests+golden masters / tests only /
   typecheck only / nothing? (Modules answering "nothing" get net-building
   tasks FIRST and are otherwise frozen.)
W5 AUTONOMY: approve every task / every batch / plan-only then run with
   final report?
W6 DELIVERY: PR per task / PR per phase / single integration branch /
   direct commits to main?
Then write guard.config.json capturing my answers as enforceable constraints
(path allow-list, max tier, approval cadence, delivery mode, frozen modules),
and show me a plain-language summary of what each choice will mean in practice.
```

**P4 — Plan Synthesis + Gate B**

```text
GUARD PHASE 4 — PLAN. Read-only.
Using the Gate-A-approved findings and guard.config.json, write PLAN.md:
1. RUN SUMMARY: baseline state, approved findings by tier, expected measurable
   end state (duplication %, LOC, complexity), explicit non-goals.
2. GLOBAL INVARIANTS: after every task — build green, suite green, golden
   masters unchanged; one concern per commit; failure → revert + stop + report.
3. TASK CARDS in dependency order (prerequisites first; leaf tasks first;
   front-load T0/T1 quick wins). Each card MUST contain: task id, tier,
   finding reference + confidence, falsification record (if negative), exact
   change description, file allow-list, PROOF-RUNG with the specific revert-
   mutation or anchor, verbatim verify commands from BASELINE.md, rollback
   path, acceptance criteria, and for T2/T3 the extra protocol steps (golden-
   master diff review / flag + staged rollout with Off = old behavior).
4. RESPECT guard.config.json absolutely: nothing outside scope, nothing above
   max tier — overflow becomes a "deferred" section for a future run.
Then STOP and present the plan with a one-page plain-language risk brief.
This is GATE B. No application code changes until I approve.
```

**P5 — Guarded Execution**

```text
GUARD PHASE 5 — EXECUTE task {TASK_ID} from PLAN.md.
Protocol, in order, logging each step to EXECUTION.log:
1. Create branch {BRANCH_NAME} from latest green main.
2. PRE-FLIGHT: run this card's verify commands; confirm they act on a non-empty
   subject and exit by code, not output text. If red or vacuous, STOP — the
   baseline moved or the check is blind; report instead of proceeding.
3. Implement exactly the card's change. Touch only its file allow-list.
4. Run verify commands. Diff golden masters. Run the module's characterization
   tests. 100% green required — "mostly passing" is failure.
5. PROOF-RUNG: reach the card's rung — falsification record (V3), or revert the
   change and watch the NAMED test go red then restore (V4), or the anchor
   probe (V5). The task is done at its rung, not at "green".
6. Commit as ONE atomic commit: "refactor({scope}): {change} [GUARD {TASK_ID}]".
7. Report per my autonomy setting, with claim labels.
ON ANY FAILURE: revert immediately to last green (never debug forward), log
what failed and your hypothesis, mark the task blocked, and either continue
with the next independent task or stop, per my autonomy setting. Never weaken a
gate to pass it; never run a suite concurrently with another.
```

**P6 — Verify & Close-out**

```text
GUARD PHASE 6 — CLOSE-OUT.
1. Run the FULL verification battery on the integration result: build, entire
   test suite, all golden masters, typecheck, plus a smoke pass of primary
   user flows if the app runs.
2. ANCHOR the result where it matters: confirm the deployed service serves the
   new SHA, a real request returns the expected shape — a measurement, not a
   report about one. Record ANCHORED / UNANCHORED / UNKNOWN; UNKNOWN blocks.
3. Re-measure every BASELINE.md metric with the same tools and commands.
4. Write DELTA.md containing: (a) the equivalence evidence — what was proven
   and at what RUNG (suite / golden master / mutation / anchor); (b) the
   metrics table: baseline vs final vs target, each labeled VERIFIED/STATED;
   (c) the residual register — deferred findings with evidence, T3 items still
   behind flags with stabilization-window exit dates, temporary golden masters
   to retire, and anything intentionally left out of scope; (d) what was NOT
   proven and where residual risk lives.
5. Mint any new field lessons from failures this run caused.
Do not claim success in prose; show it in deltas. Label every claim.
```

---

## 13. Risk Communication Guide

The framework requires the agent to explain risk in a fixed format, because "it should be safe" is how regressions ship. Every T1+ task and every gate presentation uses this five-part brief — v2.0 adds the claim label and the proof-rung so the user can see *how* each safety statement is known.

| Element | Content | Example |
|---|---|---|
| **What could break** | concrete downstream consumers | "4 call sites pass pre-rounded values; consolidating changes their rounding path" |
| **What proves it didn't** | the specific net **and its rung** | "Golden master on invoice PDF (V5-anchored) + 14 characterization tests (V4 mutation-proven)" |
| **Residual uncertainty** | what the net cannot see, labeled | "STATED: no coverage of the PDF email path; visually spot-check after deploy" |
| **Rollback** | exact action and time-to-revert | "git revert of one commit, < 1 min" or "flag off, instant" [^38^] |
| **Decision needed** | what the user must choose, with a recommendation | "Approve / keep legacy rounding (recommended) / accept ±$0.01 delta" |

Tier-3 briefs add the rollout plan: flag name and polarity, stages with metric watch, the stabilization window (default 30 days with explicit exit criteria), the kill-switch owner, and the **anchor** that will close the change [^38^][^40^]. The pattern exists because the documented failure mode of AI-assisted development is not bad code but **unearned confidence** — fluent output that is "almost right" [^27^]. Forcing the agent to name what it cannot prove, and at what rung each proof sits, keeps confidence calibrated to evidence. The user's role is not to re-verify; it is to read the labels and decide.

---

## 14. Metrics, Acceptance Criteria, and Anti-Gaming

A GUARD run is accepted only if **all** equivalence criteria hold and the improvement metrics move correctly; partial movement with full equivalence is a valid, shippable outcome — "never broken" outranks "maximally clean."

| Criterion | Threshold | Rung | Notes |
|---|---|---|---|
| Build / typecheck | green at every commit | V2 | non-negotiable; checker proven to see the files |
| Test suite | 100% pre-existing + new pass | V1+ | no test deleted to pass (anti-weakening) |
| Golden masters | byte-identical or user-approved diffs | V5 | approval is a conscious act [^56^] |
| Net integrity | mutation spot-checks green | V4 | revert-mutation on changed critical paths |
| Duplication | monotone decrease | V3 | same jscpd config both sides [^22^] |
| Complexity (CC p95, MI red) | monotone decrease | V3 | NIST ≤10 per function [^41^] |
| Public API / schema surface | unchanged unless T3-approved | V5 | diff exported surface as a check |
| Equivalence (deployed) | anchor confirms | V5 | production serves new SHA |
| Reverts | logged, not hidden | — | high revert rate = plan-quality signal [^64^] |

Three anti-gaming rules guard the metrics, since every metric can be gamed [^48^]. **Coverage cannot be traded for deletion** — removing uncovered code raises coverage without making anything safer, so coverage deltas are reported alongside mutation scores, which cannot be gamed without assertions that genuinely constrain behavior [^48^]. **Complexity cannot be laundered through sprawl** — splitting one 40-line function into ten 4-line functions in a call chain lowers per-function CC while raising system complexity, so file- and module-level MI must also improve or stay flat. **Duplication removal must be semantic** — consolidating blocks token-detectors called identical but that differ in constants is a behavior change in a cleanup costume [^23^], and belongs at T2 with golden-master proof, not in a T0 batch.

---

## 15. The Field-Lessons Ledger

This is the mechanism that makes the framework self-improving, absorbed directly from the orchestration record's most durable idea. Every rule in GUARD that looks arbitrary should be traceable to what it cost. When the framework itself causes a failure — a false-positive deletion that slipped through, a gate that passed on nothing, a plan that broke the build — that failure is minted as a **numbered lesson**, recorded with three honest states:

- **MECHANISED** — a script or emitted contract enforces it; the mechanism is named.
- **DOCTRINE** — a standing rule with no cheap mechanism; said plainly as such.
- **OUTSTANDING** — a proposed mechanism not yet built, with its owner named.

The governing commitments: **a lesson appears once and is done** — if a class recurs after being absorbed, the recurrence is a failure of *the framework*, not of the operator. **A lesson can be wrong** — when one is refuted it is rewritten with the true cause rather than deleted, because the mistake's *shape* is the durable part. And **the ledger outlives the session** — it lives in the repo (`GUARD-LESSONS.md`), so a filling context window costs nothing and the next run starts wiser.

The seed lessons below are absorbed from the field record that motivated this upgrade, re-expressed for cleanup work:

| # | Lesson (cleanup framing) | State |
|---|---|---|
| GL-01 | A green gate is V1; it proves the check ran, not that the change is safe. Match the rung to the tier. | DOCTRINE |
| GL-02 | A check that cannot fail is worse than no check. Prove the net catches before relying on it (revert-mutation). | DOCTRINE |
| GL-03 | "Dead code" is a falsifiable claim. Grep the string name, not just the symbol, before deleting. | DOCTRINE |
| GL-04 | Token-identical blocks can differ in a constant that matters. Read both fully; parameterize, don't delete. | DOCTRINE |
| GL-05 | A failed command must never read as a benign value (`wc -l` → 0). Judge by exit code. | DOCTRINE |
| GL-06 | UNKNOWN is a verdict and it blocks. Never invent a confident answer to pass a gate. | DOCTRINE |
| GL-07 | A false CLEAN is permanent; a false finding self-corrects. Falsify the "safe" verdicts too. | DOCTRINE |
| GL-08 | Lifecycle defects live in failure/cancel/empty/reload branches a diff can't show. Enumerate transitions. | DOCTRINE |
| GL-09 | Don't weaken a gate to close a hole. Narrow scope, never assertion count. | DOCTRINE |
| GL-10 | Verify merges by content, not ancestry — squash merges break every graph check. | DOCTRINE |

---

## 16. Failure Modes and Limits

| Failure mode | Symptom | Framework defense | Residual risk |
|---|---|---|---|
| **Scope leak** | diffs grow beyond task cards [^64^] | file allow-lists; one-concern commits; diff review | subtle leaks in shared files need human review |
| **False-positive deletion** | dynamically-referenced code removed [^13^][^19^] | falsification pass; DYNAMIC-ZONE registry; full build + smoke | novel dynamic patterns a scan didn't anticipate |
| **Semantic "duplicates"** | merged blocks differing in constants [^23^] | parameterize-not-delete; golden masters at boundaries | differences invisible to output capture (timing) |
| **Vacuous green** | check passes on an absent/empty subject | presence assertions (V2); exit-code judging | a check blind in a new way |
| **Net that can't catch** | suite green but behavior changed | revert-mutation (V4); scoped mutation score [^48^] | mutation run scoped too narrowly |
| **Circular verification** | reports confirm reports, nothing touches ground | anchors (V5); UNKNOWN blocks | anchors skipped under schedule pressure |
| **Net fossilization** | golden masters kept forever [^56^] | residual register with retirement dates | a human must eventually decide intent |
| **Green-leaf illusion** | tasks green, integration broken [^64^] | full-battery + anchor in Phase 6 | rare interaction bugs; bisectable history mitigates |
| **Plan rot** | repo drifts between analysis and execution | per-task pre-flight; re-baseline on red | long runs need periodic re-baselining |
| **Metric theater** | numbers improve, code doesn't | anti-gaming rules (§14); mutation spot-checks | aesthetics still need judgment |

The framework has honest limits. It needs a runnable repo — a project that cannot build cannot be verified, so Phase 0 routes to "fix the build first." It needs reasonably fast feedback — Mikado revert discipline works because each experiment is cheap; a 20-minute suite raises the cost of every task and argues for investing in test speed early [^64^]. It cannot judge product intent — whether a "redundant" path is a deliberate fallback is a business question, which is why C0 findings and suspicious survivals route to the user. And it does not remove the human — it puts the human **at the head of the loop**, which is where the trust research says the human must be: layered defenses plus human oversight as final authority [^27^]. The most sophisticated version of this machinery is the one honest enough to mark where its own authority ends.

---

## 17. Optional Multi-Agent Execution Mode

For most repos a single disciplined agent running the pipeline is enough. But T2/T3 work — cross-module consolidation, shared-code changes, anything touching data or contracts — benefits from a property one agent cannot give itself: **an independent verifier that did not write the code.** This optional mode, adapted from the multi-engine orchestration record, adds it without the full roster machinery.

### 17.1 The principle: nobody grades their own homework

The single strongest structural rule in the absorbed record is that a reviewer must not share the author's reasoning lineage — a model reviewing its own output is "a model agreeing with its own reasoning," which passes silently because there is no disagreement to notice. In practice: the agent that *implements* a T2/T3 change should not be the agent that *reviews* it. A second model (different family) reviews the scoped diff, adversarially hunting for failure rather than confirming success.

### 17.2 The minimal graph

```
plan ──▶ implement ──▶ review ──pass──▶ verify(rung) ──pass──▶ commit
            ▲             │                 │
            └── fix ◀──fail──────────fail───┘
              (bounded rounds, then escalate to user)
```

Three rules make it safe. **The reviewer is read-only** — a reviewer that can fix stops judging. **Rounds are bounded** (default 3) with a declared exhaustion route (escalate to the user) — an unbounded fix loop is how budgets burn. **The verdict is anchored** — the reviewer's PASS is bound to the exact commit SHA it reviewed, so a later change invalidates it, and a review of an unmerged worktree is never presented as a merged PASS.

### 17.3 The adversarial review lenses

The reviewing agent does not skim for style; it hunts four specific defect classes that machine gates historically miss, and it must write a finding for each — **"none found" is a claim the reviewer owns**, not silence:

1. **Silent success** — a path that reports success while producing nothing (a swallowed exception, an export that builds nothing, a button that no-ops). The dominant defect class.
2. **Code-exists ≠ capability-ships** — for every capability the diff claims, name its caller; one grep discharges it, and the inverse (claiming no consumer when one exists) also fails.
3. **Mocking the layer whose configuration is wrong** — a mock can make a defect invisible; assert the real configuration, negatively (a positive assertion passes even when the wrong value is also sent).
4. **Satisfiable by absence** — for each check, what would it do if its subject were entirely absent?

Plus the **lifecycle lens** for data work (§7.3) and the **verification doctrine**: a negative test must go red when the fix is reverted; assert the discriminating detail, not the error class; check each mock's return shape against the real implementation's return statement.

### 17.4 When to use it

| Signal | Single agent is enough | Add a second reviewer |
|---|---|---|
| Tier | T0–T1 | T2–T3 |
| Blast radius | module-internal | cross-module / data / contract |
| Net strength | mutation-proven | thin or partial |
| Cost of a mistake | a revert | an outage, data loss, money |

The bar is real: a second engine costs tokens and coordination, and over-spawning reviewers for work that never needed them is its own failure. Reach for it when the cost of being wrong exceeds the cost of the review — which, for the changes GUARD reserves for T2/T3, is exactly the case.

---

## 18. Quick-Start Checklist

For a first run on a typical AI-built web app (React/Next.js + Node API):

1. **Paste the GUARD Constitution v2** (§12.0) into the agent's rules/AGENTS.md.
2. **Run P0** — expect 30–90 min of net-building on an untested repo, **including proving the net catches** (one revert-mutation per module). That time is the price of every safe change that follows [^53^].
3. **Run P1–P2** — review the triaged findings at **Gate A**; expect to reject 10–30% as false positives, and read the **falsification records** on anything marked "dead" or "duplicate." That rejection rate is the filter working [^27^].
4. **Run P3** — choose **Balanced** unless you have a reason otherwise.
5. **Run P4** — review `PLAN.md` at **Gate B**; confirm every T1+ card names a proof-rung and every negative claim has a falsification record. Strike anything you can't explain [^30^].
6. **Run P5** per task; enjoy the boring T0 batches, which typically clear a fifth to a third of findings at near-zero risk [^12^][^16^]. For T2/T3, optionally add an independent reviewer (§17).
7. **Run P6** — read `DELTA.md`, confirm the equivalence evidence is **anchored**, approve the residual register, schedule flag retirements [^38^].
8. **Record any lessons** the run surfaced into `GUARD-LESSONS.md`, and repeat quarterly or pre-release. Each run starts from a better baseline and a longer ledger.

The framework's success criterion is not a spotless repo. It is a repo that **does exactly what it did before — provably, to a named rung of proof — while being measurably cheaper to change tomorrow**, with every step owned by the user who drove it, and every claim labeled by how it is known.

---

*The GUARD Framework v2.0 — built from the refactoring literature (Feathers, Fowler, Ellnestam & Brolund), the safe-deployment canon (strangler fig, branch by abstraction, feature flags, canary rollout), the measurement tradition (complexity, maintainability, churn, mutation scoring), the 2024–2026 evidence base on AI-generated code quality and AI review reliability, and a field-hardened operational record of ~150 numbered lessons on making agent verification actually mean something.*
