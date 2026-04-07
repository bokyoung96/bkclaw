# 0042 — Cross-workspace drift audit and refactor plan

## Summary

이 리팩토링은 `workspace` 와 `workspace-research` 사이에서 반복적으로 충돌하거나 드리프트가 생길 수 있는 운영 규칙을 정리하기 위한 것이다.
핵심은 모든 문서를 하나로 합치는 것이 아니라,
**공통 anchor는 canonical로 올리고, lane-specific 차이는 각 workspace에 남기는 것**이다.

## Problems observed

### 1. Quant-team intake drift
- 어떤 세션/채널에서는 quant-team 문서가 이미 있어도 일반 Q&A처럼 먼저 답한 적이 있었다.
- 해결 원칙:
  - quant-team 진입은 `quant-team/QUANT_TEAM_ENTRY.md`
  - cross-workspace anchor는 `harness/GAEJAE_OPERATING_POLICY.md`

### 2. Tavily preflight drift
- Tavily는 research lane baseline인데도 새 세션/새 채널에서 preflight 없이 `안 된다`로 간 적이 있었다.
- 해결 원칙:
  - key -> runtime env -> smoke call 순서로 확인
  - 실패는 레이어별로 보고

### 3. Discord/media delivery drift
- artifact 생성만으로 전달 완료처럼 말하거나,
  attachment가 너무 많아 Discord 렌더링이 불안정했던 적이 있었다.
- 해결 원칙:
  - provider-visible delivery proof 전 완료 판정 금지
  - 다중 차트는 subplot/번들 우선

### 4. Completion proof drift
- git / Discord notify / media 전달에서 내부 ack나 부분 완료를 전체 완료처럼 말할 위험이 있었다.
- 해결 원칙:
  - local commit / push / merge / cleanup / notify proof 분리

## Refactor decisions

### Canonical (shared)
다음은 공통 anchor로 관리한다.
- shared venv 확인
- quant-team intake-first
- Tavily preflight
- Discord/media delivery proof
- git completion proof
- long-task progress visibility
- `/new`는 좋은 재적용 트리거지만 drift 0으로 단정하지 않는 규칙

### workspace local
다음은 repo/workspace 특화로 유지한다.
- git preflight 상세
- repo root / remote / branch / merge flow
- long-task helper / progress artifact 운용
- direct Discord send proof when relevant

### workspace-research local
다음은 research lane 특화로 유지한다.
- source tiering
- research summary shape
- Discord chart packaging preference
- questioning style for large research work
- reflection / evaluator / subagent policy

## File changes in this refactor

1. Added `harness/GAEJAE_OPERATING_POLICY.md`
2. Updated `CANONICAL_AGENT_RULES.md` to point to the new anchor
3. Updated `WORKING_RULES.md` to treat the anchor as common operating reference
4. Updated `TOOLS.md` to sync Tavily/Discord/backtest delivery posture with the anchor
5. This audit document added for future comparison

## Expected benefit

- `/new` 이후에도 재적용 기준점이 더 명확해진다.
- quant/backtest/research-heavy 요청에서 질문 우선 흐름이 더 안정된다.
- Tavily/Discord/media/git 관련 반복 미스가 문서상 preflight/proof gate로 고정된다.
- 공통 규칙과 lane-specific 규칙의 경계가 더 명확해진다.
