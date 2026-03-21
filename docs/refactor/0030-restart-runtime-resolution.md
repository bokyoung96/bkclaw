# Restart Runtime Resolution

## Problem

`./bin/restart_gaejae` failed on a synced local workspace because the script assumed `docker compose` could run from the repo root without an explicit compose file.

## Root cause

- The workspace repo (`bkclaw`) is not guaranteed to be the same directory that contains the compose file.
- The old script used `docker compose down/up` directly with no `-f` resolution.

## Fix

The restart script now:
1. tries to resolve a real compose file from known candidate paths
2. includes the common local operator path `~/openclaw/docker-compose.yml`
3. uses `docker compose -f <resolved-file>` when available
4. otherwise restarts the runtime through `openclaw gateway restart`
5. records the chosen runtime controller in the restart report

## Why this is not just a workaround

The real issue was runtime-controller resolution. The script now resolves the controller instead of blindly assuming the repo root is the compose root.

## Operator override

If needed, a specific compose file can be forced:

```bash
COMPOSE_FILE=/absolute/path/to/compose.yml ./bin/restart_gaejae
```

## Host vs container path reminder

- `/home/node/.openclaw/workspace` is the container-internal workspace path.
- On a local Mac/host shell, operators should use host paths such as:
  - `~/.openclaw/workspace`
  - `~/openclaw`
- The restart command should therefore be documented and run with host paths, not the container path.


## Apply-step rule

After a fix, explicitly classify the required apply path:

- config file changed -> reload/restart runtime
- Dockerfile/image changed -> rebuild image, then restart
- workspace helper/script changed -> rerun helper; restart only if runtime boot path depends on it

This prevents false assumptions such as expecting a config-only restart to apply an image-level OpenClaw CLI upgrade.
