# src/backtest

## 역할
이 디렉터리는 bkclaw의 **백테스트 운영 래퍼 / 호환 계층**이다.

현재 역할:
- bkclaw 입력 스펙(`BacktestSpec`) 유지
- 기존 호출 경로(`scripts/run_backtest.py`) 유지
- owner checklist 생성
- 결과물 표준화/패키징
- 운영 검증(`src/validation/backtest_validation.py`)과 연결

## 비목표
이 디렉터리를 **장기적인 백테스트 코어 엔진의 주 개발 장소**로 키우지 않는다.

특히 아래 영역에서 `external/1w1a/backtesting` 과 중복 구현을 늘리지 않는다.
- engine core
- strategy abstraction / registry
- execution cost / fill / schedule core
- reporting core
- validation core (signal/session/split 성격)

## 현재 권장 원칙
- 코어 엔진/전략/리포팅 발전은 우선 `external/1w1a/backtesting` 에서 검토한다.
- 이 디렉터리는 bkclaw 문맥에 필요한 wrapper / compatibility / delivery proof 역할에 집중한다.
- 새 중복이 생기면 `1w1a 우선, bkclaw bridge 후행` 원칙으로 정리한다.

## migration 방향
장기적으로는 아래 형태를 목표로 한다.

1. bkclaw `BacktestSpec` 입력 유지
2. 내부 adapter가 `1w1a.backtesting.run.RunConfig` 로 변환
3. 1w1a 엔진 실행
4. bkclaw 검증 / checklist / packet 생성

즉 `src/backtest` 는 엔진 자체보다 **orchestration boundary** 로 축소하는 방향이 맞다.

## 주의
현재는 내부 참조가 남아 있으므로 즉시 삭제하지 않는다.
실제 삭제/축소 전에는 아래를 확인한다.
- 호출자 호환성
- 동일 전략 재현 가능성
- 산출물 경로 호환성
- Discord/reporting 전달 경로 유지
