from __future__ import annotations

import math
from pathlib import Path

from src.backtest.models import BacktestOutputFiles, BacktestSpec, ValidationItem, ValidationReport


def validate_backtest_package(
    spec: BacktestSpec,
    summary: dict,
    run_dir: Path,
    output_files: BacktestOutputFiles | None = None,
) -> ValidationReport:
    items: list[ValidationItem] = []

    def add(name: str, ok: bool, warn: bool, pass_msg: str, fail_msg: str, warn_msg: str | None = None) -> None:
        if ok:
            items.append(ValidationItem(name=name, level="PASS", message=pass_msg))
        elif warn:
            items.append(ValidationItem(name=name, level="WARN", message=warn_msg or fail_msg))
        else:
            items.append(ValidationItem(name=name, level="FAIL", message=fail_msg))

    add(
        "strategy_name",
        bool(spec.strategy_name.strip()),
        False,
        "전략명이 존재합니다.",
        "전략명이 비어 있습니다.",
    )
    add(
        "universe",
        bool(spec.universe.strip()),
        False,
        "유니버스가 정의되어 있습니다.",
        "유니버스가 비어 있습니다.",
    )
    add(
        "date_range",
        bool(spec.start_date and spec.end_date),
        False,
        "기간이 정의되어 있습니다.",
        "시작일/종료일이 누락되었습니다.",
    )
    add(
        "cost_model",
        (spec.cost_bps + spec.slippage_bps) > 0,
        spec.mode == "fast",
        "비용/슬리피지가 반영되었습니다.",
        "비용/슬리피지가 0입니다.",
        "빠른 실험 모드에서는 비용이 0일 수 있습니다. 해석 시 주의하세요.",
    )
    add(
        "rebalance_rule",
        bool(spec.rebalance_rule.strip()),
        False,
        "리밸런싱 규칙이 정의되어 있습니다.",
        "리밸런싱 규칙이 비어 있습니다.",
    )

    sharpe = summary.get("sharpe")
    mdd = summary.get("max_drawdown")
    turnover = summary.get("turnover")
    cagr = summary.get("cagr")

    add(
        "summary_metrics_present",
        all(key in summary for key in ["cagr", "sharpe", "max_drawdown"]),
        False,
        "핵심 성과 지표가 존재합니다.",
        "핵심 성과 지표가 누락되었습니다.",
    )
    add(
        "summary_metrics_finite",
        all(not (isinstance(v, float) and (math.isnan(v) or math.isinf(v))) for v in [sharpe, mdd, cagr] if v is not None),
        False,
        "핵심 성과 지표가 유한값입니다.",
        "핵심 성과 지표에 NaN/Inf가 있습니다.",
    )
    add(
        "turnover_reasonable",
        turnover is not None and turnover <= 5.0,
        turnover is not None,
        "turnover가 허용 범위 안입니다.",
        "turnover가 과도하거나 누락되었습니다.",
        "turnover가 높습니다. 해석 시 체결 가능성을 재점검하세요.",
    )
    add(
        "reproduce_script",
        (run_dir / "reproduce.sh").exists(),
        False,
        "재현 스크립트가 존재합니다.",
        "재현 스크립트가 없습니다.",
    )
    add(
        "owner_checklist",
        (run_dir / "owner_checklist.md").exists(),
        False,
        "owner checklist가 존재합니다.",
        "owner checklist가 없습니다.",
    )
    add(
        "daily_series_csv",
        bool(output_files and output_files.daily_series_csv and Path(output_files.daily_series_csv).exists()),
        False,
        "일별 시계열 CSV가 존재합니다.",
        "일별 시계열 CSV가 없습니다.",
    )
    add(
        "monthly_series_csv",
        bool(output_files and output_files.monthly_series_csv and Path(output_files.monthly_series_csv).exists()),
        False,
        "월별 시계열 CSV가 존재합니다.",
        "월별 시계열 CSV가 없습니다.",
    )
    add(
        "positions_csv",
        bool(output_files and output_files.positions_csv and Path(output_files.positions_csv).exists()),
        True,
        "포지션 CSV가 존재합니다.",
        "포지션 CSV가 없습니다.",
        "포지션 CSV가 아직 생성되지 않았습니다. 최소 holdings CSV는 확인하세요.",
    )
    add(
        "cumulative_chart",
        bool(output_files and output_files.cumulative_chart and Path(output_files.cumulative_chart).exists()),
        False,
        "누적수익/드로우다운 차트가 존재합니다.",
        "누적수익/드로우다운 차트가 없습니다.",
    )
    add(
        "distribution_chart",
        bool(output_files and output_files.distribution_chart and Path(output_files.distribution_chart).exists()),
        True,
        "수익분포 차트가 존재합니다.",
        "수익분포 차트가 없습니다.",
        "분포 차트가 아직 없습니다.",
    )

    overall = "PASS"
    if any(item.level == "FAIL" for item in items):
        overall = "FAIL"
    elif any(item.level == "WARN" for item in items):
        overall = "WARN"

    return ValidationReport(overall=overall, items=items)
