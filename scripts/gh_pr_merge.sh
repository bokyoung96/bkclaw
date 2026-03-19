#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/github_env.sh
. "$SCRIPT_DIR/lib/github_env.sh"
require_github_auth

pr_ref="${1:-}"
merge_mode="${MERGE_MODE:-merge}"
repo="bokyoung96/bkclaw"

if [ -z "$pr_ref" ]; then
  pr_ref="$(gh pr view --repo "$repo" --json number --jq '.number')"
fi

case "$merge_mode" in
  merge) mode_flag="--merge" ;;
  squash) mode_flag="--squash" ;;
  rebase) mode_flag="--rebase" ;;
  *) echo "[gh-pr-merge] unsupported MERGE_MODE=$merge_mode" >&2; exit 1 ;;
esac

gh pr merge "$pr_ref" --repo "$repo" "$mode_flag" --delete-branch=false
