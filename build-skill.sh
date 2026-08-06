#!/usr/bin/env bash
# Build the installable guard-framework.skill from source.
# Usage: bash build-skill.sh
set -euo pipefail
cd "$(dirname "$0")"

# --- Gate: validate before packaging (a build that skips its checks ships blind)
python3 - <<'PY'
import re, sys
t = open('SKILL.md', encoding='utf-8').read()
fm = re.match(r"---\n(.*?)\n---\n", t, re.S)
assert fm, "SKILL.md: no frontmatter"
keys = set(re.findall(r"(?m)^([a-z-]+):", fm.group(1)))
allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
extra = keys - allowed
assert not extra, f"SKILL.md: non-spec frontmatter keys {extra} (upload would hard-fail)"
d = re.search(r'description: "(.*?)"\n[a-z-]+:', fm.group(1) + "\nend:", re.S).group(1)
assert 1 <= len(d) <= 1024, f"description is {len(d)} chars (spec limit 1024)"
c = re.search(r'compatibility: "(.*?)"\n', fm.group(1))
assert c is None or len(c.group(1)) <= 500, "compatibility over 500 chars"
name = re.search(r'(?m)^name: (\S+)$', fm.group(1)).group(1)
assert name == "guard-framework", "frontmatter name must match the directory name"
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name), "name violates spec charset"
print(f"validate: frontmatter OK (description {len(d)} chars)")
PY
python3 scripts/guard_lint.py sync .
python3 scripts/guard_lint.py config assets/templates/guard.config.example.json >/dev/null
python3 scripts/guard_lint.py plan assets/templates/PLAN.md >/dev/null
echo "validate: templates + prompt-suite sync OK"

# --- Package (fresh archive every time: zip -r UPDATES an existing archive and
# --- keeps entries whose sources were deleted — a stale, contaminated skill)
STAGE=".skill-build"
OUT="guard-framework.skill"
rm -rf "$STAGE"
rm -f "$OUT"
mkdir -p "$STAGE/guard-framework"

cp SKILL.md LICENSE "$STAGE/guard-framework/"
cp -r references scripts assets agents "$STAGE/guard-framework/"
find "$STAGE" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

( cd "$STAGE" && zip -qr "../$OUT" guard-framework )
rm -rf "$STAGE"

echo "Built $OUT ($(wc -c < "$OUT") bytes)"
unzip -l "$OUT" | tail -3
