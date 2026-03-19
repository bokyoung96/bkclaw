#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=./load_env.sh
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/load_env.sh"
load_workspace_env

resolve_docker_build_args() {
  printf '%s\n' "--build-arg CLOUDFLARED_VERSION=${CLOUDFLARED_VERSION:-2026.2.1}"
}
