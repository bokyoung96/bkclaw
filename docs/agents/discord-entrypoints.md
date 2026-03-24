# Discord Agent Entry Points

## 목표
Discord에서 현재 agent 구조를 **쉽게 부르고**, **헷갈리지 않게 보고**, **팀 오케스트레이션을 이해**할 수 있게 한다.

---

## 1. `/agents`

### 의도
운영 중인 agent inventory를 Discord에서 즉시 확인한다.

### 최소 포함 항목
- agent id
- 표시 이름
- 역할
- workspace
- 호출 패턴

### 예시 출력 형태
- `main` — 메인 coordinator
- `research` — 웹 리서치 / source scouting
- `reviewer` — 결과 검토 / 품질 점검
- `backtest` — 전략 구현 / 실험
- `performance-review` — 성과 해석 / 리스크 점검

### 운영 원칙
- inventory 문서와 내용이 어긋나면 안 된다
- 새 agent를 추가하면 `/agents` 출력도 함께 갱신한다

---

## 2. `/agent_team_orchestration`

### 의도
현재 team 구조와 escalation 경계를 Discord에서 바로 보여준다.

### 최소 포함 항목
- coordinator: `main`
- specialists: `research`, `reviewer`, `backtest`, `performance-review`
- external harness: ACP / Codex / OMX
- capability layer: Tavily / web / GitHub / browser / memory
- policy layer: skills / operating rules

### 예시 해석
- 일반 대화: `main`
- 자료 조사: `research`
- 결과 검토: `reviewer`
- 전략 실험: `backtest`
- 성과 보고: `performance-review`
- 긴 코딩/실행: ACP / Codex / OMX escalation

---

## 3. 멘션 호출면

현재 agent별 호출 패턴은 inventory 문서를 따른다.

권장 원칙:
- agent 이름과 호출 패턴을 최대한 일치시킨다
- 같은 별칭을 너무 많은 agent가 공유하지 않는다
- `가재`, `가재야` 같은 공통 호출은 coordinator로 우선 해석하는 편이 안전하다

---

## 4. 후속 작업
향후 필요 시 다음을 추가한다.
- `/agent_status`
- `/agent_inventory`
- `/agent_bindings`
- `/agent_capabilities`
