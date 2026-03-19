# Docker Runtime Paths

## Goal

Preserve the cleaned operational entrypoints across rebuilds by making the expected runtime PATH explicit.

## Current PATH additions

- `/home/node/.openclaw/workspace/bin`
- `/home/node/.local/bin`

## Why

- `bin/` now holds user-facing workspace commands.
- `.local/bin` holds user-space tools such as `gh`.
- The workspace is bind-mounted at runtime, so these paths remain useful after rebuilds.
