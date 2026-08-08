#!/usr/bin/env python3
"""guard_lint.py — mechanised checks for GUARD run artifacts.

Subcommands:
  config    <guard.config.json>      validate against references/guard.config.schema.json rules
  plan      <PLAN.md>                every task card complete; zero cards = FAIL
  findings  <FINDINGS.triaged.md>    required columns + DYNAMIC-ZONE register; empty = FAIL
  run-state <GUARD-RUN.md>           phase valid; passed gates carry recorded decisions
  sync      [repo-root]              references/prompts.md + constitution.md match docs copy

Design rules (the framework's own):
  * Judge by exit code: 0 = pass, 1 = lint failures, 2 = usage/unreadable input.
  * Never satisfiable by absence: a missing or empty subject is a FAILURE, not a pass.
  * Stdout carries findings; stderr carries diagnostics.

No dependencies outside the Python 3.8+ standard library. Not interactive.
"""
import json
import re
import sys
from pathlib import Path

FAILS = []


def fail(msg):
    FAILS.append(msg)


def read_subject(path):
    """Read a file, enforcing the non-empty-subject precondition."""
    p = Path(path)
    if not p.is_file():
        print(f"guard_lint: subject does not exist: {path}", file=sys.stderr)
        sys.exit(2)
    text = p.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        print(f"guard_lint: subject is empty: {path} — a check with no subject is not a check",
              file=sys.stderr)
        sys.exit(2)
    return text


# ---------------------------------------------------------------- config ----

ENUMS = {
    "status": {"provisional", "final"},
    "trigger": {"routine-hygiene", "pre-release-hardening", "performance-pain", "post-incident"},
    "max_tier": {"T0", "T1", "T2", "T3"},
    "proof_rung_ceiling": {"V2", "V3", "V4", "V5"},
    "approval_cadence": {"per-task", "per-batch", "per-t2-change", "plan-only"},
    "delivery": {"pr-per-task", "pr-per-phase", "integration-branch", "direct"},
}
NET_VALUES = {"tests+gm", "tests", "typecheck", "none"}
KNOWN_KEYS = set(ENUMS) | {"scope", "delivery_base", "frozen_modules",
                           "net_status", "net_status_claimed", "run_id", "baseline_tag"}
REQUIRED_ALWAYS = ["status", "trigger", "scope", "delivery", "delivery_base"]
REQUIRED_FINAL = ["max_tier", "proof_rung_ceiling", "approval_cadence"]


def lint_config(path):
    try:
        cfg = json.loads(read_subject(path))
    except json.JSONDecodeError as e:
        fail(f"config: not valid JSON — {e}")
        return
    if not isinstance(cfg, dict):
        fail("config: top level must be an object")
        return
    for k in cfg:
        if k not in KNOWN_KEYS:
            fail(f"config: unknown key '{k}' (contract: references/guard.config.schema.json)")
    for k in REQUIRED_ALWAYS:
        if k not in cfg:
            fail(f"config: missing required key '{k}'")
    if cfg.get("status") == "final":
        for k in REQUIRED_FINAL:
            if k not in cfg:
                fail(f"config: status=final requires '{k}' (Wizard II not compiled)")
    for k, allowed in ENUMS.items():
        if k in cfg and cfg[k] not in allowed:
            fail(f"config: {k}={cfg[k]!r} not in {sorted(allowed)}")
    scope = cfg.get("scope")
    if scope is not None:
        if not isinstance(scope, dict):
            fail("config: scope must be an object with 'allow' (and optional 'deny')")
        else:
            allow = scope.get("allow")
            if not (isinstance(allow, list) and allow and all(isinstance(x, str) for x in allow)):
                fail("config: scope.allow must be a non-empty list of globs — "
                     "an empty allow-list authorizes nothing and masks a wizard skip")
            deny = scope.get("deny", [])
            if not (isinstance(deny, list) and all(isinstance(x, str) for x in deny)):
                fail("config: scope.deny must be a list of globs")
            for k in scope:
                if k not in ("allow", "deny"):
                    fail(f"config: unknown scope key '{k}'")
    if cfg.get("delivery") == "integration-branch" and cfg.get("delivery_base") in ("", "main", "master"):
        fail("config: delivery=integration-branch but delivery_base is the trunk — "
             "name the integration branch tasks are cut from")
    for field in ("net_status", "net_status_claimed"):
        ns = cfg.get(field)
        if ns is not None:
            if not isinstance(ns, dict):
                fail(f"config: {field} must map module path -> one of {sorted(NET_VALUES)}")
            else:
                for mod, v in ns.items():
                    if v not in NET_VALUES:
                        fail(f"config: {field}[{mod!r}]={v!r} not in {sorted(NET_VALUES)}")


# ------------------------------------------------------------------ plan ----

CARD_RE = re.compile(r"^###\s+(TASK-\S+)\s+\[(T[0-3])\]", re.M)
CARD_FIELDS = ["Finding", "Falsification", "Change", "Touches", "Proof-rung",
               "Verify", "Rollback", "Acceptance"]


