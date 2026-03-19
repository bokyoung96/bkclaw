from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal
import json

from src.common.runtime import RuntimeContext, resolve_runtime_context

BacktestMode = Literal["fast", "deep"]
ValidationLevel = Literal["PASS", "WARN", "FAIL"]


@dataclass
class BacktestSpec:
    strategy_name: str
    hypothesis: str
    universe: str
    datasource: str = "quant_db"
    frequency: str = "daily"
    start_date: str = ""
    end_date: str = ""
    rebalance_rule: str = ""
    execution_assumption: str = "close_to_close"
    cost_bps: float = 0.0
    slippage_bps: float = 0.0
    constraints: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=lambda: ["summary", "plots"])
    mode: BacktestMode = "fast"

    def runtime_context(self) -> RuntimeContext:
        return resolve_runtime_context(mode=self.mode, purpose="backtest", tags=(self.strategy_name,))

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["runtime_context"] = self.runtime_context().to_dict()
        return payload


@dataclass
class ValidationItem:
    name: str
    level: ValidationLevel
    message: str


@dataclass
class ValidationReport:
    overall: ValidationLevel
    items: list[ValidationItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "overall": self.overall,
            "items": [asdict(item) for item in self.items],
        }


@dataclass
class BacktestSummary:
    status: str
    strategy_name: str
    start: str
    end: str
    cagr: float
    annual_vol: float
    sharpe: float
    max_drawdown: float
    turnover: float
    rebalance_count: int = 0
    final_holdings_count: int = 0
    notes: list[str] = field(default_factory=list)
    raw_metrics: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BacktestOutputFiles:
    daily_series_csv: str | None = None
    monthly_series_csv: str | None = None
    positions_csv: str | None = None
    holdings_csv: str | None = None
    cumulative_chart: str | None = None
    distribution_chart: str | None = None
    progress_note: str | None = None
    extra_files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BacktestExecutionResult:
    summary: BacktestSummary
    output_files: BacktestOutputFiles
    validation_context: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "summary": self.summary.to_dict(),
            "output_files": self.output_files.to_dict(),
            "validation_context": self.validation_context,
            "warnings": self.warnings,
        }


@dataclass
class BacktestRunArtifacts:
    run_dir: Path

    @property
    def plots_dir(self) -> Path:
        return self.run_dir / "plots"

    @property
    def spec_path(self) -> Path:
        return self.run_dir / "spec.json"

    @property
    def data_dir(self) -> Path:
        return self.run_dir / "data"

    @property
    def notes_dir(self) -> Path:
        return self.run_dir / "notes"

    @property
    def summary_path(self) -> Path:
        return self.run_dir / "summary.json"

    @property
    def validation_path(self) -> Path:
        return self.run_dir / "validation.json"

    @property
    def reproduce_path(self) -> Path:
        return self.run_dir / "reproduce.sh"

    @property
    def owner_checklist_path(self) -> Path:
        return self.run_dir / "owner_checklist.md"

    def ensure(self) -> None:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
