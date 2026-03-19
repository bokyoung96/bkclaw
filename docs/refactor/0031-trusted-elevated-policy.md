# Trusted Elevated Policy Baseline

## Problem

Issue #16 asked whether trusted Discord channels could get a durable `elevated=full` posture instead of depending on ad-hoc per-session behavior.

## Current behavior

The persistent path is not a single knob. It is the combination of:

1. `agents.defaults.elevatedDefault = "full"`
2. `tools.elevated.enabled = true`
3. `tools.elevated.allowFrom.discord` containing the trusted operator id
4. trusted Discord channels being allowlisted
5. `channels.discord.execApprovals` still requiring the trusted approver in DM

That means:
- trusted channels can start from a stronger default execution posture
- but explicit approval flow still exists for exec approval routing
- session/model hiccups can still happen independently of config correctness

## Why this issue looked inconsistent

There are two separate layers:

- **persistent config layer**
  - controls whether elevated host execution is allowed by default for the runtime
- **live session / model layer**
  - can still fail because of model errors, retries, or per-request execution problems

So a failed session is not sufficient evidence that the durable elevated policy is missing.

## Resolution

This repo now includes an executable verification path:

```bash
python3 scripts/check_trusted_elevated_policy.py
```

The check confirms the current trusted elevated baseline for:
- trusted operator id `530011557837406218`
- trusted user allowlists on both `discord` and `webchat`
- `#chat` channel `1482511006440620072`
- `#main` channel `1481805554157359327`
- `#dev` channel `1482514790768447590`
- announcement thread `1484048004779474995`

## Policy recommendation

For this workspace, the safe baseline is:
- keep `agents.defaults.elevatedDefault = "full"`
- restrict `tools.elevated.allowFrom` to the trusted operator only
- allow the trusted operator on both `discord` and `webchat`
- treat `#chat`, `#dev`, and `#main` as the primary elevated-capable Discord lanes
- keep Discord `execApprovals.target = "dm"`
- keep channel allowlists explicit
- verify config changes with the check script instead of relying on chat-session impressions alone

## Acceptance mapping

- Document current behavior ✅
- Recommend a safe default policy ✅
- Provide a durable config verification path instead of manual toggling ✅

## Operator note

This resolves the configuration question for issue #16.
The intended operator posture is:
- the trusted user can use elevated flows from DM / direct trusted-user contexts
- the primary Discord elevated lanes are `#chat`, `#dev`, and `#main`

If a future session still fails, investigate runtime/model/tool execution separately rather than reopening the policy question first.
