from __future__ import annotations

import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

from src.backtest.models import BacktestExecutionResult, BacktestOutputFiles, BacktestSpec, BacktestSummary

ROOT = Path(__file__).resolve().parents[2]
ONEW1A_ROOT = ROOT / "external" / "1w1a"
if str(ONEW1A_ROOT) not in sys.path:
    sys.path.insert(0, str(ONEW1A_ROOT))

from backtesting.run import BacktestRunner, RunConfig  # type: ignore

SUPPORTED_STRATEGIES = {
    "quant_db_momentum_fast": "momentum",
    "spy_momentum_top10": "momentum",
    "momentum": "momentum",
}


def supports_strategy(strategy_name: str) -> bool:
    return strategy_name in SUPPORTED_STRATEGIES


def _map_schedule(spec: BacktestSpec) -> str:
    rule = (spec.rebalance_rule or "monthly").strip().lower()
    if rule in {"daily", "weekly", "monthly"}:
        return rule
    if "week" in rule:
        return "weekly"
    if "day" in rule:
        return "daily"
    return "monthly"


def _map_fill_mode(spec: BacktestSpec) -> str:
    assumption = (spec.execution_assumption or "close_to_close").strip().lower()
    if assumption in {"next_open", "open_to_open", "close_to_open"}:
        return "next_open"
    return "close"


def _map_run_config(spec: BacktestSpec) -> RunConfig:
    strategy = SUPPORTED_STRATEGIES[spec.strategy_name]
    return RunConfig(
        start=spec.start_date,
        end=spec.end_date,
        strategy=strategy,
        name=spec.strategy_name,
        top_n=10 if spec.strategy_name == "spy_momentum_top10" else 20,
        lookback=20,
        schedule=_map_schedule(spec),
        fill_mode=_map_fill_mode(spec),
        fee=spec.cost_bps / 10000.0,
        slippage=spec.slippage_bps / 10000.0,
    )


def _copy(src: Path, dst: Path) -> str | None:
    if not src.exists():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return str(dst)


def run_via_1w1a(spec: BacktestSpec, *, run_dir: Path, notifier=None) -> BacktestExecutionResult:
    if not supports_strategy(spec.strategy_name):
        raise KeyError(f"1w1a adapter does not support strategy: {spec.strategy_name}")

    config = _map_run_config(spec)
    result_root = ONEW1A_ROOT / 'results' / 'backtests'
    if notifier:
        notifier.info('bridge', f'1w1a bridge start: {config.strategy}')
    report = BacktestRunner(result_dir=result_root).run(config)
    output_dir = report.output_dir
    if output_dir is None:
        raise RuntimeError('1w1a run returned no output_dir')

    artifacts = {
        'daily_series_csv': _copy(output_dir / 'series' / 'equity.csv', run_dir / 'data' / 'daily_portfolio_series.csv'),
        'monthly_series_csv': _copy(output_dir / 'series' / 'monthly_returns.csv', run_dir / 'data' / 'monthly_portfolio_returns.csv'),
        'positions_csv': _copy(output_dir / 'positions' / 'latest_qty.csv', run_dir / 'data' / 'last_holdings.csv'),
        'holdings_csv': _copy(output_dir / 'positions' / 'latest_weights.csv', run_dir / 'data' / 'last_holdings_weights.csv'),
        'cumulative_chart': _copy(output_dir / 'plots' / 'equity.png', run_dir / 'plots' / 'cumulative_return_and_drawdown.png'),
        'distribution_chart': _copy(output_dir / 'plots' / 'drawdown.png', run_dir / 'plots' / 'return_distributions.png'),
    }

    bridge_meta = {
        'source': '1w1a',
        'source_output_dir': str(output_dir),
        'run_config': asdict(config),
        'raw_summary': report.summary,
    }
    (run_dir / 'bridge_1w1a.json').write_text(json.dumps(bridge_meta, ensure_ascii=False, indent=2), encoding='utf-8')

    summary = BacktestSummary(
        status='OK',
        strategy_name=spec.strategy_name,
        start=spec.start_date,
        end=spec.end_date,
        cagr=float(report.summary.get('cagr', 0.0)),
        annual_vol=float(report.summary.get('annual_vol', 0.0)),
        sharpe=float(report.summary.get('sharpe', 0.0)),
        max_drawdown=float(report.summary.get('mdd', 0.0)),
        turnover=float(report.summary.get('avg_turnover', 0.0)),
        rebalance_count=0,
        final_holdings_count=0 if report.result.qty.empty else int((report.result.qty.iloc[-1] != 0).sum()),
        notes=[f'1w1a_source:{output_dir.name}'],
        raw_metrics=dict(report.summary),
    )
    output_files = BacktestOutputFiles(
        daily_series_csv=artifacts['daily_series_csv'],
        monthly_series_csv=artifacts['monthly_series_csv'],
        positions_csv=artifacts['positions_csv'],
        holdings_csv=artifacts['holdings_csv'],
        cumulative_chart=artifacts['cumulative_chart'],
        distribution_chart=artifacts['distribution_chart'],
        extra_files={'bridge_meta': str(run_dir / 'bridge_1w1a.json')},
    )
    if notifier:
        notifier.done('bridge', '1w1a bridge completed')
    return BacktestExecutionResult(summary=summary, output_files=output_files, validation_context=bridge_meta, warnings=[])
