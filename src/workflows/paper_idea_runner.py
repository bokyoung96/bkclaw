from __future__ import annotations

from pathlib import Path

from src.workflows.paper_idea_pipeline import PaperIdeaPipeline


DEFAULT_CONFIG_PATH = Path("configs/experiments/example_experiment.yaml")


def run_paper_idea_pipeline(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, str]:
    pipeline = PaperIdeaPipeline(config_path=config_path)
    return pipeline.run()
