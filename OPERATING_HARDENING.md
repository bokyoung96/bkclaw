# OPERATING_HARDENING.md

## Goal

가재의 운영 일관성 부족을 **기억력 보강**이 아니라 **절차 강제화**로 줄인다.
핵심 목표는 다음과 같다.

1. 중요한 단계를 기억에 덜 의존하기
2. 중요한 작업은 gate / checklist / proof 기반으로 끝내기
3. 완료와 부분 완료를 엄격히 구분하기

## Core Posture

기억에 기대지 않는다.
중요한 규칙은 아래 순서로 강제한다.

1. canonical 문서
2. 작업별 gate
3. 체크리스트 / 상태 파일
4. 스크립트 / 자동화
5. 최종 보고 문구 제한

## Hard Gates

### 1) Python / Environment Gate
다음 확인 없이 `python이 없다`, `라이브러리가 없다`고 말하지 않는다.

- 현재 런타임 기본 Python
- shared venv (`/home/node/.openclaw/workspace/.venv/bin/python`)
- 필요 시 프로젝트/로컬 전용 환경

shared venv 확인 전 허용되는 표현:
- `현재 런타임에서 아직 확인되지 않았다`

금지되는 표현:
- `python이 없다`
- `pandas가 없다`
- `라이브러리가 없다`

### 2) Quant-Team Intake Gate
전략 / 백테스트 / 성과 / 탐색 요청에서는 바로 전략 제안으로 들어가지 않는다.
최소한 아래를 먼저 잠근다.

- iteration / rounds
- strategies per round
- reporting cadence
- stop conditions
- 필요 시 git/reporting scope

그 다음 execution assumptions:
- universe
- test period
- benchmark
- transaction cost / slippage
- rebalance cadence
- structure
- risk constraints

큰 작업에서는 가능하면 최소 한 번은 질문 턴을 거친다.
가정이 비어 있으면 바로 구현/추천/결론으로 점프하지 않는다.

### 3) Tavily / Media Preflight Gate
반복 장애가 있었던 Tavily / Discord media / provider delivery 문맥은 아래를 먼저 확인한다.

- Tavily
  - key 존재
  - active runtime env 노출
  - smoke call 성공
- media / delivery
  - artifact 생성
  - staging path 적합성
  - provider-visible send success 또는 동급 proof

preflight 전 `없다`, `안 된다`, `보냈다`, `완료` 같은 단정은 금지한다.

### 4) Git Completion Gate
다음 항목이 분리 확인되기 전에는 `완료`라고 말하지 않는다.

- local commit
- remote push
- merge
- branch cleanup
- git notify proof (`messageId` 또는 동등한 provider-visible proof)

허용 표현 예시:
- `로컬 커밋 완료, 원격 push 미확인`
- `merge 완료, git 채널 전달 미확인`

## Proof-First Reporting Rule

중요 작업의 완료는 **행위 자체**보다 **검증 가능한 증거**로 판단한다.
예:
- git: commit hash / push success / merge commit / branch deletion / messageId
- media: provider-visible attachment success
- env: 실제 interpreter / pip 결과

## Checklist / Artifact Rule

반복 작업은 가능한 한 파일 기반 흔적을 남긴다.
예:
- git 완료 체크리스트
- quant intake 체크리스트
- python env 확인 결과

세션이 바뀌어도 판단 근거가 남아 있어야 한다.

## Completion Language Rule

- 모든 단계가 확인되기 전에는 `완료`, `다 끝났다`, `보냈다`를 쓰지 않는다.
- 부분 완료는 부분 완료로 분리 보고한다.
- 불확실하면 `미확인`이라고 명시한다.

## Preferred Next Automation

우선 자동화 대상은 아래 순서다.
1. git finish + notify gate
2. python/shared-venv check helper
3. quant intake template/checker
4. Tavily/media preflight checker

## Concrete Helpers

- check_shared_python
  - base Python / shared venv / package visibility를 분리 확인한다.
- git_finish_and_notify
  - push -> main merge -> push -> git notify -> branch cleanup 흐름을 묶는다.
- quant-team/INTAKE_GATE_CHECKLIST.md
  - run-policy first gate를 체크리스트로 고정한다.

