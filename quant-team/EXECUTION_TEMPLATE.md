# EXECUTION_TEMPLATE.md

## 목적
이 문서는 가재 퀀트 팀 v1을 실제로 실행할 때 사용하는 표준 템플릿이다.
목표 입력, 라운드 진행, 역할 호출 순서, stop/retry 규칙, Discord 보고, git commit 규칙을 고정한다.

---

## 1. 실행 입력 포맷
Supervisor는 시작 시 아래 입력을 채운다.

```yaml
strategy_theme: <예: crypto carry / equity revision / cross-sectional momentum>
universe: <예: SPY-US / top liquid perps / KRX large cap>
period:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
success_criteria:
  sharpe_min: 1.0
  mdd_min: -0.25
  turnover_max: 1.00
  subperiod_pass: 2/3
acceptance:
  required_metrics: [CAGR, Volatility, Sharpe, MDD]
  required_robustness_checks: [subperiod, cost_sensitivity]
  verdict_required: true
delivery:
  channel: <channel id or session>
  format: summary|summary+charts
  charts_visible_in_chat: true
  completion_proof: message_id_or_equivalent
constraints:
  - no excessive parameter sweep
  - conservative transaction cost assumptions
  - avoid implementation complexity beyond stated scope
max_rounds: 5
reporting:
  discord_updates: true
  report_frequency: milestone_only
  report_channel: <channel id or session>
git:
  branch: <branch-name>
  auto_local_commit: true
  auto_push: false
  auto_merge: false
```

---

## 2. 라운드별 호출 순서

### Round 0 — mandate lock
1. Supervisor
   - 목표 수치화
   - 금지사항/종료조건 정의
   - 역할 할당 결정
2. Ops Recorder
   - mandate 요약 작성
   - acceptance criteria / verification plan / delivery proof expectation 기록

### Round 1 — idea discovery
1. Research Lead
2. Data Steward
3. Supervisor
4. Ops Recorder

출력:
- shortlist
- 제외 후보
- 초기 데이터 리스크

### Round 2 — first build
1. Quant Engineer
2. Ops Recorder
3. Supervisor

출력:
- 첫 구현
- first-pass backtest
- 첫 commit

### Round 3 — first evaluation
1. Risk Manager
2. Fitting Manager
3. Execution Realism Analyst
4. Trader
5. Supervisor
6. Ops Recorder

출력:
- risk memo
- fitting memo
- execution memo
- trader verdict
- retry or stop

### Round 4+ — retry loop
retry가 결정되면 아래 중 필요한 역할만 재호출:
- Research Lead
- Quant Engineer
- Risk Manager
- Fitting Manager
- Execution Realism Analyst
- Trader
- Ops Recorder

---

## 3. Retry 규칙
Supervisor는 한 라운드에 한 번에 너무 많은 변경을 넣지 않는다.
기본적으로 retry에서는 아래 중 1~2개만 바꾼다.

가능한 retry 조치:
- signal simplification
- risk overlay addition
- rebalance cadence adjustment
- cost assumption tightening
- universe refinement
- parameter reduction
- sector-neutral variant
- regime filter addition

금지:
- 근거 없는 대규모 파라미터 스윕
- 1라운드에 4개 이상 변화
- fitting 경고 무시한 채 성과만 추구

---

## 4. 역할별 표준 출력 포맷

### Research Lead
- 후보 전략
- 핵심 근거
- source tier
- 데이터 요구사항
- 구현 난이도
- 제외 후보

### Data Steward
- 데이터 소스
- 편향 가능성
- 결측/정합성 리스크
- 실험 가능/보류 판단

### Quant Engineer
- 구현 내용
- 변경 파일
- 실행 실험
- 결과 요약
- 다음 수정 포인트
- commit 필요 여부

### Risk Manager
- MDD
- volatility
- concentration
- turnover
- liquidity
- regime risk
- verdict: veto / conditional pass / pass

### Fitting Manager
- sensitivity
- robustness
- leakage suspicion
- complexity penalty
- verdict: severe / medium / low

### Execution Realism Analyst
- fee/slippage realism
- liquidity realism
- venue dependency
- rebalance practicality
- deployability score

### Trader
- 운용 관점 평가
- live simplification 가능성
- promote / hold / discard

### Ops Recorder
- round summary
- decision log
- commit summary
- Discord update draft

---

## 5. Stop / Continue / Retry 규칙

### Continue
- 아직 필수 검토가 남아 있음
- 다음 검토 라운드가 필요함

### Retry
- 성과 미달이나 리스크 미달이지만 개선 여지가 명확함
- 다음 수정 포인트가 명시적임

### Stop-Success
- success criteria 충족
- severe fitting 경고 없음
- trader / execution realism에서 연구 가치 이상 판정

### Stop-Fail
- 최대 라운드 초과
- 2회 연속 개선 미미
- severe fitting 지속
- 데이터 결함 심각
- risk veto 지속

### Hold
- 성과는 보이나 지금은 인프라/데이터 부족
- 후속 과제로 보류

---

## 6. git commit 규칙

### commit 생성 조건
다음 중 하나면 commit 생성 가능:
- 전략 로직 변경
- 실험 설계 변경
- 리스크 오버레이 추가
- 보고/평가 문서화 가치가 큼

### commit 예시
- research: shortlist top 3 strategy candidates
- feat: add first-pass carry backtest
- refactor: add regime overlay for drawdown control
- tune: reduce turnover with monthly gate
- docs: add round-3 fitting review

### commit 금지
- 무의미한 로그 차이
- 중복 실행
- 설명 불가능한 수치 변화만 있을 때

---

## 7. Discord 보고 템플릿

### round start
[Round {n}] 시작
- 목표: ...
- 이번 라운드 담당: ...
- 확인할 포인트: ...

### retry decision
[Round {n}] 재실행 결정
- 미달 항목: ...
- 주요 이유: ...
- 다음 수정 포인트: ...

### best-so-far
[Round {n}] 최고 성과 갱신
- 전략: ...
- 주요 지표: ...
- 남은 검증: ...

### final
[최종] 종료
- 결과: promote / hold / discard
- 핵심 지표: ...
- 핵심 리스크: ...
- 다음 액션: ...

---

## 8. 추천 첫 pilot

### Pilot A
- theme: crypto carry vs momentum
- rounds: 3
- report: round end only
- git: local commit only

### Pilot B
- theme: equity revision with regime overlay
- rounds: 3~5
- report: milestone only
- git: local commit automatic, push manual
