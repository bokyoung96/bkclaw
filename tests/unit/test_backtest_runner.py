from pathlib import Path

from src.backtest.models import BacktestSpec
from src.backtest.runner import build_owner_checklist


def test_owner_checklist_contains_requested_fields() -> None:
    spec = BacktestSpec(
        strategy_name="spy_momentum_top10",
        hypothesis="momentum persists",
        universe="SPY members",
        start_date="2020-01-01",
        end_date="2024-12-31",
        rebalance_rule="monthly",
    )

    checklist = build_owner_checklist(spec)

    assert "전략명: spy_momentum_top10" in checklist
    assert "리밸런싱: monthly" in checklist
