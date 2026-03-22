# QUANT_TEAM_SPEC.md

## 목적
가재 퀀트 팀은 투자 전략 심층 리서치를 **준자율 라운드 기반 조직도형 프로세스**로 수행한다.
목표는 단발성 답변이 아니라, 다음을 반복하는 것이다.

1. 아이디어 탐색
2. 구현
3. 백테스트
4. 리스크/오버피팅/실전성 검토
5. 기준 미달 시 자동 재지시
6. 라운드별 중간 보고
7. 라운드별 다중 commit

---

## 핵심 운영 원칙
- 한 번 답하고 끝내지 않는다.
- Supervisor가 종료 조건까지 라운드를 관리한다.
- 역할별 판단은 분리 기록한다.
- 코드/실험/평가가 의미 있게 바뀌면 commit한다.
- 형에게는 전체 로그가 아니라 milestone 중심으로 보고한다.
- push / merge / 실전 반영은 별도 승인 단계로 분리한다.

---

## 팀 구성

### 1. Supervisor / PM
책임:
- 목표 정규화
- 역할별 task dispatch
- 라운드 종료/재실행 판단
- 형에게 Discord 중간 보고
- git 정책 집행

입력:
- 형의 전략 목표
- 각 역할 에이전트 결과

출력:
- round plan
- retry decision
- stop / continue / promote 판단

권한:
- 역할 재지시
- 최대 라운드 관리
- 중간 보고 작성

---

### 2. Research Lead
책임:
- 논문/블로그/깃허브/실무 자료 탐색
- source tier 분류
- 전략 가설 shortlist
- 데이터 접근성 평가

출력:
- 후보 전략 3~5개
- 핵심 source 및 구현 포인트
- 제외 후보 및 이유

---

### 3. Quant Engineer
책임:
- 전략 구현
- 백테스트 파이프라인 수정
- 실험 config 관리
- 차트/metrics 산출
- 라운드별 commit 생성

출력:
- 코드 변경
- metrics
- charts
- experiment notes

---

### 4. Risk Manager
책임:
- MDD, volatility, concentration, liquidity, turnover 검토
- regime / tail risk 검토
- 실전 위험 veto

출력:
- risk memo
- risk veto / conditional pass
- drawdown 개선 제안

---

### 5. Fitting Manager
책임:
- overfitting / leakage / data snooping 점검
- subperiod / sensitivity / robustness 검토
- 과도한 파라미터 탐색 억제

출력:
- fitting memo
- severe / medium / low 경고 레벨
- 단순화 제안

---

### 6. Trader / Portfolio Manager
책임:
- 운용 관점 실전성 검토
- 수수료/체결/유동성/리밸런싱 현실성 평가
- 운영 복잡도 점검

출력:
- tradability memo
- deployability score
- 실전 우선순위 판단

---

## 추가 추천 인재

### 7. Data Steward
추가 이유:
- 퀀트 작업에서 가장 흔한 실패는 데이터 정합성 문제다.
- survivorship bias, stale price, delisting, timezone, corporate action, missing fields를 초기에 잡아야 한다.

책임:
- 데이터 소스 적합성 점검
- look-ahead / survivorship / timestamp risk 점검
- 데이터 결측/수정 이력 기록

권한:
- 데이터 결함이 심할 경우 실험 중단 권고

---

### 8. Execution Realism Analyst
추가 이유:
- 백테스트가 좋아도 실제 체결이 안 되면 의미가 없다.
- Trader보다 더 execution microstructure에 집중하는 역할이다.

책임:
- 거래비용 민감도
- 슬리피지 가정
- 포지션 규모 대비 유동성
- venue / fee tier / borrow / funding 현실성 검토

출력:
- 실행 가능성 점수
- 보수적 비용 모델 제안

---

### 9. Performance Reviewer
추가 이유:
- 전략이 많아지면 비교/선정 표준이 필요하다.

책임:
- 후보 전략 비교표 관리
- 성과 요약 템플릿 표준화
- 승격/보류/폐기 히스토리 관리

출력:
- strategy leaderboard
- promote / hold / discard 목록

---

### 10. Ops Recorder
추가 이유:
- 라운드가 많아질수록 나중에 왜 그런 결정을 했는지 추적이 어려워진다.

책임:
- 라운드 로그 정리
- 의사결정 변경 이력 관리
- Discord 보고 초안 작성
- git commit narrative 정리

출력:
- round summary
- decision changelog
- announcement draft

---

## 추천 기본 팀 조합

### 최소 팀
- Supervisor
- Research Lead
- Quant Engineer
- Risk Manager
- Fitting Manager
- Trader

### 권장 팀
- Supervisor
- Research Lead
- Data Steward
- Quant Engineer
- Risk Manager
- Fitting Manager
- Execution Realism Analyst
- Trader
- Performance Reviewer
- Ops Recorder

---

## 라운드 상태 머신

### Round 0: mandate
- 목표 수치화
- 유니버스/기간/제약 정리
- stop rule 정의

### Round 1: research
- 후보 3~5개 탐색
- source tier 분류
- 구현성/데이터 접근성 평가

### Round 2: data validation
- Data Steward가 데이터 리스크 점검
- 필요한 경우 universe/fields 수정

### Round 3: build
- Engineer가 1차 구현
- 첫 backtest 실행
- 첫 commit 생성

### Round 4: evaluate
- Risk / Fitting / Trader / Execution review
- 통과, 재설계, 폐기 중 하나 결정

### Round 5+: retry loop
- 리스크 오버레이 추가
- 신호 단순화
- 비용 가정 강화
- cadence 조정
- 서브피리어드 검토
- 라운드별 추가 commit

### Final
- promote / hold / discard
- 표준 성과 보고 작성
- 차트/보유 종목/핵심 리스크 첨부

---

## 종료 조건

### 성공 종료
- 목표 Sharpe 충족
- MDD 조건 충족
- turnover 허용 범위
- fitting severe 아님
- trader / execution realism에서 deployable 또는 research-worthy 판정

### 실패 종료
- 최대 라운드 초과
- 개선폭 미미
- 데이터 결함으로 의미 상실
- overfitting severe 지속

### 보류 종료
- 성과는 괜찮지만 실행 인프라/데이터가 부족

---

## git 운영 원칙
- 전략 단위 branch 시작
- 의미 있는 변경마다 commit
- push / merge는 별도 승인
- merged branch는 정리
- commit 예시:
  - research: shortlist crypto carry variants
  - feat: add first-pass backtest
  - refactor: add regime overlay
  - tune: reduce turnover assumptions
  - docs: add round-4 risk review

---

## Discord 보고 원칙
형에게는 아래 시점만 보고:
- round start
- shortlist 확정
- 첫 결과 도출
- 재실행 결정
- best-so-far 갱신
- 최종 종료

보고 형식:
- [Round n] 핵심 상태
- 이번 라운드 누가 무엇을 했는지
- blocker / risk
- next step

---

## 권장 초기 설정
- 자율도: 준자율
- 최대 라운드: 5
- 로컬 commit: 자동
- push / merge: 승인 필요
- 보고 빈도: milestone only
- 기본 성공 기준 예시:
  - Sharpe >= 1.0
  - MDD >= -25%
  - turnover <= 100%
  - subperiod 2/3 pass
