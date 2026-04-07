from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DiscordPayload:
    message_markdown: str
    attachment_paths: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def build_discord_payload(run_or_bundle_dir: str | Path) -> DiscordPayload:
    root = Path(run_or_bundle_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"bundle directory not found: {root}")

    summary = _load_summary(root)
    metrics = _extract_metrics(summary)
    strategy_name = _extract_strategy_name(root, summary)
    period = _extract_period(summary, metrics)
    attachments = _collect_attachments(root)
    progress_note = _load_optional_text(root / "progress_note.md")
    packet_note = _load_optional_text(root / "packet.md")

    lines = [
        "[성과 요약] 📊",
        f"**전략:** {strategy_name}",
    ]
    if period:
        lines.append(f"**기간:** {period}")
    if metrics:
        lines.append("**핵심 성과지표**")
        for label, key in _metric_order():
            if key in metrics:
                lines.append(f"- {label}: {_format_metric(key, metrics[key])}")
    if progress_note:
        lines.extend(["**전략 설명**", *_markdownify_note(progress_note)])
    elif packet_note:
        lines.extend(["**메모**", *_markdownify_note(packet_note)])
    if attachments:
        lines.append(f"**첨부 차트:** {len(attachments)}개")

    metadata = {
        "bundle_dir": str(root),
        "strategy_name": strategy_name,
        "period": period,
        "summary_path": str(root / "summary.json") if (root / "summary.json").exists() else None,
        "progress_note_path": str(root / "progress_note.md") if (root / "progress_note.md").exists() else None,
        "attachment_count": len(attachments),
        "metrics": metrics,
        "source_kind": _detect_source_kind(root),
    }
    return DiscordPayload(
        message_markdown="\n".join(lines).strip() + "\n",
        attachment_paths=[str(path) for path in attachments],
        metadata=metadata,
    )


def _load_summary(root: Path) -> dict[str, Any]:
    summary_path = root / "summary.json"
    if not summary_path.exists():
        return {}
    return json.loads(summary_path.read_text(encoding="utf-8"))


def _extract_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    metrics = summary.get("metrics")
    if isinstance(metrics, dict):
        return metrics
    if not summary:
        return {}
    passthrough_keys = {
        "start",
        "end",
        "cagr",
        "annual_return",
        "annual_vol",
        "volatility",
        "sharpe",
        "max_drawdown",
        "mdd",
        "calmar",
        "avg_monthly_turnover",
        "turnover",
        "rebalance_count",
        "final_holdings_count",
    }
    return {key: value for key, value in summary.items() if key in passthrough_keys}


def _extract_strategy_name(root: Path, summary: dict[str, Any]) -> str:
    for key in ("strategy", "strategy_name", "name"):
        value = summary.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return root.name


def _extract_period(summary: dict[str, Any], metrics: dict[str, Any]) -> str | None:
    start = metrics.get("start") or summary.get("start")
    end = metrics.get("end") or summary.get("end")
    if start and end:
        return f"{start} ~ {end}"
    return None


def _metric_order() -> list[tuple[str, str]]:
    return [
        ("CAGR", "cagr"),
        ("Annual Return", "annual_return"),
        ("Volatility", "annual_vol"),
        ("Sharpe", "sharpe"),
        ("MDD", "max_drawdown"),
        ("Calmar", "calmar"),
        ("Turnover", "avg_monthly_turnover"),
        ("Rebalance Count", "rebalance_count"),
        ("Holdings", "final_holdings_count"),
    ]


def _format_metric(key: str, value: Any) -> str:
    if isinstance(value, float):
        if key in {"cagr", "annual_return", "annual_vol", "volatility", "max_drawdown", "mdd", "avg_monthly_turnover", "turnover"}:
            return f"{value:.2%}"
        return f"{value:.3f}"
    return str(value)


def _collect_attachments(root: Path) -> list[Path]:
    candidates = [
        root / "strategy_bundle.png",
        root / "cumulative_return_and_drawdown.png",
        root / "return_distributions.png",
        root / "return_histograms.png",
        root / "cumulative_return_and_drawdown_lite.jpg",
        root / "return_distributions_lite.jpg",
    ]
    out: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path.exists() and path not in seen:
            seen.add(path)
            out.append(path)
    return out


def _load_optional_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def _markdownify_note(note: str) -> list[str]:
    lines = []
    for raw in note.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("- "):
            lines.append(line)
        else:
            lines.append(f"- {line}")
    return lines[:8]


def _detect_source_kind(root: Path) -> str:
    if (root / "bridge_1w1a.json").exists():
        return "1w1a_run_dir"
    if (root / "strategy_bundle.png").exists():
        return "report_bundle"
    if (root / "summary.json").exists():
        return "saved_run"
    return "bundle_dir"
