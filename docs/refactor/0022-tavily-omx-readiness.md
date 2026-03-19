# Tavily / OMX Readiness Check

## Result

Both Tavily and OMX are usable, but there is an important operational distinction between the clean `main`-based worktree and the user's long-lived `gaejae` working tree.

## Findings

### Tavily
- `TAVILY_API_KEY` exists in workspace `.env`
- local Tavily skills are present:
  - `skills/tavily-research-agent/`
  - `skills/openclaw-tavily-search/`
- Tavily is ready to be used as a research-lane tool

### OMX
- active OMX checkout exists at:
  - `/home/node/.openclaw/workspace/external/oh-my-codex`
- local OMX state directory exists under `.omx/`
- `./bin/omx --help` works from the clean `main`-based worktree
- OMX surface confirms useful commands exist:
  - `omx doctor`
  - `omx explore`
  - `omx team`
  - `omx ralph`
  - `omx autoresearch`
  - `omx sparkshell`

## Important operational caveat

The long-lived workspace branch `gaejae` is heavily ahead/dirty relative to `main` and does not reflect the newly-merged `bin/omx` baseline yet.

That means:
- readiness checks should prefer a clean `main`-based worktree
- repo-level operational docs and wrappers should be validated against `main`
- if `gaejae` is intended to remain a daily driver, it should eventually be rebased/synced or retired in favor of the current baseline

## Recommended next step

1. use Tavily in a small research-lane test
2. run a lightweight OMX test from a clean worktree
3. test Ralph mode in a tightly scoped task
4. only then design the broader team-orchestration layer
