# Git Runtime Hardening

## Goal

Keep git/GitHub automation stable across docker restarts, compose down/up cycles, and worktree changes.

## Problems addressed

1. `gh` installed only in user-local runtime can disappear after container rebuild/restart
2. repo-local `credential.helper` can point at a stale worktree path

## Fixes

### Docker image
`Dockerfile.gaejae` now installs:
- `cloudflared`
- `@openai/codex`
- `gh`

This makes `gh` available after rebuilds instead of relying only on ad-hoc user-local install.

### Dynamic git credential helper
Use a repo-root-resolving helper instead of a worktree-specific absolute path.

Helper script:
- `scripts/git_configure_auth.sh`

Behavior:
- configures `credential.helper` using a dynamic shell helper
- resolves the current repo root at execution time
- avoids stale references to old `/tmp/...` worktrees

## Operator command

```bash
cd ~/.openclaw/workspace
./scripts/git_configure_auth.sh
```

## Recommended use

Run the helper after significant repo/worktree changes or after restoring a workspace into a new container.
