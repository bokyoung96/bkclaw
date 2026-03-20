#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BIN="${OLLAMA_BIN:-$HOME/.local/bin/ollama}"
HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
MODEL="${OLLAMA_EMBED_MODEL:-nomic-embed-text}"
LOG_FILE="${OLLAMA_LOG_FILE:-$HOME/.openclaw/logs/ollama.log}"
PID_FILE="${OLLAMA_PID_FILE:-$HOME/.openclaw/logs/ollama.pid}"

mkdir -p "$(dirname "$LOG_FILE")"

if [ ! -x "$OLLAMA_BIN" ]; then
  for candidate in \
    "$HOME/.local/bin/ollama" \
    "$HOME/.local/lib/ollama/bin/ollama" \
    "/usr/local/bin/ollama" \
    "/usr/local/ollama" \
    "$(command -v ollama 2>/dev/null || true)"
  do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then
      OLLAMA_BIN="$candidate"
      break
    fi
  done
fi

if [ ! -x "$OLLAMA_BIN" ]; then
  echo "[ERROR] ollama binary not found: $OLLAMA_BIN" >&2
  echo "[next] run: ~/.openclaw/workspace/scripts/install_ollama_user.sh" >&2
  exit 1
fi

if curl -fsS "http://$HOST/api/tags" >/dev/null 2>&1; then
  echo "[ok] ollama already serving on $HOST"
else
  nohup env OLLAMA_HOST="$HOST" "$OLLAMA_BIN" serve >"$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  for _ in $(seq 1 30); do
    if curl -fsS "http://$HOST/api/tags" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
fi

curl -fsS "http://$HOST/api/tags" >/dev/null
"$OLLAMA_BIN" pull "$MODEL"

echo "[ok] ollama serving on $HOST"
echo "[ok] model ready: $MODEL"
