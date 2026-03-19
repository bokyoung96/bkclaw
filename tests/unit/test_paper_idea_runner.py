from pathlib import Path

from src.workflows.paper_idea_runner import run_paper_idea_pipeline


def test_paper_idea_runner_returns_both_reports(tmp_path: Path) -> None:
    config = tmp_path / "exp.yaml"
    config.write_text("name: momentum_trial\n", encoding="utf-8")

    result = run_paper_idea_pipeline(config)

    assert "dev_report" in result
    assert "research_report" in result
    assert "momentum_trial" in result["dev_report"]
