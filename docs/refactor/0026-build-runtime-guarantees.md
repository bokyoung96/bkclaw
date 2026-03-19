# Build Runtime Guarantees

## Goal

Document what the image build is expected to preserve across docker compose down/up and rebuild cycles.

## Current guarantees from `Dockerfile.gaejae`

The built image is expected to provide:
- `cloudflared`
- `codex`
- `gh`
- runtime PATH including:
  - `/home/node/.openclaw/workspace/bin`
  - `/home/node/.local/bin`

## Operational meaning

After rebuild/restart, the operator should not have to re-install these tools manually just to resume normal git/gh/Codex workflows.

## Follow-up check

After rebuild:
```bash
cd ~/.openclaw/workspace
./bin/restart_gaejae
./scripts/git_configure_auth.sh
```
