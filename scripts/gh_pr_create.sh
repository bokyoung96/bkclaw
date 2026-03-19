#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/github_env.sh
. "$SCRIPT_DIR/lib/github_env.sh"
require_github_auth

cd "$(git rev-parse --show-toplevel)"

branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
base="${2:-main}"
title="${3:-$(git log -1 --pretty=%s)}"
body_file="${4:-docs/refactor/pr-body-agent-runtime-5step.md}"

if [ ! -f "$body_file" ]; then
  echo "[gh-pr-create] body file not found: $body_file" >&2
  exit 1
fi

gh pr create \
  --repo bokyoung96/bkclaw \
  --head "$branch" \
  --base "$base" \
  --title "$title" \
  --body-file "$body_file"
