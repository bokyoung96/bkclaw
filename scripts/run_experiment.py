from pathlib import Path

from src.workflows.paper_idea_runner import run_paper_idea_pipeline


if __name__ == "__main__":
    result = run_paper_idea_pipeline(Path("configs/experiments/example_experiment.yaml"))
    print(result["dev_report"])
    print()
    print(result["research_report"])
