#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/github_env.sh
. "$SCRIPT_DIR/lib/github_env.sh"
load_workspace_env

TARGET_CHANNEL="${GIT_NOTIFY_CHANNEL_TARGET:-channel:1483989656470294548}"
MESSAGE="${1:-}"

if [ -z "$MESSAGE" ]; then
  echo "usage: $0 '<message>'" >&2
  exit 1
fi

openclaw message send \
  --channel discord \
  --target "$TARGET_CHANNEL" \
  --message "$MESSAGE" \
  --json >/dev/null

echo "[git-notify] sent to $TARGET_CHANNEL"