def lint_plan(path):
    text = read_subject(path)
    if not re.search(r"(?im)^##.*global invariants", text):
        fail("plan: no 'Global invariants' section")
    if not re.search(r"(?im)^##.*run summary", text):
        fail("plan: no 'Run summary' section")
    matches = list(CARD_RE.finditer(text))
    if not matches:
        fail("plan: ZERO task cards found (headings must look like '### TASK-001 [T1] ...') — "
             "an empty plan is a lint failure, not a pass")
        return
    for i, m in enumerate(matches):
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        card, tier = m.group(1), m.group(2)
        for f in CARD_FIELDS:
            if not re.search(rf"(?im)^\s*[-*]\s*{re.escape(f)}\b", body):
                fail(f"plan: {card} [{tier}] missing mandatory field '{f}'")
        if tier in ("T2", "T3") and not re.search(r"(?im)^\s*[-*]\s*(Mutation-proof|Anchor)\b", body):
            fail(f"plan: {card} [{tier}] must name its Mutation-proof (V4) or Anchor (V5)")
    print(f"plan: {len(matches)} task card(s) checked", file=sys.stderr)


# -------------------------------------------------------------- findings ----

FINDING_COLS = ["id", "location", "smell", "confidence", "tier",
                "proof-rung", "falsification", "evidence"]


def lint_findings(path):
    text = read_subject(path)
    header = None
    for line in text.splitlines():
        if line.strip().startswith("|") and "id" in line.lower():
            header = line.lower()
            break
    if header is None:
        fail("findings: no markdown table with an 'id' column found")
    else:
        for col in FINDING_COLS:
            if col not in header:
                fail(f"findings: table header missing column '{col}'")
    data_rows = re.findall(r"(?im)^\|\s*F-\S+\s*\|", text)
    # The escape hatch must be a DECLARATION LINE, not the token appearing
    # anywhere in the document. A plain `"NO-FINDINGS:" in text` was satisfied
    # by the template's own instructions ("...write `NO-FINDINGS: <counts>`"),
    # so every report derived from the template passed with zero rows without
    # anyone ever declaring it — this check being satisfiable by absence is
    # exactly what this file's design rules forbid. Anchored at line start and
    # required to carry content, so prose and backticked examples do not count.
    declared = re.search(r"(?im)^\s*NO-FINDINGS:\s*\S+", text)
    if not data_rows and not declared:
        fail("findings: zero data rows and no explicit 'NO-FINDINGS: <per-lens zero counts>' line — "
             "an empty report must say so out loud, not pass by absence")
    if not re.search(r"(?im)^##.*dynamic-zone", text):
        fail("findings: no 'DYNAMIC-ZONE register' section "
             "(if truly none were flagged, the section says 'none flagged')")


# ------------------------------------------------------------- run-state ----

PHASES = ["P0-wizard-I", "P0", "P1", "P2", "gate-A", "P3", "P4", "gate-B", "P5", "P6", "closed"]


def lint_run_state(path):
    text = read_subject(path)
    m = re.search(r"(?im)^\s*[-*]?\s*Phase:\s*(\S+)", text)
    if not m:
        fail("run-state: no 'Phase: <value>' line")
        return
    phase = m.group(1)
    if phase not in PHASES:
        fail(f"run-state: phase {phase!r} not in {PHASES}")
        return
    idx = PHASES.index(phase)
    decisions = re.findall(r"(?im)^\|\s*F-\S+\s*\|\s*(accept|defer|reject)\b", text)
    if idx > PHASES.index("gate-A") and not decisions:
        fail("run-state: phase is past gate-A but no per-finding decisions "
             "(| F-xxx | accept/defer/reject |) are recorded — an unrecorded gate was not passed")
    if idx > PHASES.index("gate-B") and not re.search(r"(?im)^\s*[-*]?\s*Gate B:\s*approved", text):
        fail("run-state: phase is past gate-B but no 'Gate B: approved ...' line is recorded")


# ------------------------------------------------------------------ sync ----

BLOCK_RE = re.compile(r"```text\n(GUARD (?:PHASE \d|CONSTITUTION)[^\n]*\n.*?)```", re.S)


def _blocks(text):
    out = {}
    for m in BLOCK_RE.finditer(text):
        body = m.group(1).strip()
        out[body.splitlines()[0].strip()] = body
    return out


def lint_sync(root):
    root = Path(root)
    refs = _blocks(read_subject(root / "references" / "prompts.md"))
    refs.update(_blocks(read_subject(root / "references" / "constitution.md")))
    docs = _blocks(read_subject(root / "docs" / "GUARD-Framework.md"))
    if not refs:
        fail("sync: no fenced GUARD blocks found in references/ — subject vanished")
        return
    for key, body in sorted(refs.items()):
        if key not in docs:
            fail(f"sync: docs copy missing block: {key!r}")
        elif docs[key] != body:
            fail(f"sync: drift in block {key!r} — references/ is the source of truth; "
                 f"update docs/GUARD-Framework.md §12 to match")
    print(f"sync: {len(refs)} block(s) compared", file=sys.stderr)


# ------------------------------------------------------------------ main ----

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(argv) >= 2 else 2
    cmd, args = argv[1], argv[2:]
    if cmd == "config" and len(args) == 1:
        lint_config(args[0])
    elif cmd == "plan" and len(args) == 1:
        lint_plan(args[0])
    elif cmd == "findings" and len(args) == 1:
        lint_findings(args[0])
    elif cmd == "run-state" and len(args) == 1:
        lint_run_state(args[0])
    elif cmd == "sync" and len(args) <= 1:
        lint_sync(args[0] if args else Path(__file__).resolve().parent.parent)
    else:
        print(__doc__)
        return 2
    if FAILS:
        for f in FAILS:
            print(f"FAIL  {f}")
        print(f"guard_lint {cmd}: {len(FAILS)} failure(s)")
        return 1
    print(f"guard_lint {cmd}: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
