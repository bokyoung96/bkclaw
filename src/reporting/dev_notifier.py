from __future__ import annotations

from pathlib import Path

from src.backtest.progress import read_progress_tail


def build_dev_summary(run_dir: str | Path) -> str:
    run_dir = Path(run_dir)
    progress = read_progress_tail(run_dir / "progress_log.jsonl", n=10)
    if not progress:
        return f"[dev] backtest\n- run_dir: {run_dir}\n- status: no progress yet"

    last = progress[-1]
    return (
        f"[dev] {last.get('strategy_name','backtest')}\n"
        f"- event: {last.get('event_type')}\n"
        f"- step: {last.get('step')}\n"
        f"- message: {last.get('message')}\n"
        f"- progress_pct: {last.get('progress_pct')}\n"
        f"- run_dir: {run_dir}"
    )
