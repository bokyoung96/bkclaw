# Current Agent Inventory

_Last refreshed: 2026-03-23 UTC_

## Summary

현재 확인된 운영 agent:

1. `main`
2. `research`
3. `reviewer`
4. `backtest`
5. `performance-review`

별도로 runtime state 경로에는 `codex` 관련 세션 저장 흔적이 보인다.
이 항목은 현재 `agents.list[]`의 일반 업무 agent와는 구분해서 본다.

---

## 1. main
- **Name:** 가재
- **Role:** 메인 기본 agent
- **Workspace:** `~/.openclaw/workspace`
- **Runtime state:** `~/.openclaw/agents/main`
- **Model:** `openai-codex/gpt-5.4`
- **Mention patterns:**
  - `가재`
  - `가재야`
  - `가재 메인`
  - `메인 가재`

## 2. research
- **Name:** 가재 리서치
- **Role:** 웹 리서치 / 논문 / source scouting 전담
- **Workspace:** `~/.openclaw/workspace-research`
- **Runtime state:** `~/.openclaw/agents/research`
- **Model:** `openai-codex/gpt-5.4`
- **Mention patterns:**
  - `가재`
  - `가재야`
  - `가재 리서치`
  - `리서치 가재`
  - `리서치`

## 3. reviewer
- **Name:** 가재 리뷰어
- **Role:** 리서치/구현 결과 검토, 품질 점검
- **Workspace:** `~/.openclaw/workspace-research`
- **Runtime state:** `~/.openclaw/agents/reviewer`
- **Model:** `openai-codex/gpt-5.4`
- **Mention patterns:**
  - `가재 리뷰어`
  - `리뷰어 가재`
  - `검토 가재`
  - `검토해 가재`

## 4. backtest
- **Name:** 가재 백테스트
- **Role:** 전략 구현 / 실험 / 백테스트 전담
- **Workspace:** `~/.openclaw/workspace`
- **Runtime state:** `~/.openclaw/agents/backtest`
- **Model:** `openai-codex/gpt-5.4`
- **Mention patterns:**
  - `가재 백테스트`
  - `백테스트 가재`
  - `전략 테스트 가재`

## 5. performance-review
- **Name:** 가재 성과평가
- **Role:** 성과 해석 / 리스크 점검 / 보고 포맷 전담
- **Workspace:** `~/.openclaw/workspace`
- **Runtime state:** `~/.openclaw/agents/performance-review`
- **Model:** `openai-codex/gpt-5.4`
- **Mention patterns:**
  - `가재 성과평가`
  - `성과평가 가재`
  - `성과 가재`
  - `리포트 가재`

---

## Runtime-only note: codex
- 현재 runtime state 경로에는 `~/.openclaw/agents/codex`가 보인다.
- 하지만 현재 확인 시점의 `agents.list[]` 일반 inventory에는 포함되지 않았다.
- 따라서 이 항목은 일반 역할형 agent라기보다 **Codex 관련 세션/연동 상태 저장 흔적**으로 우선 분류한다.

---

## Refactor stance

이 inventory 리팩토링의 목적은 다음이다.

- 사람 기준으로 agent 구조를 한 번에 파악하게 만들기
- runtime storage (`~/.openclaw/agents`)를 직접 뒤지지 않도록 하기
- future binding / routing / mention pattern 변경 시 함께 갱신하기

### Do not merge blindly
다음 항목은 그대로 유지한다.
- `~/.openclaw/agents/...` runtime state
- agent별 세션 저장
- agent별 auth/model profile

즉 이 문서는 **관리 inventory**이고,
runtime state 저장소를 대체하지 않는다.
