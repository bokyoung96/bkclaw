#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HELPER='!f() { REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; "$REPO_ROOT/scripts/git-credential-env.sh" "$@"; }; f'

git config credential.helper "$HELPER"
git config credential.useHttpPath true

echo "[git-auth] configured credential.helper for repo-root dynamic resolution"
echo "[git-auth] repo=$REPO_ROOT"
