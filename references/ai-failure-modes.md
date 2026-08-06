# AI Failure Modes

Read at Phase 1 (the semantic track) and keep in mind at Phase 5. These are the
patterns LLM-generated code repeats systematically — the defects linters cannot
see, and the ones most likely to be present in an AI-built repo *and* most
likely to sneak into your own edits. Distilled from published research and an
operational field catalog of AI-authored defects.

For each: the pattern, why it happens, the rule. Nine of fifteen trace to one
root cause — **the model is biased toward emitting more code, more guards, more
abstraction than the spec requires.** The cure is restraint.

1. **Catch-all handlers that swallow failures.** `try/catch` returning
   null/empty success on any error — a DB outage becomes indistinguishable from
   "no data." *Catch only the specific error you can recover from; never return
   empty success unless the contract says so.*
2. **Defensive guards for impossible cases.** Null/type checks the type system
   or call graph already prevents. *Trust the contract inside a trust boundary;
   validate only at the boundary.*
3. **Premature abstraction.** Factories, strategies, plugin hooks before a
   second concrete user exists. *One implementation = inline it.*
4. **Comment pollution.** Line-by-line comments restating the code; leftover
   "Step N" scaffolding. *Comments explain why, never what.*
5. **Duplication instead of reuse.** Inline copies of logic that already exists
   in a helper. The strongest quantitative result in the literature (GitClear:
   blocks of 5+ duplicated lines up ~8× during 2024; by H1 2026 copy/pasted
   lines reached 15.7% of all changes vs 9.4% in 2022, and refactored "moved"
   code fell to 3.8%). *Search for an existing function before writing one.*
6. **Hallucinated APIs and packages.** Imports/methods/signatures that don't
   exist in the installed version (~20% of LLM package references are
   fabricated across 16 models). *Verify every external call against the
   installed version — read the package or lockfile.*
7. **Generic, intent-less naming.** `data`, `result`, `item`, `temp`, `helper`,
   `handle_*`, `process_*`. *Identifiers must reveal intent.*
8. **Long functions doing many things.** I/O + logic + formatting in one body.
   *One function does one thing; ~50-line ceiling, ≤4 params, CC ≤10.*
9. **Parameter explosion.** 6+ positional args that should be a typed config
   object. *At 5 params, introduce a request/config object.*
10. **Inconsistency with surrounding code.** snake_case in a camelCase file, a
    new HTTP client when the repo has one. *Read the file and a neighbor before
    writing; match conventions; reuse existing utilities.*
11. **Dead code, unused imports, half-implementations.** Never-referenced
    symbols, unreachable branches, "just in case" exports. *Run a static check
    before finalizing; don't leave a function nothing calls.*
12. **"Declares success" — mock/hardcoded fallbacks in production.** Returning
    fixture data or canned success instead of doing the work. *Never hardcode
    success; never disable a test to pass it; fail explicitly and say what's
    missing.*
13. **Plausible-but-wrong code.** Compiles and reads correctly but encodes a
    subtly wrong boundary/range/null semantic. *Write the case enumeration
    (empty/one/even/odd/null) first and verify each; never copy-adapt a similar
    function — re-derive.*
14. **YAGNI — speculative configurability.** Config flags, env vars, toggles
    for use cases that don't exist. *No optional parameter without a present-day
    caller.*
15. **New dependency for trivial work.** A package for what the stdlib or a few
    lines already cover. *Check stdlib and installed deps first; add a
    dependency only for real complexity (crypto, parsing, time zones).*

**Cross-cutting:** an LLM that "knows" SOLID still produces these. They are the
high-leverage check — walk them before delivery, and hunt them during the scan.
