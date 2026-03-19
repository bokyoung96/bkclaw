#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=./load_env.sh
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/load_env.sh"
load_workspace_env

export PATH="/home/node/.local/bin:${PATH}"

if [ -n "${GITHUB_TOKEN:-}" ]; then
  export GH_TOKEN="$GITHUB_TOKEN"
fi

require_gh() {
  if ! command -v gh >/dev/null 2>&1; then
    echo "[github-env] gh CLI not found on PATH" >&2
    return 1
  fi
}

require_github_auth() {
  require_gh
  gh auth status >/dev/null 2>&1
}
