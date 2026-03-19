#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/load_env.sh
. "$SCRIPT_DIR/lib/load_env.sh"
load_workspace_env

case "${1:-}" in
  get)
    if [ -n "${GITHUB_TOKEN:-}" ]; then
      printf 'username=%s\n' "${GITHUB_USERNAME:-x-access-token}"
      printf 'password=%s\n' "$GITHUB_TOKEN"
    fi
    ;;
  store|erase)
    ;;
esac
