# BACKTEST_VERIFICATION_CHECKLIST.md

## Goal

백테스트 결과를 `성과 요약` 또는 `완료`로 보고하기 전에,
최소한의 가정/성과/실전성/전달 검증을 체크리스트로 고정한다.

## Assumptions Gate

- [ ] universe
- [ ] test period
- [ ] benchmark
- [ ] transaction cost / slippage
- [ ] rebalance cadence
- [ ] structure (long-only / long-short / market-neutral)
- [ ] risk constraints if any

## Core Performance Gate

- [ ] CAGR
- [ ] Volatility
- [ ] Sharpe
- [ ] MDD
- [ ] Calmar or equivalent downside metric
- [ ] Win Rate or equivalent hit-rate metric

## Robustness Gate

- [ ] subperiod / regime perspective checked or marked 미확인
- [ ] cost sensitivity checked or marked 미확인
- [ ] parameter sensitivity / fitting risk commented
- [ ] benchmark-relative interpretation included when relevant

## Deployability Gate

- [ ] turnover / rebalance practicality commented when relevant
- [ ] liquidity / concentration / implementation complexity commented
- [ ] final verdict given: Promote / Hold / Discard (or equivalent)

## Delivery Gate

- [ ] requested output scope matched (report / charts / git / merge)
- [ ] if charts requested, actual provider-visible delivery confirmed
- [ ] file generation only was not mistaken for user-visible delivery

## Rule

위 항목이 비어 있으면 아래처럼 분리 보고한다.
- `초안은 나왔지만 검증은 아직입니다.`
- `차트는 생성됐지만 Discord 전달 확인은 아직입니다.`
- `핵심 수치는 정리됐지만 비용 민감도 검증은 남아 있습니다.`
