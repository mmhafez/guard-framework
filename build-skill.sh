#!/usr/bin/env bash
# Build the installable guard-framework.skill from source.
# Usage: bash build-skill.sh
set -euo pipefail
cd "$(dirname "$0")"

STAGE=".skill-build"
rm -rf "$STAGE"
mkdir -p "$STAGE/guard-framework"

cp SKILL.md "$STAGE/guard-framework/"
cp -r references "$STAGE/guard-framework/"
cp -r agents "$STAGE/guard-framework/"

( cd "$STAGE" && zip -qr ../guard-framework.skill guard-framework )
rm -rf "$STAGE"

echo "Built guard-framework.skill ($(wc -c < guard-framework.skill) bytes)"
