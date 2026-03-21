# Runtime Verification and Channel Delivery

## Purpose

Prevent two recurring classes of mistakes:
1. declaring tools/runtime support missing before verifying the right layer
2. treating session-level acknowledgements as if they proved Discord-visible delivery

## Runtime verification order

Before saying `없다`, `안 된다`, or `미설치`, verify in this order:
1. binary exists
2. PATH exposure
3. env/token injection
4. host vs container path differences
5. user-provided runtime/Dockerfile assumptions already in place

## Reporting layers

Always separate these three layers in reports:
- **Runtime layer**: current OpenClaw container / active env / system binaries
- **Workspace layer**: shared `.venv`, shared scripts, shared `.env`
- **Project layer**: project-local Dockerfile, local env, project-only validation

## Channel delivery rules

### Current channel
- normal replies use the current session's built-in routing

### Cross-session routing
- `sessions_send` proves session injection / routing only
- it does not, by itself, prove Discord-visible delivery

### Direct provider delivery
- `openclaw message send --channel discord --target ...` should be preferred when delivery proof matters
- `messageId` or actual visible chat delivery is the strongest completion proof

## Completion posture

When in doubt, report separately:
- config changed
- runtime reloaded
- session routed
- visible delivery confirmed / unconfirmed

Do not collapse these into one vague `done`.
