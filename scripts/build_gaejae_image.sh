#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_TAG="${IMAGE_TAG:-gaejae-v1:latest}"
DOCKERFILE_PATH="${DOCKERFILE_PATH:-$ROOT_DIR/Dockerfile.gaejae}"
CLOUDFLARED_VERSION="${CLOUDFLARED_VERSION:-2026.2.1}"

if [ ! -f "$DOCKERFILE_PATH" ]; then
  echo "[ERROR] Dockerfile not found: $DOCKERFILE_PATH" >&2
  exit 1
fi

cd "$ROOT_DIR"

echo "[build] dockerfile=$DOCKERFILE_PATH"
echo "[build] image_tag=$IMAGE_TAG"
echo "[build] cloudflared_version=$CLOUDFLARED_VERSION"

docker build \
  -f "$DOCKERFILE_PATH" \
  --build-arg CLOUDFLARED_VERSION="$CLOUDFLARED_VERSION" \
  -t "$IMAGE_TAG" \
  .

echo "[ok] built $IMAGE_TAG"
echo "[next] run: cd ~/openclaw && ./restart_gaejae"
