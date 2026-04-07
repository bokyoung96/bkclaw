# 2026-04-07 1w1a vs bkclaw backtest gap analysis

## 1. 결론

현재 기준에서 **중복 위험의 중심은 `백테스트 코어` 자체를 두 군데에서 동시에 키우는 것**이다.

따라서 권장 방향은 아래와 같다.

- `external/1w1a/backtesting` → **코어 엔진 / 전략 / 리포팅 / validation의 우선 후보**
- `src/backtest` → **bkclaw 운영 래퍼 / delivery proof / owner checklist / 기존 호출 호환 계층**

즉, 지금 바로 `src/backtest` 전체 삭제는 비추천이다.
대신 **`src/backtest`를 코어 엔진이 아니라 orchestration boundary로 축소**하는 리팩토링이 맞다.

---

## 2. 비교 대상

### A. bkclaw 현재 계층
- `src/backtest/runner.py`
- `src/backtest/models.py`
- `src/backtest/output_standardizer.py`
- `src/backtest/strategy_registry.py`
- `src/backtest/strategies/*.py`
- `src/validation/backtest_validation.py`
- `scripts/run_backtest.py`

### B. 1w1a 현재 계층
- `external/1w1a/backtesting/run.py`
- `external/1w1a/backtesting/engine/*`
- `external/1w1a/backtesting/data/*`
- `external/1w1a/backtesting/execution/*`
- `external/1w1a/backtesting/strategies/*`
- `external/1w1a/backtesting/reporting/*`
- `external/1w1a/backtesting/validation/*`
- `external/1w1a/tests/*`

---

## 3. 기능 비교 요약

| 영역 | bkclaw `src/backtest` | `1w1a/backtesting` | 판단 |
|---|---|---|---|
| 실행 진입 | `scripts/run_backtest.py` + `runner.py` | `backtesting/run.py` | 둘 다 있음, 1w1a가 더 두꺼움 |
| spec/config | `BacktestSpec` | `RunConfig` | 둘 다 있음 |
| 엔진 | legacy script wrapper 중심 | 자체 엔진(`engine/core.py`) | **1w1a 우세** |
| 전략 registry | 소수 전략 alias 중심 | strategy registry + base strat 계층 | **1w1a 우세** |
| 비용/체결/스케줄 | 얇음, legacy 의존 | `execution/costs.py`, `fill.py`, `schedule.py` | **1w1a 우세** |
| 데이터 로딩 | 간접/legacy 중심 | `catalog`, `data.loader`, `store`, `ingest` | **1w1a 우세** |
| reporting | artifact 표준화 중심 | report builder / tables / figures / html / pdf | **1w1a 우세** |
| validation | 결과 패키지 검증 강함 | signal/session/split validation | 상호 보완 |
| owner checklist | 있음 | 없음(현재 기준) | **bkclaw 우세** |
| delivery proof | Discord/reporting 문맥과 연결 쉬움 | 별도 운영 proof는 없음 | **bkclaw 우세** |
| 테스트 | 일부 unit test | 광범위한 tests | **1w1a 우세** |

---

## 4. 핵심 판단

### 4.1 1w1a가 더 강한 영역
1. 순수 백테스트 엔진
2. 전략 abstraction
3. 데이터 계층
4. 리포팅 계층
5. 테스트 밀도

### 4.2 bkclaw가 더 강한 영역
1. 현재 운영 호출 호환성
2. owner checklist
3. 결과물 전달/검증 문맥
4. 기존 repo 문맥과의 연결
5. backtest package validation의 운영 체크 성격

### 4.3 가장 위험한 중복
가장 위험한 중복은 아래다.

- 엔진 로직을 `src/backtest` 와 `1w1a/backtesting` 에서 동시에 발전시키는 것
- 전략 registry를 두 군데에서 별도로 키우는 것
- 리포팅 산출 규격을 둘 다에서 별도로 갖는 것

