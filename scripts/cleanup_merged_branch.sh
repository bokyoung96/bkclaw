#!/usr/bin/env bash
set -euo pipefail

export PATH="/home/node/.local/bin:${PATH}"
set -a
. /home/node/.openclaw/workspace/.env
set +a
export GH_TOKEN="${GITHUB_TOKEN:-}"

BRANCH="${1:-}"
REPO="bokyoung96/bkclaw"

if [ -z "$BRANCH" ]; then
  echo "usage: $0 <branch>" >&2
  exit 1
fi

MERGED_STATE="$(gh pr list --repo "$REPO" --state merged --head "$BRANCH" --json number --jq 'length')"
if [ "$MERGED_STATE" = "0" ]; then
  echo "[branch-cleanup] no merged PR found for branch=$BRANCH" >&2
  exit 1
fi

git fetch origin >/dev/null 2>&1 || true
git push origin --delete "$BRANCH"

echo "[branch-cleanup] remote branch deleted: $BRANCH"
