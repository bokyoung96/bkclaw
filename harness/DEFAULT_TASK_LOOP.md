# DEFAULT_TASK_LOOP.md

## Purpose

가재의 의미 있는 작업 기본 루프를 한 장으로 고정한다.
이 문서는 research / backtest / result validation / delivery 작업의 상위 contract다.

## Default loop

의미 있는 작업의 기본값은 아래 순서를 따른다.

1. **Question**
2. **Assumption lock**
3. **Acceptance criteria**
4. **Execute**
5. **Verification**
6. **Delivery proof**
7. **Response / report**

한 줄 규칙:

> Default for meaningful work: **question -> assumption lock -> acceptance criteria -> verification -> delivery proof**.

## Trigger scope

이 루프는 아래에 기본 적용한다.
- research
- strategy / backtest
- result validation
- report / delivery
- git/reporting tasks where proof matters

## Skip rule

- 이미 mandate가 명확히 잠겨 있으면 `question` / `assumption lock` 일부는 생략 가능
- 단, 아래는 생략 금지:
  - verification
  - delivery proof (delivery가 요청 범위일 때)
  - completion language discipline

## Done language rule

산출물이 생성되었다고 완료가 아니다.
완료는 아래가 충족되어야 한다.
1. acceptance criteria 충족
2. validation evidence 존재
3. delivery가 요청 범위면 delivery proof 존재
4. remaining risks 또는 미확인 항목 명시

## Not-done language

아래 표현을 사용한다.
- `초안은 나왔지만 검증은 아직입니다.`
- `차트는 생성됐지만 Discord 전달 확인은 아직입니다.`
- `수정은 끝났지만 완료 proof는 아직입니다.`

## Subagent boundary

기본 규칙:
- **Lock first, split later. Merge centrally, declare done only with proof.**
- 의미 있는 병렬 spawn은 assumption lock 이후에만 수행한다.
- 예외:
  - 사용자가 명시적으로 넓은 exploratory scan을 요청한 경우
  - 추천/완료 판정이 없는 순수 탐색 작업

## Delivery proof examples

- Discord: message id / provider-visible success
- Git: local commit + push + merge + cleanup + notify proof when required
- Backtest: metric source artifact + chart artifact + delivery proof when requested
- Research: source-backed summary + requested delivery format satisfied
