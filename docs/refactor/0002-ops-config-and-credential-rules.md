# Ops Rules: Config, Credentials, and Repeated Runtime Issues

## Goal

Frequent operational failures should not remain hidden in chat history.
They should be managed in one place, encoded into scripts/helpers when possible,
and treated as workspace-level rules.

## Rules

### 1. Credentials live in `.env`
- Store recurring credentials and config values in `.env`.
- Do not hardcode them into Dockerfiles, scripts, or ad-hoc command snippets.
- Do not re-expose secrets in chat when the value is already known locally.

### 2. Scripts should load config consistently
- When a script depends on GitHub auth or other runtime auth, load `.env` explicitly.
- Prefer a single helper / wrapper over per-command improvisation.
- If a credential helper depends on environment variables, that dependency must be documented near the helper.

### 3. Repeated failures deserve a permanent fix
Examples:
- git push auth not loaded into shell
- runtime config mismatch between docker and host
- media upload path not allowed from workspace
- channel delivery path differs from local inspection path

For repeated issues:
1. document the rule,
2. encode it in a helper/script if possible,
3. add a quick validation check.

### 4. Docker/runtime truth wins over assumptions
- When verifying OpenClaw/runtime behavior, prefer the actual docker/runtime environment over host guesses.
- A config is not "set" until it is confirmed from the environment that actually runs the service.

### 5. Git operations should use the workspace repo contract
- Workspace repo: `bkclaw`
- Default working branch: `gaejae`
- Refactor work should prefer isolated branches/worktrees when the main workspace tree is dirty.

## Concrete implications

- GitHub push helpers should work from `.env`-backed credentials.
- Repeated operational fixes should be added to docs and then to code/scripts.
- The assistant should check the real repo/worktree before cloning unrelated upstream repos.

## Follow-up implementation ideas

- add a shared `.env` loader helper for scripts
- add a git push wrapper that sources `.env` before invoking git
- add a runtime self-check command for auth/config-sensitive operations
