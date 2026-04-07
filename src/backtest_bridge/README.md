# src/backtest_bridge

## purpose
This directory will become bkclaw's bridge/orchestration layer for 1w1a-backed backtests.

It is intentionally separate from the backtest engine itself.

## intended responsibilities
- map bkclaw request/spec to 1w1a `RunConfig`
- invoke 1w1a backtest runs
- read persisted run outputs
- assemble owner checklist / packet / Discord-facing summary
- normalize saved runs/report bundles into Discord payload pieces (markdown + attachments + metadata)
- enforce verification and delivery-proof rules

## non-responsibilities
- no engine core
- no strategy core
- no duplicate reporting core
- no duplicate performance calculation logic

## migration note
`src/backtest` is legacy and should be reduced over time.
New bridge-facing work should prefer this directory rather than adding more backtest-core logic under `src/backtest`.
