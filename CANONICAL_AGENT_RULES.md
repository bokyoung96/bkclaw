# CANONICAL_AGENT_RULES.md

## Purpose

이 문서는 `workspace` 와 `workspace-research` 양쪽에 공통으로 유지해야 하는 **canonical 운영 규칙**을 모아둔 단일 기준 문서다.
중요한 공통 규칙은 이 문서를 먼저 갱신하고, 각 workspace 문서는 자신의 역할에 맞는 차이만 덧붙인다.

## Scope Split

- `workspace`
  - 실제 코드 / git repo / 운영 반영 / compose / PR / merge
- `workspace-research`
  - 웹 리서치 / 자료 정리 / source shortlisting / 임시 분석 / 전략 탐색 보고

## Session Priority Rule

현재 세션의 기본 행동 원칙(톤, 역할, 기본 출력 형식)은 **현재 세션이 붙은 workspace의 문맥 파일**을 우선한다.
즉:
- `workspace` 세션이면 repo/workspace 문맥 우선
- `workspace-research` 세션이면 research 문맥 우선

같은 이름의 파일이 양쪽에 있어도 자동 동기화된다고 가정하지 않는다.
중요한 규칙은 명시적으로 비교/반영한다.

## Startup Canonical Rule

새 세션(`/new`, `/reset`, 런타임 재시작 포함)에서는 아래 원칙을 우선 적용한다.

1. 핵심 정체성/사용자/공통 규칙 문서를 기준으로 톤과 역할을 고정한다.
2. 내부 절차, 파일, 도구, 초기화 여부를 사용자에게 설명하지 않는다.
3. 시작 응답은 짧은 인사 + 역할 반영 + 질문형 마무리로 끝낸다.
4. 불필요한 상태 문구는 사용자가 요구하지 않는 한 말하지 않는다.
5. 기본 답변은 한국어, 핵심부터, 구조적으로 한다.
6. 과장된 친밀감보다 담백하고 근거 우선의 톤을 유지한다.

## Shared Python / Environment Rule

Python, 패키지, 실행환경 관련 답변에서는 먼저 **shared venv**를 확인한다.

- canonical interpreter: `/home/node/.openclaw/workspace/.venv/bin/python`
- canonical pip: `/home/node/.openclaw/workspace/.venv/bin/python -m pip`

주의:
- base/runtime Python만 보고 `python이 없다`, `pandas가 없다`, `라이브러리가 없다`고 결론내리지 않는다.
- 보고는 아래 레이어를 분리한다.
  1. 현재 런타임 기본 Python
  2. shared venv
  3. 프로젝트/로컬 전용 환경
- 아직 확인 전이면 `현재 런타임에서 아직 확인되지 않았다`고 표현한다.

## Quant-Team Canonical Entry Rule

전략 / 백테스트 / 성과 / 탐색 요청은 `quant-team/QUANT_TEAM_ENTRY.md`를 canonical entry로 본다.
첫 응답에서 바로 전략 아이디어나 feasibility 설명으로 들어가지 않는다.

기본 순서:
1. run-policy intake
   - iteration / rounds
   - strategies per round
   - reporting cadence
   - stop conditions
   - git/reporting scope when relevant
2. execution assumptions
   - universe
   - test period
   - benchmark
   - transaction cost / slippage
   - rebalance cadence
   - structure
   - risk constraints
3. mandate lock
4. round start

## Delivery / Completion Proof Rule

특히 Discord / git / media 전달에서는 내부 ack만으로 완료 판정하지 않는다.
완료 판정은 실제 provider-visible delivery 또는 그에 준하는 명시적 성공 신호를 우선한다.

## Drift Prevention Rule

- 공통 규칙은 이 문서를 먼저 갱신한다.
- 각 workspace의 `AGENTS.md`, `TOOLS.md`, `BOOTSTRAP.md`, `WORKING_RULES.md` 등에는 공통 규칙 전체를 복붙하지 말고, 역할별 차이만 둔다.
- 드리프트 고위험 항목은 정기적으로 비교한다:
  1. shared venv 확인 규칙
  2. quant-team intake 순서
  3. 전달 완료 판정 규칙
  4. startup 톤/형식 규칙
