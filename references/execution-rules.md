# Execution rules and hardening

Read at Phase 5. The per-task protocol, then the field lessons that cost the
most, encoded as standing rules.

## Per-task protocol (in order)

Log each step to `EXECUTION.log` as `timestamp | task | step | result`.

1. **Branch** from the latest green delivery base (per W6: main, or the
   integration branch). Never stack unverified changes.
2. **Pre-flight** — run the card's verify commands before editing; confirm they
   act on a non-empty subject (V2). A red or vacuously-green pre-flight means
   stop and report, not proceed.
3. **Minimal change** — implement exactly the card; nothing adjacent. No
   drive-by edits.
4. **Verify** — run the commands verbatim; diff golden masters; run
   characterization tests. 100% green; no "mostly passed."
5. **Proof-rung** — reach the card's rung: falsification record (V3),
   revert-mutation (V4), or anchor (V5). Done at the rung, not at "green."
   (Multi-agent mode: the independent review slots between steps 4 and 5, on
   the exact tree it approves — see multi-agent.md.)
6. **Commit** — one atomic commit referencing task + finding IDs.
7. **Report** — result, metrics touched, surprises, claim labels, per W5 cadence.

On any failure: **revert immediately** (never debug forward on a broken tree),
log the hypothesis, mark the task blocked, continue to the next independent task
or stop per autonomy. Clustered failures in one area mean the plan's model of
that area is wrong — return to re-triage, don't push harder.

## Hardening rules (each one bought by a real failure)

- **Never run a suite while another job runs one.** Concurrency produces phantom
  failures against a true value of zero. A quiet gate (no other test/engine
  process alive) precedes any measurement, excluding its own shell. A workable
  probe — judged by exit code, never by counting output lines:

  ```sh
  # exit 0 = quiet, exit 1 = another runner is alive
  ps -eo pid,command | awk -v self=$$ \
    '$1==self || /awk/ {next} /vitest|jest|pytest|go test/ {f=1} END {exit f}'
  ```
- **A failed command must never read as a benign value.** `git status | wc -l` →
  `0` on failure reads as "clean"; `|| echo 0` turns a failed count into
  "nothing to do." Judge by exit code; sweep the *semantic class* — any command
  whose failure and whose negative answer are the same value.
- **A verdict printed beside a number it cannot contradict is decoration.**
  Never write a fixed string narrating what a number "should" be; interpolate
  the value and assert on it, letting a non-zero exit speak.
- **Probe the exact invocation before relying on it.** A command that returns in
  seconds failed; a working long operation does not return instantly. The first
  real run of any command is its functional probe.
- **Never `pkill -f` / `pgrep` a name that appears in your own command line.**
  It matches the caller and either kills the orchestrator or waits on itself
  forever. Track pids explicitly.
- **Don't weaken a gate to close a hole.** When a check blocks, satisfy it or
  narrow its *scope* — never remove the assertion, add a skip, or loosen an
  anchor. At merge, check anti-weakening: no vanished test names, no new
  skip/xfail/only, no dropped assertion count without a numbered justification.
- **Verify merges by content, not ancestry.** In a squash-merge repo a merged
  branch is never an ancestor of main, and "behind main" is true of every live
  branch minutes after any merge — `git diff` the content, don't trust the graph.
- **A slow process and a dead process look identical from outside.** Budget
  patience proportional to the work; never read an empty log as death (it's
  consistent with buffering, slow start, a long think, AND death — it separates
  none of them).
