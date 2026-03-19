# Docker Build Rules

## Goal

Keep Docker-specific configuration repeatable and easy to audit.

## Rules

- Docker build scripts should load `.env` through shared helpers.
- Build args that vary by environment should be resolved in one helper, not duplicated across scripts.
- Wrapper commands at repo root should stay thin and forward into `scripts/`.
- Persona / identity / operating-rule files are not part of Docker cleanup.

## Current helper

- `scripts/lib/docker_env.sh`

## Current entrypoint

- `scripts/build_gaejae_image.sh`
