from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class JsonlProgressNotifier:
    def __init__(self, run_dir: Path, strategy_name: str):
        self.run_dir = run_dir
        self.strategy_name = strategy_name
        self.path = run_dir / "progress_log.jsonl"

    def emit(self, level: str, step: str, message: str, event_type: str, progress_pct: float | None = None) -> None:
        payload = {
            "ts": datetime.now(UTC).isoformat(),
            "level": level,
            "step": step,
            "message": message,
            "run_dir": str(self.run_dir),
            "strategy_name": self.strategy_name,
            "event_type": event_type,
            "progress_pct": progress_pct,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def info(self, step: str, message: str, progress_pct: float | None = None) -> None:
        self.emit("INFO", step, message, "step_info", progress_pct)

    def warning(self, step: str, message: str, progress_pct: float | None = None) -> None:
        self.emit("WARNING", step, message, "step_warning", progress_pct)

    def error(self, step: str, message: str, progress_pct: float | None = None) -> None:
        self.emit("ERROR", step, message, "run_failed", progress_pct)

    def done(self, step: str, message: str, progress_pct: float | None = 100.0) -> None:
        self.emit("DONE", step, message, "run_finished", progress_pct)


def read_progress_tail(path: Path, n: int = 20) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()[-n:]
    return [json.loads(line) for line in lines if line.strip()]
