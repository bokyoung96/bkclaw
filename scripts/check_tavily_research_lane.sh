#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=./lib/load_env.sh
. "$ROOT_DIR/scripts/lib/load_env.sh"
load_workspace_env

printf '[config]\n'
if [ -n "${TAVILY_API_KEY:-}" ]; then
  printf 'TAVILY_API_KEY=present\n'
else
  printf 'TAVILY_API_KEY=missing\n'
fi

printf '\n[runtime]\n'
if env | grep -q '^TAVILY_API_KEY='; then
  printf 'active_env=present\n'
else
  printf 'active_env=missing\n'
fi

printf '\n[smoke]\n'
if command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'python3=available'
else
  printf '%s\n' 'python3=missing'
fi

printf '\n[result]\n'
printf '%s\n' 'Treat Tavily as ready only after key/config, active runtime env, and a real search smoke test all pass.'
