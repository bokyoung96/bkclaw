# GitHub CLI Automation Rules

## Goal

Promote GitHub operations from ad-hoc terminal steps to repeatable workspace automation.

## Rules

- `git` handles local working tree operations.
- `gh` handles PR creation, PR inspection, checks, and merges.
- `gh` commands should load `.env` through shared helpers so `GH_TOKEN` is always present.
- repo-specific defaults should be explicit for this workspace.

## Repo defaults

- repo: `bokyoung96/bkclaw`
- default base branch: `main`
- default day-to-day working branch: `gaejae`

## Helpers

- `scripts/lib/github_env.sh`
- `scripts/gh_pr_create.sh`
- `scripts/gh_pr_merge.sh`

## Example flows

```bash
./scripts/git_push_current.sh refactor/agent-runtime-5step
./scripts/gh_pr_create.sh refactor/agent-runtime-5step main "refactor: agent runtime cleanup"
./scripts/gh_pr_merge.sh
```
