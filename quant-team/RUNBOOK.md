# RUNBOOK.md

## 첫 실행 절차

### 1. 목표 정의
Supervisor가 아래를 고정한다.
- strategy theme
- universe
- backtest period
- success criteria
- max rounds
- cost assumptions
- forbidden moves

### 2. Round 1
- Research Lead: 후보 3~5개 제안
- Data Steward: 데이터 적합성 점검
- Supervisor: 1~2개 채택

### 3. Round 2
- Quant Engineer: 첫 구현 + fast backtest
- commit 1 생성
- Ops Recorder: round summary 기록

### 4. Round 3
- Risk Manager: 위험 평가
- Fitting Manager: overfitting 평가
- Execution Realism Analyst: 실행 가능성 평가
- Trader: 운용 가능성 판단
- Supervisor: continue / retry / stop 판단

### 5. Retry loop
기준 미달 시 아래 중 하나만 선택해서 수정:
- signal simplification
- risk overlay
- rebalance change
- fee assumptions 강화
- universe refinement
- parameter reduction

### 6. git discipline
- 각 라운드의 의미 있는 코드/문서 변화는 commit
- push / merge는 승인 전까지 보류

### 7. Discord reporting discipline
형에게는 다음만 보고:
- shortlist 확정
- 첫 result
- major failure / veto
- new best result
- final status

## 추천 첫 파일 구조
- quant-team/QUANT_TEAM_SPEC.md
- quant-team/ROLE_PROMPTS.md
- quant-team/RUNBOOK.md
- quant-team/rounds/
  - round-01.md
  - round-02.md
  - ...

## 추천 첫 pilot
주제: crypto carry / momentum / revision-like equities one each 비교
최대 라운드: 3
보고 빈도: round end only
commit 정책: local only
