#!/usr/bin/env bash
set -euo pipefail

load_workspace_env() {
  local script_dir root_dir env_file
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  root_dir="$(cd "$script_dir/../.." && pwd)"
  env_file="${ENV_FILE:-$root_dir/.env}"

  if [ -f "$env_file" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$env_file"
    set +a
  fi
}
