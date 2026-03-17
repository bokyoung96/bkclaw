#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env}"
if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

REPORT_DIR="$ROOT_DIR/logs/openclaw_restart_reports"
STATE_DIR="$ROOT_DIR/logs/openclaw_runtime_state"
mkdir -p "$REPORT_DIR" "$STATE_DIR"

IMAGE_SOURCE_TAG="${IMAGE_SOURCE_TAG:-gaejae-v1:latest}"
COMPOSE_TARGET_TAG="${COMPOSE_TARGET_TAG:-openclaw:local}"
CONTAINER_NAME="${CONTAINER_NAME:-openclaw-openclaw-gateway-1}"
COMPOSE_CMD="${COMPOSE_CMD:-docker compose}"
OPENCLAW_STATUS_CMD="${OPENCLAW_STATUS_CMD:-openclaw status}"
DB_CHECK_SCRIPT="$ROOT_DIR/scripts/check_quant_db.sh"
TIME_ZONE="${TIME_ZONE:-Asia/Seoul}"
TIMESTAMP="$(TZ="$TIME_ZONE" date '+%Y%m%dT%H%M%S%z' | sed 's/+0900/KST/')"
REPORT_FILE="$REPORT_DIR/restart_report_$TIMESTAMP.txt"
STATUS_OUTPUT="$STATE_DIR/openclaw_status_$TIMESTAMP.txt"
PIP_SNAPSHOT="$STATE_DIR/pip-freeze.current.txt"
PIP_DIFF_FILE="$STATE_DIR/pip-freeze.diff.txt"
NOW_HUMAN="$(TZ="$TIME_ZONE" date '+%Y-%m-%d %H:%M:%S %Z')"
DEV_SEND_LOG="$STATE_DIR/dev_channel_send_$TIMESTAMP.log"

STEP="init"
RESULT="SUCCESS"
FAIL_REASON=""
NEXT_ACTION="none"
HEALTH_STATUS="unknown"
IMAGE_NAME="unknown"
IMAGE_ID="unknown"
CONTAINER_IMAGE_ID="unknown"
DB_STATUS="NOT_RUN"
DB_OUTPUT=""
CLOUDFLARED_STATUS="unknown"
IMAGE_REFRESH_STATUS="unknown"
IMAGE_REFRESH_DETAIL="baseline not checked"
STATUS_SUMMARY="not collected"
REPORT_LABEL="OPENCLAW RESTART REPORT"
DISPLAY_STEP="init"
DEV_SUMMARY_FILE="$REPORT_DIR/restart_summary_$TIMESTAMP.txt"
DEV_CHANNEL_ENABLED="${DEV_CHANNEL_ENABLED:-1}"
DEV_CHANNEL_TARGET="${DEV_CHANNEL_TARGET:-channel:1482514790768447590}"
DEV_CHANNEL_NAME="${DEV_CHANNEL_NAME:-discord}"
DEV_CHANNEL_SEND_STATUS="not sent"

cleanup() {
  if [ "$RESULT" != "SUCCESS" ]; then
    write_report
  fi
}
trap cleanup EXIT

write_report() {
  if [ "$RESULT" = "SUCCESS" ]; then
    DISPLAY_STEP="completed: $STEP"
  else
    DISPLAY_STEP="$STEP"
  fi

  cat > "$REPORT_FILE" <<EOF
[$REPORT_LABEL]
- Time: $NOW_HUMAN
- Result: $RESULT
- Step: $DISPLAY_STEP
- Failure Reason: ${FAIL_REASON:-none}
- Next Action: $NEXT_ACTION
- Source Image Tag: $IMAGE_SOURCE_TAG
- Compose Target Tag: $COMPOSE_TARGET_TAG
- Container: $CONTAINER_NAME
- Container Image: $IMAGE_NAME
- Container Image ID: $CONTAINER_IMAGE_ID
- Target Image ID: $IMAGE_ID
- Health: $HEALTH_STATUS
- Cloudflared: $CLOUDFLARED_STATUS
- Quant DB: $DB_STATUS
- Image Refresh Needed: $IMAGE_REFRESH_STATUS
- Image Refresh Detail: $IMAGE_REFRESH_DETAIL
- OpenClaw Status: $STATUS_SUMMARY
- Dev Channel Send: $DEV_CHANNEL_SEND_STATUS
- DB Output:
$DB_OUTPUT
EOF

  cat > "$DEV_SUMMARY_FILE" <<EOF
[$REPORT_LABEL]
- Time: $NOW_HUMAN
- Result: $RESULT
- Step: $DISPLAY_STEP
- Container Image: $IMAGE_NAME
- Health: $HEALTH_STATUS
- Cloudflared: $CLOUDFLARED_STATUS
- Quant DB: $DB_STATUS
- Image Refresh Needed: $IMAGE_REFRESH_STATUS
- Image Refresh Detail: $IMAGE_REFRESH_DETAIL
- OpenClaw Status: $STATUS_SUMMARY
EOF
}

send_dev_summary() {
  if [ "$DEV_CHANNEL_ENABLED" != "1" ]; then
    DEV_CHANNEL_SEND_STATUS="disabled"
    return 0
  fi

  if openclaw message send --channel "$DEV_CHANNEL_NAME" --target "$DEV_CHANNEL_TARGET" --message "$(cat "$DEV_SUMMARY_FILE")" >"$DEV_SEND_LOG" 2>&1; then
    DEV_CHANNEL_SEND_STATUS="sent: $DEV_CHANNEL_NAME $DEV_CHANNEL_TARGET"
  else
    DEV_CHANNEL_SEND_STATUS="failed: $DEV_CHANNEL_NAME $DEV_CHANNEL_TARGET (see $(basename "$DEV_SEND_LOG"))"
  fi
}

