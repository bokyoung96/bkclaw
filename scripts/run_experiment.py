from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.workflows.paper_idea_pipeline import PaperIdeaPipeline


if __name__ == "__main__":
    pipeline = PaperIdeaPipeline(
        config_path=Path("configs/experiments/example_experiment.yaml")
    )
    result = pipeline.run()
    print(result["dev_report"])
    print()
    print(result["research_report"])
