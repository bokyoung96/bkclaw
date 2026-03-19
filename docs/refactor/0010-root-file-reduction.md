# Root File Reduction

## Goal

Reduce root-level operational clutter so the repository root mostly contains project metadata, policy files, and core build/runtime definitions.

## Changes

Moved operational entrypoints out of the repo root:
- `build_gaejae_image` -> `bin/build_gaejae_image`
- `check_gaejae_db` -> `bin/check_gaejae_db`
- `restart_gaejae` -> `bin/restart_gaejae`
- `dispatch_discord.py` -> `scripts/discord/dispatch_discord.py`

## Rules

- Root should prefer long-lived project files over task wrappers.
- User-facing command shims belong under `bin/`.
- Operational scripts belong under `scripts/`.
- Persona / operating-rule files remain at root by design and are not cleanup targets.
