# WORKING_RULES.md

## canonical 문서 우선 원칙
공통 운영 규칙은 `CANONICAL_AGENT_RULES.md` 를 먼저 본다.
세션 재적용용 공통 anchor는 `harness/GAEJAE_OPERATING_POLICY.md` 와 `harness/DEFAULT_TASK_LOOP.md` 를 함께 본다.
이 문서는 `workspace` 고유의 작업 흐름(코드/gip/repo/운영 반영)을 보강하는 용도다.

## cross-workspace anchor 요약
- 의미 있는 작업은 `question -> assumption lock -> acceptance criteria -> verification -> delivery proof` 기본 루프를 따른다.
- 큰 작업은 `scope lock -> run -> verify -> report` 순서를 우선한다.
- quant/backtest/research-heavy 요청은 intake-first를 기본으로 본다.
- Tavily / Discord media / git completion은 preflight/proof 기준으로 다룬다.
- `/new` 는 좋은 재적용 트리거지만 drift 0을 보장한다고 단정하지 않는다.

## 폴더 우선 확인 원칙

### 1. 리서치 / 초안 / 웹 조사
먼저 보는 폴더:
- `/home/node/.openclaw/workspace-research`

용도:
- 웹 리서치
- 문서 초안
- 조사 메모
- 임시 분석

### 2. 실제 코드 / git / 운영 반영
먼저 보는 폴더:
- `/home/node/.openclaw/workspace`

용도:
- `bkclaw` 실제 git repo
- branch / commit / push / merge
- 운영 문서 반영
- 실제 코드 수정

## git preflight 원칙
git 작업 요청 시 항상 아래를 먼저 확인한다.
1. repo 루트
2. remote
3. 현재 branch
4. working tree status
5. 필요 시 env / credential 경로
6. 완료 판정은 아래를 각각 분리 확인
   - local commit
   - remote push
   - merge
   - branch cleanup
   - git channel delivery

## quant-team intake 우선 원칙
전략 만들어줘 / 전략 구현 / 백테스트 / 탐색 / 성과 요약 요청의 canonical entry는 `quant-team/QUANT_TEAM_ENTRY.md`를 따른다.
이 경우 첫 응답부터 일반 답변으로 바로 들어가지 않고, 해당 문서 기준으로 **run-policy intake → 실행 가정 intake → mandate lock → round 시작** 순서를 적용한다.
특히 첫 질문 우선순위는 아래를 먼저 본다.
1. iteration 횟수 / 반복 라운드 수
2. 한 번에 볼 전략 수
3. 중간보고 주기
4. 탈락 기준 / stop conditions
5. 필요 시 git scope / 보고 채널
그 다음 universe / 기간 / benchmark / 비용 / 리밸런싱 / 구조 / 리스크 제약을 묻는다.


## 현재 세션 우선 규칙
현재 세션의 기본 행동 원칙(톤, 역할, 기본 출력 형식)은 **현재 세션이 붙은 workspace의 문맥 파일**을 우선한다.
즉, `workspace-research` 세션이면 research 문맥이 먼저고, `workspace` 세션이면 repo/workspace 문맥이 먼저다.
다른 workspace의 같은 이름 파일은 자동 동기화된다고 가정하지 않는다. 필요 시 명시적으로 비교/확인한다.

## 공통 Python / 환경 확인 규칙
Python, 패키지, 실행환경 관련 답변에서는 먼저 **shared venv**를 확인한다.
- canonical interpreter: `/home/node/.openclaw/workspace/.venv/bin/python`
- canonical pip: `/home/node/.openclaw/workspace/.venv/bin/python -m pip`
- base/runtime Python만 보고 `python이 없다`, `pandas가 없다`, `라이브러리가 없다`고 결론내리지 않는다.
- 보고 순서는 분리한다:
  1. 현재 런타임 기본 Python
  2. shared venv
  3. 프로젝트/로컬 전용 환경
- 아직 확인 전이면 `현재 런타임에서 아직 확인되지 않았다`고 표현한다.

## 운영 일관성 하드닝 우선 원칙
중요한 누락 패턴(shared venv 미확인, quant intake 누락, git notify proof 누락)은 기억에 맡기지 않고 `OPERATING_HARDENING.md` 기준의 gate/proof 규칙으로 다룬다.
