#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env}"
if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

CONTAINER_NAME="${CONTAINER_NAME:-openclaw-openclaw-gateway-1}"
WORKSPACE_VENV="${WORKSPACE_VENV:-/home/node/.openclaw/workspace/.venv/bin/activate}"
DB_USER="${QUANT_DB_USER:-}"
DB_PASSWORD="${QUANT_DB_PASSWORD:-}"
PYTHON_BIN="${PYTHON_BIN:-python}"

if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
  echo "[ERROR] QUANT_DB_USER / QUANT_DB_PASSWORD not set. Use $ENV_FILE" >&2
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -Fxq "$CONTAINER_NAME"; then
  echo "[ERROR] container not running: $CONTAINER_NAME" >&2
  exit 1
fi

docker exec -i "$CONTAINER_NAME" bash -lc ". '$WORKSPACE_VENV' && $PYTHON_BIN -c \"from topquant_ksk.db import DBConnection; conn = DBConnection(db_user=\\\"$DB_USER\\\", db_password=\\\"$DB_PASSWORD\\\", local_host=False); print(conn.tools.check_existing_tables(detailed_column_date=False))\""
