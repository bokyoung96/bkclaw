# OMX Baseline

## Goal

Treat oh-my-codex (OMX) as an operational runtime that should be launched consistently from this workspace.

## Local source

- active local checkout path: `/home/node/.openclaw/workspace/external/oh-my-codex`
- wrapper override: `OMX_DIR=/custom/path ./bin/omx ...`

## User-facing command

```bash
./bin/omx --help
```

## Why this wrapper exists

- avoids remembering deep vendor paths
- keeps OMX invocation aligned with repo layout rules
- gives one stable operator entrypoint even if the vendor directory moves later

## Intended use in this workspace

- team / orchestration workflows
- Codex-first multi-agent execution
- persistent runtime state under `.omx/`
- operator-facing status / doctor / team commands

## Important note

OMX is a runtime around Codex, not a replacement for the repository's own branch/ops discipline.
It should follow the same cleanup principles:
- avoid root clutter
- prefer stable wrappers in `bin/`
- document runbooks instead of relying on memory alone
