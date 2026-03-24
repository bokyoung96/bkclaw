# Harness Architecture

## 목적
OpenClaw 운영 구조를 아래 세 층으로 나눠서 본다.

1. **agent** — 역할 단위
2. **mcp / tool capability** — 외부 상호작용 단위
3. **skills** — 절차 / 판단 규칙 단위

이 문서는 agent inventory와 orchestration 문서 사이에서,
하네스 관점의 경계를 명확히 하기 위한 canonical note다.

---

## 1. Agent layer
Agent는 **누가 어떤 종류의 일을 소유하는가**를 정의한다.

현재 core agents:
- `main`
- `research`
- `reviewer`
- `backtest`
- `performance-review`

Agent는 다음을 가진다.
- 역할
- workspace
- 호출 패턴
- runtime state
- handoff 책임

---

## 2. MCP / tool capability layer
이 층은 **무엇을 통해 바깥 세계와 상호작용하는가**를 다룬다.

예:
- web search / fetch
- browser
- memory
- GitHub / gh
- ACP
- Codex CLI
- OMX
- Tavily research capability

중요:
- capability 차이만으로 새 agent를 만들지 않는다.
- 먼저 기존 agent에 capability를 붙이는 방식으로 해결 가능한지 본다.

### Tavily position
Tavily는 기본적으로:
- `research` agent가 주로 쓰는 capability
- agent 자체가 아니라 research-lane capability
- research lane / deep research / browser escalation 사이의 앞단 source discovery 역할

---

## 3. Skills layer
Skill은 **절차와 판단 규칙**이다.

예:
- `agent-team-orchestration`
- `research-lane`
- `deep-research-lane`
- `discord-channel-actions`
- `notice-channel-formatting`

Skill의 역할:
- agent가 같은 실수를 반복하지 않게 함
- lane별 workflow를 표준화함
- tool 사용 순서 / escalation 기준 / formatting 규칙을 제공함

---

## 4. Runtime boundary
아래는 모두 같은 층이 아니다.

### current session
- 현재 대화 중인 active session

### specialist agent
- 역할형 lane

### subagent
- 임시 병렬 worker

### ACP
- 외부 agent protocol bridge

### Codex / OMX / exec
- shell / runtime execution layer

이 구분이 흐려지면,
- tool 문제를 agent 문제로 착각하거나
- runtime 문제를 persona 문제로 잘못 해석하게 된다.

---

## 5. Canonical files
이 구조의 canonical human-managed 문서는 아래에 둔다.

- `docs/agents/inventory.md`
- `docs/agents/orchestration.md`
- `docs/agents/discord-entrypoints.md`
- `docs/agents/harness-architecture.md`

반면 runtime truth는 아래에 있다.
- `~/.openclaw/agents/...`
- OpenClaw config (`agents.list[]`, bindings)

즉:
- 문서 truth = `docs/agents/`
- runtime truth = config + `~/.openclaw/agents/...`

---

## 6. Anti-duplication rule
중복을 줄이기 위한 규칙:

1. 역할/호출/구조 설명은 `docs/agents/`를 canonical로 둔다.
2. skill은 상세 구조를 복제하지 말고 canonical 문서를 참조한다.
3. runtime state 경로 설명은 inventory 쪽에만 둔다.
4. Discord 호출면 설명은 `discord-entrypoints.md`를 우선한다.
5. 하네스 계층 설명은 `harness-architecture.md`를 우선한다.
