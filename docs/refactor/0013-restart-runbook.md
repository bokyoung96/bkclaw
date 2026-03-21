# Restart Runbook

## Primary command

```bash
cd ~/.openclaw/workspace
./bin/restart_gaejae
```

If the synced local repo lives under `~/openclaw` instead:

```bash
cd ~/openclaw
./bin/restart_gaejae
```

Do not use `/home/node/.openclaw/workspace` from a Mac/host shell.
That path is container-internal.

## When to use

Use this when:
- OpenClaw/gateway/container behavior looks stale
- the image was rebuilt and should be reloaded
- you want an end-to-end restart + verification + dev summary send

## Related commands

### Rebuild image first
```bash
cd ~/.openclaw/workspace
./bin/build_gaejae_image
./bin/restart_gaejae
```

### Rebuild 후 git/GitHub helper 재고정
```bash
cd ~/.openclaw/workspace
./scripts/git_configure_auth.sh
```

### Gateway-only restart
```bash
openclaw gateway restart
```

### Check current gateway state
```bash
openclaw gateway status
```

### Validate DB access only
```bash
cd ~/.openclaw/workspace
./bin/check_gaejae_db
```

### Re-freeze baseline after validating a new image/runtime
```bash
cd ~/.openclaw/workspace
./scripts/mark_image_baseline.sh
```

## Expected outputs

- restart report written under `logs/openclaw_restart_reports/`
- runtime state artifacts written under `logs/openclaw_runtime_state/`
- dev summary sent to the configured dev Discord channel when enabled


## Runtime-change classification

Treat restart work in three buckets:

1. **Config-only change**
   - examples: allowlists, sandbox mode, trusted proxies
   - requires runtime reload / gateway restart semantics

2. **Image-level change**
   - examples: OpenClaw CLI version, ollama binary, cloudflared, entrypoint PATH
   - requires image rebuild + container restart

3. **Workspace-only change**
   - examples: scripts, skills, docs, reports, helper checks
   - may require no restart unless entrypoint/runtime wiring depends on it

Operator rule: do not collapse these into one vague restart story. State which layer changed and what apply step is required.
