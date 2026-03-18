from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.backtest.models import BacktestRunArtifacts, BacktestSpec


STANDARD_PLOT_NAMES = {
    "cumulative_return_and_drawdown.png": "plots/cumulative_return_and_drawdown.png",
    "return_distributions.png": "plots/return_distributions.png",
    "return_histograms.png": "plots/return_distributions.png",
}

STANDARD_DATA_NAMES = {
    "daily_portfolio_series.csv": "data/daily_portfolio_series.csv",
    "daily_returns.csv": "data/daily_portfolio_series.csv",
    "monthly_portfolio_returns.csv": "data/monthly_portfolio_returns.csv",
    "monthly_returns.csv": "data/monthly_portfolio_returns.csv",
    "last_holdings.csv": "data/last_holdings.csv",
    "turnover.csv": "data/turnover.csv",
    "nav_drawdown.csv": "data/nav_drawdown.csv",
}


def write_spec(artifacts: BacktestRunArtifacts, spec: BacktestSpec) -> None:
    artifacts.write_json(artifacts.spec_path, spec.to_dict())


def copy_standard_outputs(source_dir: Path, run_dir: Path) -> dict[str, str]:
    copied: dict[str, str] = {}
    for src_name, rel_dest in {**STANDARD_PLOT_NAMES, **STANDARD_DATA_NAMES}.items():
        src = source_dir / src_name
        if not src.exists():
            continue
        dest = run_dir / rel_dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied[src_name] = str(dest)

    progress_note = source_dir / "progress_note.md"
    if progress_note.exists():
        dest = run_dir / "notes" / "progress_note.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(progress_note, dest)
        copied["progress_note.md"] = str(dest)

    summary = source_dir / "summary.json"
    if summary.exists():
        dest = run_dir / "raw_summary.json"
        shutil.copy2(summary, dest)
        copied["summary.json"] = str(dest)

    return copied


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
