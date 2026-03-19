# Final Ops Baseline

## What this stage establishes

This stage turns the workspace into a more stable operating baseline by making the following explicit:

- where user-facing commands live (`bin/`)
- how to restart the agent/runtime after drift or rebuild
- which root files are protected by design
- how Git/GitHub/Discord operations connect to daily use
- how to quickly detect root-level clutter regression

## Most important operator commands

```bash
cd ~/.openclaw/workspace
./bin/build_gaejae_image
./bin/restart_gaejae
./bin/check_gaejae_db
python3 scripts/check_workspace_layout.py
```
