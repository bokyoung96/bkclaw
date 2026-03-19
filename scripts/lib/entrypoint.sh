#!/usr/bin/env bash
set -euo pipefail

resolve_repo_root() {
  local script_path script_dir
  script_path="$1"
  script_dir="$(cd "$(dirname "$script_path")" && pwd)"
  cd "$script_dir" && git rev-parse --show-toplevel
}

run_repo_script() {
  local script_path relative_target repo_root
  script_path="$1"
  relative_target="$2"
  repo_root="$(resolve_repo_root "$script_path")"
  exec bash "$repo_root/$relative_target" "${@:3}"
}
