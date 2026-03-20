# 0035 — Use direct Discord delivery for git channel

## Problem
Git channel `1483989656470294548` became unreliable when addressed via `sessions_send`.
The same session key text appeared with a `webchat` delivery context instead of the expected Discord context, so session-routed sends could be consumed by the wrong session.

## Root cause
- session-key collision / stale session mapping
- `sessions_send` acknowledged delivery intent, but that was not reliable proof of actual Discord delivery
- git completion reporting was therefore vulnerable to false positives

## Fix
- prefer direct Discord delivery for the git channel:
  - `openclaw message send --channel discord --target channel:1483989656470294548`
  - or `scripts/notify_git_channel.sh`
- require returned `messageId` as the primary proof of delivery
- keep git completion reporting separate from delivery confirmation

## Operational rule
For git channel notifications, do not use `sessions_send` as the primary path while the session-key collision remains possible.
Use direct Discord send and report the returned `messageId` when available.
