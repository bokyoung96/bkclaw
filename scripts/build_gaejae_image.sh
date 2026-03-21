#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=./lib/load_env.sh
. "$ROOT_DIR/scripts/lib/docker_env.sh"
IMAGE_TAG="${IMAGE_TAG:-gaejae-openclaw:latest}"
DOCKERFILE_PATH="${DOCKERFILE_PATH:-$ROOT_DIR/Dockerfile.gaejae}"

if [ ! -f "$DOCKERFILE_PATH" ]; then
  echo "[ERROR] Dockerfile not found: $DOCKERFILE_PATH" >&2
  exit 1
fi

cd "$ROOT_DIR"

echo "[build] dockerfile=$DOCKERFILE_PATH"
echo "[build] image_tag=$IMAGE_TAG"
echo "[build] cloudflared_version=${CLOUDFLARED_VERSION:-2026.2.1}"
echo "[build] openclaw_version=${OPENCLAW_VERSION:-2026.3.13}"

readarray -t BUILD_ARGS < <(resolve_docker_build_args)

docker build \
  -f "$DOCKERFILE_PATH" \
  "${BUILD_ARGS[@]}" \
  -t "$IMAGE_TAG" \
  .

echo "[ok] built $IMAGE_TAG"
echo "[next] run: cd ~/.openclaw/workspace && ./bin/restart_gaejae"
echo "[next] then: cd ~/.openclaw/workspace && ./scripts/git_configure_auth.sh"
