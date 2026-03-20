# 0036 — Activate workspace .env in gateway entrypoint

## Problem
Secrets such as `TAVILY_API_KEY` could exist on disk in `~/.openclaw/workspace/.env` but still be absent from the active gateway/runtime environment.
That created a mismatch between:
- disk state
- active gateway snapshot

## Root cause
The custom gateway entrypoint handled Ollama bootstrap, but it did not explicitly source the workspace `.env` before starting the main OpenClaw process.

## Fix
- source `/home/node/.openclaw/workspace/.env` in `scripts/entrypoint_gaejae.sh`
- export loaded values into the gateway process environment
- keep this ahead of Ollama bootstrap and `docker-entrypoint.sh`

## Expected effect
After Docker restart / `/new` / new runtime creation, variables kept in workspace `.env` (including `TAVILY_API_KEY`) should be visible to the active gateway/runtime snapshot instead of only existing on disk.

## Validation
- rebuild `gaejae-openclaw:latest`
- restart compose with `OPENCLAW_IMAGE=gaejae-openclaw:latest`
- verify env in gateway container and in agent runtime
