# Agent Inventory

이 디렉터리는 **사람이 관리하는 canonical agent inventory** 용도다.

## 목적
- 현재 운영 중인 agent 목록을 한 곳에서 보기
- 각 agent의 역할 / workspace / 호출 패턴 / runtime state 경로를 빠르게 확인
- `~/.openclaw/agents` 런타임 저장소를 직접 뒤지지 않고도 구조를 이해하기

## 중요한 구분

### 1. Runtime state (유지)
OpenClaw의 실제 세션/인증/상태 저장소는 아래를 canonical runtime location으로 유지한다.

- `~/.openclaw/agents/<agentId>/agent`
- `~/.openclaw/agents/<agentId>/sessions`

이 경로는 OpenClaw 런타임이 직접 사용하는 저장소이므로,
이 inventory 리팩토링은 **이를 대체하지 않는다**.

### 2. Human-managed inventory (여기)
이 디렉터리는 사람이 보기 좋은 정리본이다.

- 어떤 agent가 있는지
- 각 agent가 무슨 역할인지
- 어느 workspace를 쓰는지
- 어떤 호출 패턴이 있는지
- runtime state가 어디에 저장되는지

## 파일 구성
- `inventory.md`: 현재 agent 전체 목록 요약
- 필요하면 이후 agent별 상세 문서 추가
  - `main.md`
  - `research.md`
  - `reviewer.md`
  - `backtest.md`
  - `performance-review.md`

## 운영 원칙
1. 새 agent를 추가/수정하면 이 inventory도 같이 갱신한다.
2. runtime state 경로 변경 제안은 inventory 정리와 분리해서 검토한다.
3. inventory는 설명/운영 문서이고, 실제 truth는 아래 두 축을 같이 본다.
   - OpenClaw config (`agents.list[]`, bindings)
   - runtime state (`~/.openclaw/agents/...`)
