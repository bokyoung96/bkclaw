# Git Notify Format and Preflight

## Goal

Improve git-channel readability and make refactor/preflight cleanup an explicit step before pushes.

## Git channel format

Use a compact Discord-friendly message with:
- emoji by event type
- branch
- action
- optional detail line

Examples:
- `🌱` branch created
- `🧱` commit batch
- `📤` push complete
- `🔀` PR created
- `✅` merge complete
- `🧹` branch cleanup

## Pre-push rule

Before push, check:
1. is there root clutter that should move into `bin/`, `scripts/`, `src/`, or `docs/`?
2. is repetitive logic still duplicated?
3. are unnecessary/generated files hanging around?
4. does workspace layout still pass the self-check?

## Helper

```bash
cd ~/.openclaw/workspace
./scripts/pre_push_refactor_check.sh
```
