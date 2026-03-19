# Restart Runbook

## Primary command

```bash
cd ~/.openclaw/workspace
./bin/restart_gaejae
```

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
