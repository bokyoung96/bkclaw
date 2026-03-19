# Root Wrapper Policy

## Goal

Keep root-level command files extremely small and deterministic.

## Rules

- Root wrappers should not hardcode absolute workspace paths.
- Root wrappers should delegate into `scripts/` through a shared helper.
- Reusable execution logic belongs in `scripts/` or `src/`, not at repo root.

## Covered wrappers

- `build_gaejae_image`
- `check_gaejae_db`
- `restart_gaejae`
