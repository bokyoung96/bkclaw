from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.backtest.runner import load_backtest_spec
from src.reporting.backtest_packet import build_backtest_packet, load_summary, write_packet_markdown, write_packet_pdf


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate markdown/pdf packet from a backtest run directory")
    parser.add_argument("run_dir", help="Path to reports/backtests/<run>")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    spec = load_backtest_spec(run_dir / "spec.json")
    summary = load_summary(run_dir / "summary.json")
    packet = build_backtest_packet(spec, summary)

    notes_dir = run_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    md_path = notes_dir / "backtest_packet.md"
    pdf_path = notes_dir / "backtest_packet.pdf"
    write_packet_markdown(packet, md_path)
    write_packet_pdf(packet, pdf_path)
    print(md_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
