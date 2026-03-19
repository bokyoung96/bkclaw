# Gaejae OMX Ralph Launch Path

## Goal

Give Gaejae a stable, non-fragile way to launch OMX Ralph without depending on ambiguous install layers.

## Decision

Use a wrapper-based launch path:

- `bin/omx`
  - prefers globally installed OMX under `~/.local/bin/omx`
  - falls back to any `omx` visible on `PATH`
  - otherwise falls back to repo-local `external/oh-my-codex/bin/omx.js`
- `bin/ralph`
  - stable convenience entrypoint for `omx ralph ...`

## Why this is the cleanest path

- avoids depending on Python/pip layers entirely
- keeps Codex/OMX in the Node CLI lane where they naturally belong
- survives both operator styles:
  - global npm installation available
  - repo-local OMX checkout only
- gives chat automation a single predictable entrypoint

## Operator examples

```bash
cd ~/.openclaw/workspace
./bin/omx --version
./bin/ralph "fix the flaky notifier path with verification"
./bin/ralph --prd "ship a reusable operator command for release notes"
```

## Gaejae behavior recommendation

When a user explicitly asks for Ralph / persistent completion / don't-stop-until-done execution, Gaejae should prefer the wrapper entrypoint instead of hardcoding a repo path:

```bash
cd ~/.openclaw/workspace
./bin/ralph "<task>"
```

This keeps the agent-facing command stable even if the actual OMX install source changes later.
