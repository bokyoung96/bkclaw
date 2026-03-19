from pathlib import Path

from src.reporting.dev_notifier import build_dev_summary
from src.reporting.dev_report import DevReport


def test_dev_report_markdown_includes_tags() -> None:
    report = DevReport(
        experiment_name="spy_momentum_top10",
        status="RUNNING",
        summary="collecting metrics",
        next_action="wait for validation",
    )

    markdown = report.to_markdown()

    assert "[dev] spy_momentum_top10" in markdown
    assert "- tags: dev, info" in markdown


def test_build_dev_summary_without_progress_uses_structured_report(tmp_path: Path) -> None:
    summary = build_dev_summary(tmp_path)

    assert "[dev]" in summary
    assert "status: NO_PROGRESS" in summary
