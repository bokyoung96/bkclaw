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
