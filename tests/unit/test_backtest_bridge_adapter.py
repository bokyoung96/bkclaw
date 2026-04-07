from __future__ import annotations

from pathlib import Path

from src.backtest.models import BacktestSpec
from src.backtest_bridge.onew1a_adapter import supports_strategy


def test_1w1a_bridge_supports_momentum_aliases() -> None:
    assert supports_strategy("quant_db_momentum_fast") is True
    assert supports_strategy("spy_momentum_top10") is True
    assert supports_strategy("sector_neutral_6m_momentum") is False


def test_backtest_bridge_readme_exists() -> None:
    path = Path("src/backtest_bridge/README.md")
    assert path.exists()


def test_backtest_spec_still_available_for_bridge_layer() -> None:
    spec = BacktestSpec(
        strategy_name="spy_momentum_top10",
        hypothesis="momentum",
        universe="test",
        start_date="2020-01-01",
        end_date="2020-12-31",
        rebalance_rule="monthly",
    )
    assert spec.strategy_name == "spy_momentum_top10"
