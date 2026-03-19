from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.backtest.artifacts import build_artifact_manifest, resolve_artifact_spec
from src.backtest.models import BacktestRunArtifacts, BacktestSpec


def write_spec(artifacts: BacktestRunArtifacts, spec: BacktestSpec) -> None:
    artifacts.write_json(artifacts.spec_path, spec.to_dict())


def copy_standard_outputs(source_dir: Path, run_dir: Path) -> dict[str, str]:
    copied: dict[str, str] = {}
    for src_name, spec in sorted((name, spec) for name, spec in {
        key: resolve_artifact_spec(key) for key in [
            "cumulative_return_and_drawdown.png",
            "return_distributions.png",
            "return_histograms.png",
            "daily_portfolio_series.csv",
            "daily_returns.csv",
            "monthly_portfolio_returns.csv",
            "monthly_returns.csv",
            "last_holdings.csv",
            "turnover.csv",
            "nav_drawdown.csv",
            "progress_note.md",
            "summary.json",
        ]
    }.items() if spec is not None):
        src = source_dir / src_name
        if not src.exists():
            continue
        dest = run_dir / spec.relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied[src_name] = str(dest)

    manifest = build_artifact_manifest(copied, run_dir=run_dir)
    if manifest:
        (run_dir / "artifact_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return copied


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
