from __future__ import annotations

from pathlib import Path

from src.backtest.progress import read_progress_tail
from src.reporting.dev_report import DevReport


def build_dev_summary(run_dir: str | Path) -> str:
    run_dir = Path(run_dir)
    progress = read_progress_tail(run_dir / "progress_log.jsonl", n=10)
    if not progress:
        return DevReport.from_progress(run_dir).to_markdown()

    last = progress[-1]
    report = DevReport(
        experiment_name=last.get("strategy_name", "backtest"),
        status=last.get("event_type", "unknown"),
        summary=last.get("message", ""),
        next_action=f"step={last.get('step')} / progress_pct={last.get('progress_pct')}",
        run_dir=str(run_dir),
        level=last.get("level", "INFO"),
    )
    return report.to_markdown()
