# Agent Team Orchestration

## 목적
이 문서는 OpenClaw 운영을 **단일 에이전트 응답기**가 아니라,
**역할형 agent + tool/mcp capability + skills policy** 구조로 관리하기 위한
실무 기준을 정리한다.

---

## 1. 기본 관점

좋은 멀티에이전트 운영은 agent 수를 늘리는 것이 아니라,
아래 세 층을 분리하는 데서 시작한다.

1. **agent**
   - 누가 어떤 역할을 맡는가
2. **mcp / tool capability**
   - 무엇을 통해 외부 정보를 읽고 실행하는가
3. **skills**
   - 어떤 절차/판단 규칙으로 행동하는가

이 세 층을 섞으면 다음 문제가 생긴다.
- 역할과 도구가 뒤섞임
- agent 수만 늘고 호출 기준이 흐려짐
- 같은 일을 agent duplication으로 해결하려고 함
- runtime/tool failure를 persona 문제로 착각함

---

## 2. 권장 구조: `agent / mcp / skills`

### A. Agent layer
Agent는 **역할 분리 단위**다.

현재 기준 core agents:
- `main`
- `research`
- `reviewer`
- `backtest`
- `performance-review`

Agent는 다음 질문에 답해야 한다.
- 이 agent의 주 역할은 무엇인가?
- 어떤 workspace를 기본으로 쓰는가?
- 언제 직접 답하고, 언제 다른 worker로 escalation 하는가?
- 어떤 채널/호출 패턴으로 불리는가?

### B. MCP / tool capability layer
MCP/tool은 **외부 세계와 상호작용하는 capability layer**다.

예:
- web search / fetch
- Tavily 계열 research capability
- GitHub / gh
- browser
- ACP bridge
- Codex / OMX / shell runtime

중요:
- 도구가 다르다고 agent를 늘릴 필요는 없다.
- 먼저 **capability 분리**로 해결 가능한지 본다.
- Agent 추가는 역할 차이가 명확할 때만 한다.

### C. Skills layer
Skills는 **행동 규칙 / 절차 / 판단 기준**이다.

예:
- research lane workflow
- quant-team intake lock
- discord formatting
- healthcheck / github / weather / coding-agent

Skill은 “누가 하느냐”보다
“어떻게 하느냐”를 표준화하는 층이다.

---

## 3. 역할 계층

### 3.1 Coordinator
- 기본 coordinator는 `main`
- 사용자의 입력을 받고
- specialist agent 호출이 필요한지 판단한다
- orchestration ownership을 가진다
- 결과를 다시 사용자 관점으로 합친다

### 3.2 Specialists
- `research`: 웹 리서치 / 자료 탐색
- `reviewer`: 검토 / 품질 점검
- `backtest`: 전략 구현 / 실험 / 백테스트
- `performance-review`: 성과 해석 / 리스크 / 보고

### 3.3 External harness / runtime
- ACP
- Codex CLI
- OMX
- shell / exec runtime

이들은 specialist agent 자체가 아니라,
**specialist가 필요 시 활용하는 실행 하네스**다.

### 3.4 Ephemeral workers
- subagent
- one-shot isolated runs

짧은 병렬 작업이나 분리 검토에 사용한다.

---

## 4. Tavily의 위치

Tavily research는 기본적으로 **agent가 아니라 capability**다.

즉 Tavily는 다음처럼 분류하는 것이 맞다.
- **role owner:** `research`
- **layer:** MCP / tool capability
- **usage policy:** research lane skill / operating rule에 따름

정리하면:
- Tavily는 `research` agent가 자주 쓰는 대표 capability
- Tavily가 있다고 해서 별도 “Tavily agent”를 꼭 만들 필요는 없음
- 먼저 `research + Tavily capability + research skill` 조합으로 해결하는 것이 바람직함

단, 아래 경우에는 별도 lane을 검토할 수 있다.
- 아주 긴 조사 파이프라인
- 지속적인 source triage 전용 thread
- 고비용/고빈도 web research를 별도 세션으로 격리하고 싶을 때

그 전에는 Tavily를 **tool/MCP layer**로 유지하는 편이 더 단단하다.

---

## 5. Discord 운영면

형이 원하는 Discord 사용성은 아래 두 개를 중심으로 본다.

### 5.1 `/agents`
목적:
- 현재 agent 목록 표시
- 각 agent의 역할 / 호출 패턴 / workspace 표시
- operator가 빠르게 어떤 lane가 있는지 확인

권장 출력:
- agent id
- 표시 이름
- 역할
- workspace
- 주요 호출 패턴
- 필요 시 현재 binding 요약

### 5.2 `/agent_team_orchestration`
목적:
- coordinator / specialists / harness 경계 설명
- 언제 어떤 agent를 쓰는지 빠르게 안내
- escalation 기준을 보여주기

권장 출력:
- coordinator
- specialist lanes
- external harness
- example routing rules
- 현재 권장 flow

---

## 6. Agent 추가 기준

새 agent는 아래 조건을 만족할 때만 추가한다.

1. 역할이 기존 agent와 명확히 다르다
2. workspace 또는 운영 규칙이 실질적으로 다르다
3. 단순 tool 차이가 아니라 판단/보고 구조가 다르다
4. Discord 호출면에서 사용자가 실제로 구분해서 부를 가치가 있다

추가하지 않아야 하는 경우:
- 단지 특정 도구(Tavily, browser, gh)를 많이 쓴다는 이유만으로
- 같은 역할을 이름만 바꿔 다시 만드는 경우
- skill로 해결 가능한 절차 차이를 agent로 승격하는 경우

---

## 7. 현재 권장 체계

### Keep
- `main`
- `research`
- `reviewer`
- `backtest`
- `performance-review`

### Treat as harness / runtime
- ACP
- Codex CLI
- OMX
- exec / shell runtime

### Treat as capability layer
- web search/fetch
- Tavily research capability
- GitHub / gh
- browser
- memory

### Treat as policy / workflow layer
- skills
- workspace operating rules
- channel formatting rules
- quant-team intake rules

---

## 8. Hardening 방향

OpenClaw에서 구조를 단단하게 가져가려면,
agent를 늘리는 것보다 아래를 우선한다.

1. agent inventory 최신화
2. Discord 호출면 표준화
3. orchestration 문서화
4. doctor / status / binding 점검 루틴 정착
5. harness boundary 문서화
6. capability와 role을 분리해서 설계

---

## 9. One-line stance

> Agent는 역할, MCP/tool은 capability, skill은 절차다.
> 이 셋을 분리할수록 멀티에이전트 구조는 강해진다.


## 9. Responsibility rule

> Agent decides, skill executes the method.

정확히는:
- coordinator agent(`main`)가 routing / escalation / ownership을 결정한다.
- skill은 그 결정을 더 일관되게 수행하게 만드는 방법론이다.
- tool/capability는 그 결정을 실제로 집행하는 수단이다.
