# Skill Refresh and Alignment

## Goal

Keep versioned skills aligned with the actual workspace structure instead of letting local-only operating assumptions drift away from the repo.

## Changes

- refreshed `discord-research-workspace` to describe the current real channel set instead of a stale default 4-channel pattern
- added versioned `discord-channel-actions` skill
- added versioned `agent-team-orchestration` skill

## Why

Skill drift causes operational confusion:
- stale channel assumptions
- missing notice/git formatting rules
- local-only skills not reflected in the repo

## Rule

Whenever the real workspace/channel model changes materially, versioned skills should be reviewed and refreshed as part of normal cleanup.
