# Strategy Basket v1

## 목적
백테스트 전략을 개별 일회성 스크립트가 아니라, 표준 spec/config와 canonical artifact를 갖는 재실행 가능한 전략 묶음으로 관리한다.

## 원칙
- 특정 전략 하나에 과몰입하지 않는다.
- 모든 전략은 표준 runner(`scripts/run_backtest.py`)로 실행 가능해야 한다.
- 전략은 `configs/backtests/*.json` spec으로 재실행 가능해야 한다.
- 결과는 `reports/backtests/<run_id>`에 canonical artifact로 남는다.
- `spy_momentum`은 현재 **example strategy** 로 유지한다.

## 현재 basket
- `quant_db_momentum_fast`
  - 상태: active
  - 용도: example / runner smoke / owner validation baseline
- `spy_sector_neutral_6m_momentum`
  - 상태: experimental
  - 용도: 별도 안정화 후 편입 검토

## 이후 추가 전략 예시
- 6M momentum
- 12M momentum
- reversal
- quality + value
- earnings revision
- volatility managed momentum

## 운영 방식
1. 전략 spec 작성
2. 표준 runner 실행
3. validation 확인
4. plots / holdings / reproduce script 확인
5. basket status 갱신(active / experimental / deprecated)
