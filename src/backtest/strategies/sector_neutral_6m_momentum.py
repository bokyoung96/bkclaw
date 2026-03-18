from __future__ import annotations

from pathlib import Path

from src.backtest.models import BacktestExecutionResult, BacktestOutputFiles, BacktestSpec, BacktestSummary
from src.backtest.output_standardizer import copy_standard_outputs, load_json
from src.backtest.strategies.common import ROOT, run_legacy_script


LEGACY_OUTPUT = ROOT / "outputs" / "spy_sector_neutral_6m_momentum"


def run_strategy(spec: BacktestSpec, run_dir: Path, notifier=None) -> BacktestExecutionResult:
    if notifier:
        notifier.info("run", "sector_neutral legacy script execution started")
    result = run_legacy_script("sector_neutral_6m_momentum_backtest.py")
    copied = copy_standard_outputs(LEGACY_OUTPUT, run_dir)
    raw_summary = load_json(LEGACY_OUTPUT / "summary.json")
    summary = BacktestSummary(
        status="OK",
        strategy_name=spec.strategy_name,
        start=raw_summary.get("start", spec.start_date),
        end=raw_summary.get("end", spec.end_date),
        cagr=float(raw_summary.get("cagr", 0.0)),
        annual_vol=float(raw_summary.get("volatility", 0.0)),
        sharpe=float(raw_summary.get("sharpe", 0.0)),
        max_drawdown=float(raw_summary.get("mdd", 0.0)),
        turnover=float(raw_summary.get("avg_monthly_turnover", 0.0)),
        rebalance_count=int(raw_summary.get("rebalance_count", 0) or 0),
        final_holdings_count=int(raw_summary.get("final_holdings_count", 0) or 0),
        notes=[raw_summary.get("last_rebalance", "")],
        raw_metrics=raw_summary,
    )
    output_files = BacktestOutputFiles(
        daily_series_csv=copied.get("daily_returns.csv") or copied.get("daily_portfolio_series.csv"),
        monthly_series_csv=copied.get("monthly_returns.csv") or copied.get("monthly_portfolio_returns.csv"),
        positions_csv=copied.get("last_holdings.csv"),
        holdings_csv=copied.get("last_holdings.csv"),
        cumulative_chart=copied.get("cumulative_return_and_drawdown.png"),
        distribution_chart=copied.get("return_histograms.png") or copied.get("return_distributions.png"),
        progress_note=copied.get("progress_note.md"),
        extra_files=copied,
    )
    if notifier:
        notifier.done("run", "sector_neutral legacy script execution completed")
    return BacktestExecutionResult(summary=summary, output_files=output_files, validation_context={"stdout": result.stdout[-4000:]}, warnings=[])
