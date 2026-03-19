#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

STATUS_OUTPUT="$(git status --short)"

if echo "$STATUS_OUTPUT" | grep -Eq '(^\?\?|^ M|^M |^MM)'; then
  echo "[pre-push-refactor-check] working tree has pending changes or untracked files"
  echo "$STATUS_OUTPUT"
else
  echo "[pre-push-refactor-check] working tree clean"
fi

python3 scripts/check_workspace_layout.py

echo "[pre-push-refactor-check] ask before push:"
echo "- can any root-level clutter be moved into bin/scripts/src/docs?"
echo "- can repetitive logic be consolidated before shipping?"
echo "- are generated/unnecessary files excluded or cleaned up?"
