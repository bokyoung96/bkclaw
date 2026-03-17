#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/logs/openclaw_runtime_state"
mkdir -p "$STATE_DIR"

CONTAINER_NAME="${CONTAINER_NAME:-openclaw-openclaw-gateway-1}"
BASELINE_IMAGE_TAG="${BASELINE_IMAGE_TAG:-openclaw:local}"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[ERROR] python venv not found: $VENV_PYTHON" >&2
  exit 1
fi

IMAGE_ID="$(docker image inspect "$BASELINE_IMAGE_TAG" --format '{{.Id}}' 2>/dev/null || true)"
RUNNING_IMAGE_ID="$(docker inspect "$CONTAINER_NAME" --format '{{.Image}}' 2>/dev/null || true)"
UTC_NOW="$(date -u '+%Y-%m-%d %H:%M:%S UTC')"

"$VENV_PYTHON" -m pip freeze | sort > "$STATE_DIR/pip-freeze.baseline.txt"
cat > "$STATE_DIR/baseline.env" <<EOF
BASELINE_RECORDED_AT=$UTC_NOW
BASELINE_IMAGE_TAG=$BASELINE_IMAGE_TAG
BASELINE_IMAGE_ID=$IMAGE_ID
BASELINE_RUNNING_CONTAINER=$CONTAINER_NAME
BASELINE_RUNNING_IMAGE_ID=$RUNNING_IMAGE_ID
EOF

echo "[OK] baseline updated"
echo "- recorded_at: $UTC_NOW"
echo "- baseline_image_tag: $BASELINE_IMAGE_TAG"
echo "- baseline_image_id: ${IMAGE_ID:-unknown}"
echo "- running_image_id: ${RUNNING_IMAGE_ID:-unknown}"