run_step() {
  STEP="$1"
  shift
  "$@"
}

STEP="tag-image"
docker tag "$IMAGE_SOURCE_TAG" "$COMPOSE_TARGET_TAG"
IMAGE_ID="$(docker image inspect "$COMPOSE_TARGET_TAG" --format '{{.Id}}')"

STEP="compose-down"
$COMPOSE_CMD down >/dev/null

STEP="compose-up"
$COMPOSE_CMD up -d >/dev/null

STEP="container-image"
IMAGE_NAME="$(docker inspect "$CONTAINER_NAME" --format '{{.Config.Image}}')"
CONTAINER_IMAGE_ID="$(docker inspect "$CONTAINER_NAME" --format '{{.Image}}')"
if [ "$IMAGE_NAME" != "$COMPOSE_TARGET_TAG" ]; then
  RESULT="FAIL"
  FAIL_REASON="container image mismatch: expected $COMPOSE_TARGET_TAG got $IMAGE_NAME"
  NEXT_ACTION="check compose service image configuration"
  write_report
  cat "$REPORT_FILE"
  exit 1
fi

STEP="container-health"
HEALTH_WAIT_SECONDS="${HEALTH_WAIT_SECONDS:-120}"
HEALTH_POLL_INTERVAL="${HEALTH_POLL_INTERVAL:-2}"
HEALTH_ELAPSED=0
while true; do
  HEALTH_STATUS="$(docker inspect "$CONTAINER_NAME" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}')"
  if [ "$HEALTH_STATUS" = "healthy" ] || [ "$HEALTH_STATUS" = "no-healthcheck" ]; then
    break
  fi
  if [ "$HEALTH_STATUS" = "unhealthy" ]; then
    RESULT="FAIL"
    FAIL_REASON="container health is unhealthy"
    NEXT_ACTION="review docker compose logs for gateway"
    write_report
    cat "$REPORT_FILE"
    exit 1
  fi
  if [ "$HEALTH_ELAPSED" -ge "$HEALTH_WAIT_SECONDS" ]; then
    RESULT="FAIL"
    FAIL_REASON="container health remained $HEALTH_STATUS after ${HEALTH_WAIT_SECONDS}s"
    NEXT_ACTION="review docker compose logs for gateway"
    write_report
    cat "$REPORT_FILE"
    exit 1
  fi
  sleep "$HEALTH_POLL_INTERVAL"
  HEALTH_ELAPSED=$((HEALTH_ELAPSED + HEALTH_POLL_INTERVAL))
done

STEP="cloudflared-check"
if docker exec -i "$CONTAINER_NAME" bash -lc 'command -v cloudflared >/dev/null 2>&1'; then
  CLOUDFLARED_STATUS="INSTALLED"
else
  CLOUDFLARED_STATUS="MISSING"
fi

STEP="openclaw-status"
if $OPENCLAW_STATUS_CMD > "$STATUS_OUTPUT" 2>&1; then
  STATUS_SUMMARY="captured: $(basename "$STATUS_OUTPUT")"
else
  STATUS_SUMMARY="failed: $(basename "$STATUS_OUTPUT")"
fi

STEP="db-check"
if DB_OUTPUT="$(bash "$DB_CHECK_SCRIPT" 2>&1)"; then
  DB_STATUS="OK"
else
  DB_STATUS="FAIL"
  RESULT="FAIL"
  FAIL_REASON="quant DB verification failed"
  NEXT_ACTION="inspect DB output and cloudflared/runtime configuration"
fi

STEP="runtime-drift"
if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  "$ROOT_DIR/.venv/bin/python" -m pip freeze | sort > "$PIP_SNAPSHOT"
  if [ -f "$STATE_DIR/pip-freeze.baseline.txt" ]; then
    if diff -u "$STATE_DIR/pip-freeze.baseline.txt" "$PIP_SNAPSHOT" > "$PIP_DIFF_FILE"; then
      IMAGE_REFRESH_STATUS="NO"
      IMAGE_REFRESH_DETAIL="baseline matches current pip freeze"
    else
      IMAGE_REFRESH_STATUS="YES"
      IMAGE_REFRESH_DETAIL="python environment changed since last baseline: $(basename "$PIP_DIFF_FILE")"
    fi
  else
    IMAGE_REFRESH_STATUS="YES"
    IMAGE_REFRESH_DETAIL="baseline missing; run scripts/mark_image_baseline.sh after validating image"
  fi
else
  IMAGE_REFRESH_STATUS="UNKNOWN"
  IMAGE_REFRESH_DETAIL="workspace venv missing; skipped pip freeze comparison"
fi

if [ "$RESULT" = "SUCCESS" ]; then
  NEXT_ACTION="none"
  FAIL_REASON="none"
fi

write_report
send_dev_summary
write_report
cat "$REPORT_FILE"
printf '\n[DEV SUMMARY]\n'
cat "$DEV_SUMMARY_FILE"

if [ "$RESULT" != "SUCCESS" ]; then
  exit 1
fi