이 중복은 시간이 갈수록 아래 문제를 만든다.
- 결과 불일치
- 테스트 중복
- 유지보수 비용 증가
- 사용자/운영자 혼란

---

## 5. 현재 실제 사용 흔적

`src/backtest` 계층은 현재 bkclaw 내부에서 참조가 남아 있다.
예:
- `scripts/run_backtest.py`
- `scripts/generate_backtest_packet.py`
- `src/reporting/backtest_packet.py`
- `src/reporting/dev_report.py`
- `src/reporting/dev_notifier.py`
- `dags/paper_idea_pipeline.py`
- 관련 unit tests

즉 지금 당장 삭제하면 **운영 경로가 깨질 가능성**이 높다.

반면 `1w1a/backtesting` 은 `external/1w1a` 내부에서 자체적으로 일관된 코어를 형성하고 있다.

---

## 6. 권장 리팩토링 방향

### Phase 1. boundary 고정
바로 삭제하지 말고 역할을 고정한다.

- `1w1a/backtesting`: 계산/전략/리포트 코어
- `src/backtest`: bkclaw wrapper / compatibility / proof layer

### Phase 2. 코어 중복 금지
앞으로 새 엔진 기능, 새 전략 abstraction, 새 리포팅 코어는 **우선 1w1a에만 추가**한다.

`src/backtest` 에는 아래만 남기는 방향이 맞다.
- spec intake mapping
- run orchestration
- owner checklist
- artifact/delivery proof bridge
- legacy compatibility

### Phase 3. adapter 도입
중기적으로는 `src/backtest` 가 아래처럼 동작하게 만드는 것이 좋다.

- 입력: bkclaw `BacktestSpec`
- 변환: `1w1a.backtesting.run.RunConfig`
- 실행: `1w1a BacktestRunner`
- 후처리: bkclaw validation / checklist / delivery packet

즉 `src/backtest` 는 엔진이 아니라 **adapter + verification layer** 로 축소한다.

### Phase 4. 삭제 후보 정리
아래는 장기 삭제 후보다.
- `src/backtest/strategies/*.py` 의 legacy engine wrapper
- `src/backtest/strategy_registry.py` 중 전략 alias 중복 부분
- `scripts/*_backtest.py` 중 1w1a 전략으로 치환 가능한 스크립트

단, 삭제 전 조건:
1. 동일 전략이 1w1a에서 재현 가능
2. 성과 수치가 허용 오차 내 일치
3. 산출물 경로/검증/전달이 유지됨
4. 기존 호출자들이 adapter 경로로 동작함

---

## 7. 지금 즉시 삭제하면 안 되는 것

아래는 아직 남겨야 한다.

- `src/backtest/models.py`
  - bkclaw 운영 입력 스펙 역할
- `src/backtest/runner.py`
  - 현재 orchestration 진입점
- `src/validation/backtest_validation.py`
  - 운영 검증 체크
- `scripts/run_backtest.py`
  - 기존 호출 호환성
- `src/reporting/backtest_packet.py` 등 보고 연결부

즉 **지금 당장 엔진 삭제가 아니라, 엔진 책임 제거**가 먼저다.

---

## 8. 바로 실행할 리팩토링 원칙

1. `src/backtest` 를 신규 엔진 개발 장소로 쓰지 않는다.
2. 신규 전략/엔진/리포팅 코어는 `1w1a/backtesting` 우선.
3. bkclaw 쪽은 wrapper / proof / delivery / compatibility 에 집중.
4. 중복 구현이 생기면 `1w1a 우선, bkclaw bridge 후행` 원칙으로 정리.

---

## 9. 최종 권고

현재 가장 안전하고 효과적인 방향은 아래다.

- **삭제 보류**
- **역할 분리 리팩토링 즉시 적용**
- **차기 단계에서 adapter 방식으로 1w1a를 주 엔진으로 승격**

한 줄로 요약하면:

> `src/backtest` 는 줄이고, `1w1a/backtesting` 은 코어로 올리는 것이 맞다. 다만 삭제는 migration 이후다.
