from __future__ import annotations

from pathlib import Path

from src.backtest.models import BacktestExecutionResult, BacktestOutputFiles, BacktestSpec, BacktestSummary
from src.backtest.output_standardizer import copy_standard_outputs, load_json
from src.backtest.strategies.common import ROOT, run_legacy_script


LEGACY_OUTPUT = ROOT / "outputs" / "spy_momentum_top10"


def run_strategy(spec: BacktestSpec, run_dir: Path, notifier=None) -> BacktestExecutionResult:
    if notifier:
        notifier.info("run", "spy_momentum legacy script execution started")
    result = run_legacy_script("spy_momentum_backtest.py")
    copied = copy_standard_outputs(LEGACY_OUTPUT, run_dir)
    raw_summary = load_json(LEGACY_OUTPUT / "summary.json")
    raw_metrics = raw_summary.get("metrics", {})
    summary = BacktestSummary(
        status="OK",
        strategy_name=spec.strategy_name,
        start=raw_metrics.get("start", spec.start_date),
        end=raw_metrics.get("end", spec.end_date),
        cagr=float(raw_metrics.get("annual_return", 0.0)),
        annual_vol=float(raw_metrics.get("annual_vol", 0.0)),
        sharpe=float(raw_metrics.get("sharpe", 0.0)),
        max_drawdown=float(raw_metrics.get("max_drawdown", 0.0)),
        turnover=float(raw_metrics.get("avg_monthly_turnover", 0.0)),
        rebalance_count=len(raw_summary.get("rebalance_dates", [])),
        final_holdings_count=int(len((LEGACY_OUTPUT / "last_holdings.csv").read_text(encoding="utf-8").splitlines()) - 1) if (LEGACY_OUTPUT / "last_holdings.csv").exists() else 0,
        notes=[raw_metrics.get("start", ""), raw_metrics.get("end", "")],
        raw_metrics=raw_metrics,
    )
    output_files = BacktestOutputFiles(
        daily_series_csv=copied.get("daily_portfolio_series.csv"),
        monthly_series_csv=copied.get("monthly_portfolio_returns.csv"),
        positions_csv=copied.get("last_holdings.csv"),
        holdings_csv=copied.get("last_holdings.csv"),
        cumulative_chart=copied.get("cumulative_return_and_drawdown.png"),
        distribution_chart=copied.get("return_distributions.png"),
        progress_note=copied.get("progress_note.md"),
        extra_files=copied,
    )
    if notifier:
        notifier.done("run", "spy_momentum legacy script execution completed")
    return BacktestExecutionResult(summary=summary, output_files=output_files, validation_context={"stdout": result.stdout[-4000:]}, warnings=[])
