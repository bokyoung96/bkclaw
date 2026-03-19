# Git / Env Helper Rules

## Why

Some recurring failures were not real auth failures; they were environment-loading failures.
That means the fix should be part of the workspace, not left to memory.

## Rules

- shared shell helpers should source the workspace `.env` through a common loader
- git credential helpers should be workspace-owned and self-documenting
- repeatable push flows should use a wrapper script rather than an ad-hoc sourced shell

## Helpers introduced

- `scripts/lib/load_env.sh`
- `scripts/git-credential-env.sh`
- `scripts/git_push_current.sh`

## Usage

```bash
./scripts/git_push_current.sh
./scripts/git_push_current.sh refactor/agent-runtime-5step
```
