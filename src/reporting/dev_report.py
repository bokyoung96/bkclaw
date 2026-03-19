from dataclasses import dataclass
from pathlib import Path

from src.backtest.progress import read_progress_tail
from src.common.runtime import RuntimeContext, resolve_runtime_context
from src.reporting.report_envelope import ReportEnvelope


@dataclass
class DevReport:
    experiment_name: str
    status: str
    summary: str
    next_action: str
    run_dir: str | None = None
    level: str = "INFO"
    runtime_context: RuntimeContext | None = None

    def to_envelope(self) -> ReportEnvelope:
        tags = ["dev", self.level.lower()]
        if self.runtime_context is not None:
            tags.append(self.runtime_context.mode)
            tags.append(self.runtime_context.purpose)
        bullets = [
            f"level: {self.level}",
            f"status: {self.status}",
            f"summary: {self.summary}",
            f"next_action: {self.next_action}",
        ]
        if self.run_dir:
            bullets.append(f"run_dir: {self.run_dir}")
        return ReportEnvelope(title=f"[dev] {self.experiment_name}", bullets=bullets, tags=tags)

    def to_markdown(self) -> str:
        return self.to_envelope().to_markdown()

    @classmethod
    def from_progress(cls, run_dir: str | Path) -> "DevReport":
        run_dir = Path(run_dir)
        events = read_progress_tail(run_dir / "progress_log.jsonl", n=10)
        if not events:
            return cls(
                experiment_name=run_dir.name,
                status="NO_PROGRESS",
                summary="no progress log found",
                next_action="inspect runner execution",
                run_dir=str(run_dir),
                level="WARNING",
                runtime_context=resolve_runtime_context(mode="fast", purpose="reporting", tags=(run_dir.name,)),
            )
        last = events[-1]
        return cls(
            experiment_name=last.get("strategy_name", run_dir.name),
            status=last.get("event_type", "unknown"),
            summary=last.get("message", ""),
            next_action="check validation/summary artifacts",
            run_dir=str(run_dir),
            level=last.get("level", "INFO"),
            runtime_context=resolve_runtime_context(mode="fast", purpose="reporting", tags=(run_dir.name,)),
        )
