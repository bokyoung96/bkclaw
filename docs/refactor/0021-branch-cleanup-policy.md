# Branch Cleanup Policy

## Goal

Do not let merged branches accumulate.

## Default rule

Merged working branches should be deleted by default.

## Keep a branch only if

- the PR is still open
- immediate follow-up work will continue on the same branch
- the branch is serving as a temporary recovery point

## Cleanup order

1. confirm PR is merged
2. confirm `origin/main` contains the merge
3. delete the remote branch
4. delete local worktree / local branch copy

## Why

Short-lived branches keep the repo easier to reason about and reduce stale context.
