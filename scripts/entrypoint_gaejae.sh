#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BOOTSTRAP_SCRIPT="/home/node/.openclaw/workspace/scripts/start_local_ollama.sh"
OLLAMA_BOOTSTRAP_LOG="${HOME}/.openclaw/logs/ollama-bootstrap.log"
OLLAMA_AUTO_START="${OLLAMA_AUTO_START:-1}"

mkdir -p "$(dirname "$OLLAMA_BOOTSTRAP_LOG")"

if [ "$OLLAMA_AUTO_START" = "1" ] || [ "$OLLAMA_AUTO_START" = "true" ] || [ "$OLLAMA_AUTO_START" = "yes" ] || [ "$OLLAMA_AUTO_START" = "on" ]; then
  if [ -x "$OLLAMA_BOOTSTRAP_SCRIPT" ]; then
    (
      if ! "$OLLAMA_BOOTSTRAP_SCRIPT" >>"$OLLAMA_BOOTSTRAP_LOG" 2>&1; then
        echo "[warn] ollama bootstrap failed; see $OLLAMA_BOOTSTRAP_LOG" >&2
      fi
    ) &
  else
    echo "[warn] ollama bootstrap script missing: $OLLAMA_BOOTSTRAP_SCRIPT" >&2
  fi
fi

exec docker-entrypoint.sh "$@"
