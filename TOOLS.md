# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Runtime Verification Rules

- After Docker restart, `/new`, or runtime reset, do not jump straight to `없다`, `안 된다`, or `미설치`.
- Verify in this order before concluding failure:
  1. binary exists
  2. PATH exposure
  3. env/token injection
  4. host vs container path differences
  5. user-provided runtime/Dockerfile assumptions already in place
- Separate these layers explicitly when reporting:
  - 운영 런타임 (current OpenClaw container/runtime)
  - workspace 실행환경 (`.venv`, shared scripts, shared env)
  - 프로젝트 실행환경 (project-local Dockerfile/env/tests)
- If something is not yet proven, say `현재 내가 잡은 경로/세션에서는 아직 확인되지 않았다` rather than `없다`.

## Shared Python / Quant Runtime Rules

- Canonical shared Python environment for installed libraries:
  - interpreter: `/home/node/.openclaw/workspace/.venv/bin/python`
  - pip: `/home/node/.openclaw/workspace/.venv/bin/python -m pip`
- When the user asks whether Python or a library exists, check the shared venv before concluding it is missing.
- Do not answer from `/usr/bin/python3` alone when the shared venv may contain the actual user-installed stack.
- For strategy/backtest work, prefer explicit execution through the shared venv.
- If visibility differs by session, report the layers separately instead of collapsing to `없다`.

## Quant-Team Intake Sync Rule

- The canonical entry is `quant-team/QUANT_TEAM_ENTRY.md`.
- In quant-team contexts, do **not** jump from the first request straight to strategy ideas.
- Ask run-policy first:
  1. iteration / rounds
  2. strategies per round
  3. reporting cadence
  4. stop conditions
  5. git/reporting scope when relevant
- Then ask execution assumptions:
  1. universe
  2. test period
  3. benchmark
  4. transaction cost / slippage
  5. rebalance cadence
  6. structure
  7. risk constraints

## Tavily Research Lane Rules

- Treat Tavily as a **research-agent lane** capability first, not a coding-lane default.
- `TAVILY_API_KEY` existing in `.env` is not enough to declare readiness.
- Tavily readiness requires all three when relevant:
  1. key exists in `.env`
  2. key is visible in active runtime env after restart
  3. a small smoke search succeeds
- Report Tavily failures by layer:
  - key/config issue
  - active runtime env issue
  - provider/search execution issue
- Do not say `없다`, `안 된다`, `못 쓴다` before the preflight layers are checked.
- Prefer `./bin/check_tavily_ready` as the first helper for Tavily readiness checks.

## Large-work Questioning Rules

- For strategy/backtest/research-heavy work, prefer at least one explicit scope-lock question turn before broad execution.
- Separate:
  1. what the user must decide
  2. what the agent will execute
- Preferred phrasing:
  - `시작 전에 아래만 잠그겠습니다.`
  - `바로 구현보다 먼저 범위와 탈락 기준을 맞추겠습니다.`
- If assumptions are still open, do not jump straight to implementation or recommendation.

## Long Task Progress Rules

- For tasks likely to exceed about 10 minutes, provide explicit progress posture instead of going silent.
- Separate status as one of:
  - `IN_PROGRESS`
  - `BLOCKED`
  - `WAITING_ON_USER`
  - `DONE`
- For meaningful long tasks, prefer leaving a progress artifact under `logs/progress/` via `./bin/progress_note`.
- If the user wants proactive mid-task updates without re-prompting, prefer `./bin/long_task_watch` with a real channel target.
- Mid-task updates should mention:
  - current phase
  - what finished
  - what is still running
  - whether there is a blocker
- Silence for the entire duration of a long task should be treated as a quality issue unless the user explicitly wants silent execution.

## Channel Delivery Rules

- Distinguish clearly between:
  1. current-channel auto reply
  2. `sessions_send` for cross-session routing
  3. `openclaw message send` for direct provider delivery
- `sessions_send` ack alone does **not** prove Discord-visible delivery.
- For git channel and new/unstable channels, prefer **direct Discord send** when completion proof matters.
- Treat `messageId` or actual visible delivery as the primary completion proof for direct sends.
- Current notable channels:
  - `channel:1483989656470294548` → git notify, direct send preferred
  - `channel:1484724388065706054` → crypto, treat as usable but prefer visible-delivery confirmation for completion

## Backtest / Performance Reporting Rules

- For strategy research and backtest results delivered to Discord, use a **standard performance summary format** instead of ad-hoc prose.
- Trigger phrases such as `성과 요약도 부탁해`, `성과도 같이`, `정리해서 보내줘`, or similar wording in a strategy/backtest context should be treated as a request to apply the standard reporting template automatically.
- Default report package:
  1. conclusion / positioning
  2. key metrics summary
  3. strategy explanation
  4. current positions / holdings summary when available
  5. risk / caveats
  6. next action
  7. chart attachments as actual media
- Chart delivery is complete only when:
  - artifacts are staged under `~/.openclaw/media/`
  - sent with `openclaw message send --media`
  - provider delivery succeeds
- For multi-strategy reporting, do not send only one representative chart unless the user explicitly asks for a lighter version.
- Standard section order:
  1. `[성과 요약] 📊`
  2. `**전략 개요**`
  3. `**핵심 성과지표**`
  4. `**전략 설명**`
  5. `**현재 포지션 / 보유 종목 요약**`
  6. `**해석**`
  7. `**리스크 / 확인 필요**`
  8. `**첨부 차트**`
- Standard metrics when available:
  - CAGR / Vol / Sharpe / MDD / Calmar
  - Win Rate
  - Turnover
  - Rebalance frequency
  - Universe
  - Test period
  - Long/short structure
  - holdings count / top holdings summary

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Backtest Verification Rules

- Before calling a backtest/performance task `완료`, run through `quant-team/BACKTEST_VERIFICATION_CHECKLIST.md`.
- Separate clearly:
  1. result generated
  2. verification complete
  3. provider-visible delivery complete
- If charts were requested, file generation alone is not completion.
