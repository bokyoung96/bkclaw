#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib/github_env.sh
. "$SCRIPT_DIR/lib/github_env.sh"
load_workspace_env

TARGET_CHANNEL="${GIT_NOTIFY_CHANNEL_TARGET:-channel:1483989656470294548}"
ACTION="${1:-}"
BRANCH="${2:-}"
DETAIL="${3:-}"

if [ -z "$ACTION" ]; then
  echo "usage: $0 <action> [branch] [detail]" >&2
  exit 1
fi

EMOJI="🧩"
case "$ACTION" in
  branch-created) EMOJI="🌱" ;;
  commit-batch) EMOJI="🧱" ;;
  push-complete) EMOJI="📤" ;;
  pr-created) EMOJI="🔀" ;;
  merge-complete) EMOJI="✅" ;;
  conflict-resolved) EMOJI="🛠️" ;;
  branch-cleanup) EMOJI="🧹" ;;
  *) EMOJI="🧩" ;;
esac

MESSAGE="$EMOJI **bkclaw git update**"
if [ -n "$BRANCH" ]; then
  MESSAGE="$MESSAGE\n- branch: \
\\`$BRANCH\\`"
fi
MESSAGE="$MESSAGE\n- action: $ACTION"
if [ -n "$DETAIL" ]; then
  MESSAGE="$MESSAGE\n- detail: $DETAIL"
fi

openclaw message send \
  --channel discord \
  --target "$TARGET_CHANNEL" \
  --message "$MESSAGE" \
  --json >/dev/null

echo "[git-notify] sent to $TARGET_CHANNEL"
