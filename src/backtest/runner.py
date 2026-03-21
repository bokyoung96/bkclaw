from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from src.backtest.models import BacktestRunArtifacts, BacktestSpec
from src.backtest.output_standardizer import write_spec
from src.backtest.progress import JsonlProgressNotifier
from src.backtest.strategy_registry import get_strategy_runner
from src.validation.backtest_validation import validate_backtest_package


ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = ROOT / "reports" / "backtests"


def build_owner_checklist(spec: BacktestSpec) -> str:
    return f"""# Owner Checklist\n\n- 전략명: {spec.strategy_name}\n- 유니버스: {spec.universe}\n- 데이터 소스: {spec.datasource}\n- 기간: {spec.start_date} ~ {spec.end_date}\n- 리밸런싱: {spec.rebalance_rule}\n- 비용(bps): {spec.cost_bps}\n- 슬리피지(bps): {spec.slippage_bps}\n- 모드: {spec.mode}\n\n## 형이 확인할 것\n- 전략 정의가 요청과 일치하는가?\n- 비용/슬리피지가 의도와 일치하는가?\n- validation FAIL이 없는가?\n- WARN이 있으면 수용 가능한가?\n- 동일 스펙으로 재현 가능한가?\n- positions/holdings CSV가 존재하는가?\n"""


def run_backtest(spec: BacktestSpec) -> dict[str, object]:
    run_tag = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUN_ROOT / f"{spec.strategy_name.replace(' ', '_').lower()}_{run_tag}"
    artifacts = BacktestRunArtifacts(run_dir=run_dir)
    artifacts.ensure()
    notifier = JsonlProgressNotifier(run_dir=run_dir, strategy_name=spec.strategy_name)

    notifier.info("start", f"backtest started: {spec.strategy_name}", progress_pct=0.0)
    write_spec(artifacts, spec)

    strategy_runner = get_strategy_runner(spec.strategy_name)
    try:
        strategy_result = strategy_runner(spec=spec, run_dir=run_dir, notifier=notifier)
    except Exception as exc:
        notifier.error("run", f"backtest failed: {exc}")
        raise

    artifacts.write_json(artifacts.summary_path, strategy_result.summary.to_dict())
    artifacts.reproduce_path.write_text(
        f"#!/usr/bin/env bash\nset -euo pipefail\ncd {ROOT}\npython scripts/run_backtest.py --spec-file {artifacts.spec_path}\n",
        encoding="utf-8",
    )
    artifacts.reproduce_path.chmod(0o755)
    artifacts.owner_checklist_path.write_text(build_owner_checklist(spec), encoding="utf-8")
    if spec.economic_rationale or spec.rationale_risks or spec.source_links:
        research_context = {
            "economic_rationale": spec.economic_rationale,
            "rationale_risks": spec.rationale_risks,
            "source_links": spec.source_links,
        }
        artifacts.write_json(run_dir / "research_context.json", research_context)

    validation = validate_backtest_package(
        spec=spec,
        summary=strategy_result.summary.to_dict(),
        run_dir=run_dir,
        output_files=strategy_result.output_files,
    )
    artifacts.write_json(artifacts.validation_path, validation.to_dict())
    notifier.done("validation", f"validation complete: {validation.overall}", progress_pct=100.0)

    return {
        "run_dir": str(run_dir),
        "validation": validation.to_dict(),
        "summary": strategy_result.summary.to_dict(),
        "output_files": strategy_result.output_files.to_dict(),
        "warnings": strategy_result.warnings,
    }


def load_backtest_spec(spec_file: str | Path) -> BacktestSpec:
    payload = json.loads(Path(spec_file).read_text(encoding="utf-8"))
    return BacktestSpec(**payload)
