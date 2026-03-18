from __future__ import annotations

from src.backtest.strategies.sector_neutral_6m_momentum import run_strategy as run_sector_neutral_6m
from src.backtest.strategies.spy_momentum import run_strategy as run_spy_momentum


STRATEGY_REGISTRY = {
    "quant_db_momentum_fast": run_spy_momentum,
    "spy_momentum_top10": run_spy_momentum,
    "spy_sector_neutral_6m_momentum": run_sector_neutral_6m,
    "sector_neutral_6m_momentum": run_sector_neutral_6m,
}


def get_strategy_runner(strategy_name: str):
    try:
        return STRATEGY_REGISTRY[strategy_name]
    except KeyError as exc:
        raise KeyError(f"Unknown strategy: {strategy_name}. Available: {sorted(STRATEGY_REGISTRY)}") from exc
