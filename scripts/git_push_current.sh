#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/load_env.sh
. "$SCRIPT_DIR/lib/load_env.sh"
load_workspace_env

branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
remote="${2:-origin}"

echo "[git-push] remote=$remote branch=$branch"
git push -u "$remote" "$branch"
