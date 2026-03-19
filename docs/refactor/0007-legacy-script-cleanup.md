# Legacy Script Cleanup

## Goal

Legacy backtest scripts should stop re-implementing workspace path and credential logic.

## Cleanup rules

- script-local `.env` parsing should be replaced by shared helpers
- absolute workspace output paths should be replaced by root-relative paths
- DB credential loading should use a shared function

## Current progress

- shared Python env loader added
- shared Quant DB credential loader added
- `spy_momentum_backtest.py` now uses shared DB loading
- `sector_neutral_6m_momentum_backtest.py` now uses shared DB loading and root-relative output paths
