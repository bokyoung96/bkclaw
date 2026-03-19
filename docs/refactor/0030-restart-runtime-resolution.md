# Restart Runtime Resolution

## Problem

`./bin/restart_gaejae` failed on a synced local workspace because the script assumed `docker compose` could run from the repo root without an explicit compose file.

## Root cause

- The workspace repo (`bkclaw`) is not guaranteed to be the same directory that contains the compose file.
- The old script used `docker compose down/up` directly with no `-f` resolution.

## Fix

The restart script now:
1. tries to resolve a real compose file from known candidate paths
2. uses `docker compose -f <resolved-file>` when available
3. otherwise restarts the runtime through `openclaw gateway restart`
4. records the chosen runtime controller in the restart report

## Why this is not just a workaround

The real issue was runtime-controller resolution. The script now resolves the controller instead of blindly assuming the repo root is the compose root.

## Operator override

If needed, a specific compose file can be forced:

```bash
COMPOSE_FILE=/absolute/path/to/compose.yml ./bin/restart_gaejae
```
