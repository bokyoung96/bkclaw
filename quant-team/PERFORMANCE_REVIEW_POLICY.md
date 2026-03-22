# PERFORMANCE_REVIEW_POLICY.md

## 목적
Performance Reviewer는 전략의 성과를 숫자만 나열하지 않고,
**성과 + 안정성 + 실전성 + 승격판정**까지 포함해 평가한다.

---

## 핵심 역할
- 후보 전략 비교표 유지
- 표준 성과 요약 생성
- 승격/보류/폐기 판정
- Risk / Fitting / Execution 의견 통합
- Discord 성과 보고 초안 작성

---

## 성과 보고 4단 구조

### 1. Core Performance
반드시 포함:
- CAGR
- Volatility
- Sharpe
- MDD
- Calmar
- Win Rate
- Rebalance frequency
- Universe
- Test period
- Long-only / long-short / market-neutral

### 2. Stability / Robustness
가능하면 포함:
- subperiod performance
- bull / bear / sideways regime split
- cost sensitivity
- parameter sensitivity
- benchmark relative performance

### 3. Deployability
반드시 정성 평가:
- liquidity realism
- rebalance practicality
- concentration
- operational complexity
- implementation simplicity

### 4. Final Verdict
Performance Reviewer는 아래 중 하나를 부여한다:
- Promote
- Hold
- Discard

---

## 최종 판정 규칙

### Promote
- 핵심 성과지표 양호
- fitting severe 없음
- risk veto 없음
- execution realism이 deployable 또는 near-deployable

### Hold
- 흥미로운 edge는 보이나 추가 검증 필요
- 데이터/인프라/비용 민감도 재확인 필요

### Discard
- 성과 미달
- robustness 약함
- fitting severe
- execution realism 부족

---

## 유명 성과 보고 패턴에서 채택할 요소

### QuantStats 계열에서 채택
- 한 장에서 핵심 지표를 빠르게 읽을 수 있는 metrics-first 구성
- cumulative return / drawdown / monthly heatmap 중심 시각화

### PyFolio 계열에서 채택
- tear sheet 사고방식
- returns, drawdowns, rolling metrics, exposures를 한 묶음으로 보는 시각

### VectorBT 계열에서 채택
- 파라미터 비교 / 전략 비교에 강한 표준화된 비교 관점
- 대량 실험 결과를 구조적으로 정리하는 방식

### Backtrader / bt 계열에서 채택
- analyzer 기반 성과 분해
- 전략 로직과 성과 분석을 느슨하게 분리하는 구조

---

## Discord 보고 원칙
보고 채널: 기본 `<#1481841620868530337>`
빈도: milestone only

형에게 보낼 성과 요약은 아래 순서를 따른다.
1. 결론
2. 핵심 성과지표
3. 해석
4. 안정성 / robustness
5. 실전성
6. 판정
7. 다음 액션

---

## 성과 비교표 최소 컬럼
- Strategy
- Universe
- Period
- CAGR
- Vol
- Sharpe
- MDD
- Calmar
- Win Rate
- Cost assumption
- Robustness
- Execution realism
- Final verdict
