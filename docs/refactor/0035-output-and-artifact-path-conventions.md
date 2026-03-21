# Output and Artifact Path Conventions

## Problem

The workspace currently carries overlapping path conventions:
- `data/`
- `datas/`
- `outputs/`
- `reports/`
- `logs/`
- `external/`

This is workable, but it increases ambiguity when deciding where new artifacts should go.

## Current-safe convention

Until a larger migration is approved, use the following rules:

### 1. `data/`
Use for durable datasets and pipeline-ready inputs/derivatives.
Examples:
- raw market data
- processed datasets
- staging tables
- feature sets
- KIS collector outputs that behave like data assets

### 2. `outputs/`
Use for run-specific generated artifacts.
Examples:
- model outputs
- strategy result folders
- generated tables
- Tavily result bundles
- ad hoc experiment outputs

### 3. `reports/`
Use for human-facing summaries and structured reporting deliverables.
Examples:
- backtest summaries
- operator-facing markdown reports
- review notes intended for reading, not re-ingestion

### 4. `logs/`
Use for operational/runtime logs only.
Examples:
- restart reports
- runtime state captures
- collector logs
- backtest execution logs

### 5. `external/`
Use for checked-out external dependencies or vendor-style code that is not first-party workspace source.

### 6. `datas/`
Treat as legacy.
Do not create new top-level content here unless a migration plan explicitly says otherwise.
When practical, move future content toward `data/`, `outputs/`, or `reports/` depending on role.

## Operator rule

When adding a new path, ask first:
1. Is this a durable dataset? -> `data/`
2. Is this a run artifact? -> `outputs/`
3. Is this a human-facing summary? -> `reports/`
4. Is this an operational log? -> `logs/`
5. Is this third-party code? -> `external/`

## Non-goal

This document does not perform a bulk migration yet.
It defines a stable rule so future work stops increasing path entropy.
