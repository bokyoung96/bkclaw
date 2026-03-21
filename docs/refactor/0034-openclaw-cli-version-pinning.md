# OpenClaw CLI Version Pinning

## Problem

Runtime behavior after restart was still using `/usr/local/bin/openclaw` from the base image (`2026.3.11`), even though a newer user-local install had been tested earlier.

That meant:
- restarts kept returning to the older CLI inside the container
- config warnings and behavior differences remained tied to the base-image OpenClaw version
- local `npm i -g openclaw@latest` was not a durable fix across container recreation

## Fix

Pin the OpenClaw CLI version directly in `Dockerfile.gaejae`.

## Rule

If the intended fix depends on the OpenClaw CLI version itself, do not rely on an in-container ad-hoc install.
Bake the desired OpenClaw version into the image, rebuild, and restart.

## Operator flow

```bash
cd ~/.openclaw/workspace
./bin/build_gaejae_image
./bin/restart_gaejae
```

## Why this matters

This keeps runtime behavior reproducible across:
- restart
- container recreation
- gateway bootstrap
- future troubleshooting
