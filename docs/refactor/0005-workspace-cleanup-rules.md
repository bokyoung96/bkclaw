# Workspace Cleanup Rules

## Scope

Cleanup should target operational clutter and duplicated execution logic.
It should not rewrite persona, identity, user preference, heartbeat, or operating-rule files unless explicitly requested.

## Safe cleanup targets

- duplicated env-loading snippets in scripts
- duplicated build/push helper logic
- thin wrapper scripts that can be standardized
- ad-hoc channel target maps embedded in entry scripts
- undocumented build/runtime knobs that belong in `.env.example`

## Current cleanup progress

- shared env loader introduced
- git push wrapper introduced
- docker build env helper introduced
- discord target mapping extracted from entry script
- `.env.example` extended with auth/build knobs

## Not to touch in cleanup passes

- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `AGENTS.md`
- `HEARTBEAT.md`
- user-authored operating rules unless asked
