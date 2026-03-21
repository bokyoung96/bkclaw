from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.backtest.models import BacktestSpec


@dataclass
class BacktestPacket:
    title: str
    strategy_name: str
    period: str
    metrics: dict[str, Any]
    hypothesis: str
    economic_rationale: list[str]
    rationale_risks: list[str]
    source_links: list[str]
    notes: list[str]

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            "## Strategy Overview",
            f"- strategy: {self.strategy_name}",
            f"- period: {self.period}",
            f"- hypothesis: {self.hypothesis}",
            "",
            "## Key Metrics",
        ]
        for key, value in self.metrics.items():
            lines.append(f"- {key}: {value}")
        if self.economic_rationale:
            lines += ["", "## Economic Rationale"]
            lines += [f"- {item}" for item in self.economic_rationale]
        if self.rationale_risks:
            lines += ["", "## Risks / Caveats"]
            lines += [f"- {item}" for item in self.rationale_risks]
        if self.notes:
            lines += ["", "## Notes"]
            lines += [f"- {item}" for item in self.notes]
        if self.source_links:
            lines += ["", "## Source Links"]
            lines += [f"- {item}" for item in self.source_links]
        return "\n".join(lines) + "\n"


def _compact_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "cagr",
        "annual_vol",
        "volatility",
        "sharpe",
        "max_drawdown",
        "mdd",
        "calmar",
        "turnover",
        "avg_monthly_turnover",
        "rebalance_count",
        "final_holdings_count",
        "daily_win_rate",
        "monthly_win_rate",
    ]
    out: dict[str, Any] = {}
    for key in keys:
        if key in summary:
            out[key] = summary[key]
    return out


def build_backtest_packet(spec: BacktestSpec, summary: dict[str, Any]) -> BacktestPacket:
    start = summary.get("start", spec.start_date)
    end = summary.get("end", spec.end_date)
    period = f"{start} ~ {end}".strip()
    notes = list(summary.get("notes", []))
    return BacktestPacket(
        title=f"Backtest Packet — {spec.strategy_name}",
        strategy_name=spec.strategy_name,
        period=period,
        metrics=_compact_metrics(summary),
        hypothesis=spec.hypothesis,
        economic_rationale=list(spec.economic_rationale),
        rationale_risks=list(spec.rationale_risks),
        source_links=list(spec.source_links),
        notes=notes,
    )


def write_packet_markdown(packet: BacktestPacket, path: Path) -> None:
    path.write_text(packet.to_markdown(), encoding="utf-8")


def _escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_pdf_stream(lines: list[str]) -> bytes:
    commands = ["BT", "/F1 10 Tf", "50 800 Td", "14 TL"]
    first = True
    for line in lines:
        esc = _escape_pdf_text(line)
        if first:
            commands.append(f"({esc}) Tj")
            first = False
        else:
            commands.append("T*")
            commands.append(f"({esc}) Tj")
    commands.append("ET")
    return "\n".join(commands).encode("latin-1", errors="replace")


def write_packet_pdf(packet: BacktestPacket, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page_lines = [packet.title, "", f"Strategy: {packet.strategy_name}", f"Period: {packet.period}", "", "Key Metrics:"]
    for k, v in packet.metrics.items():
        page_lines.append(f"- {k}: {v}")
    if packet.economic_rationale:
        page_lines += ["", "Economic Rationale:"] + [f"- {x}" for x in packet.economic_rationale]
    if packet.rationale_risks:
        page_lines += ["", "Risks / Caveats:"] + [f"- {x}" for x in packet.rationale_risks]
    if packet.source_links:
        page_lines += ["", "Source Links:"] + [f"- {x}" for x in packet.source_links]

    wrapped: list[str] = []
    for line in page_lines:
        if not line:
            wrapped.append("")
            continue
        wrapped.extend(textwrap.wrap(line, width=95) or [""])

    stream = _build_pdf_stream(wrapped)
    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += f"xref\n0 {len(objects)+1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    path.write_bytes(out)


def load_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
