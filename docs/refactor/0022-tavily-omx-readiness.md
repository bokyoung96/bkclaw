# Tavily / OMX Readiness Check

## Result

OMX wrappers are present, and Tavily should be treated as a research-lane capability that must be verified at the **active runtime** layer, not only at the `.env` layer.

## Tavily

### Readiness rule
Tavily is considered ready only when all three are true:
1. `TAVILY_API_KEY` exists in workspace `.env`
2. the active runtime env exposes that key after restart
3. a small smoke search succeeds

### Operational note
- Do not claim `Tavily is missing` only because a project-local script or PATH binary is absent.
- First separate:
  - workspace config (`.env`)
  - active runtime env
  - project-local scripts or wrappers
- Tavily belongs to the **research agent / research lane** first.

## OMX

### Current baseline
- active OMX checkout exists at:
  - `/home/node/.openclaw/workspace/external/oh-my-codex`
- local wrappers exist under `bin/`
- OMX readiness should still be validated from a clean, operator-facing path when practical

## Important caveat

The repo must not mix up these layers when reporting:
1. OpenClaw runtime readiness
2. workspace helper/wrapper readiness
3. project-level execution readiness

This distinction matters because past confusion came from treating a project-context limitation as if the whole runtime lacked Tavily/Python support.

## Recommended next step

1. restart the runtime after Tavily key changes
2. verify active runtime env sees the new key
3. run one research-lane smoke search
4. only then label Tavily as ready in reports
