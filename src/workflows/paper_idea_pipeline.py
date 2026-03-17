from dataclasses import dataclass
from pathlib import Path

from src.common.config import YamlConfigLoader
from src.reporting.dev_report import DevReport
from src.reporting.research_report import ResearchReport


@dataclass
class PaperIdeaPipeline:
    config_path: Path

    def run(self) -> dict[str, str]:
        config = YamlConfigLoader(self.config_path).load()
        experiment_name = config.get("name", "unnamed_experiment")

        dev_report = DevReport(
            experiment_name=experiment_name,
            status="initialized",
            summary="pipeline skeleton created; waiting for data and model implementation",
            next_action="connect datasets and implement baseline model",
        )

        research_report = ResearchReport(
            title=experiment_name,
            period="N/A",
            result_summary="no experiment executed yet; skeleton only",
            risk_note="data and implementation not connected",
            next_action="add dataset config and baseline run",
        )

        return {
            "dev_report": dev_report.to_markdown(),
            "research_report": research_report.to_markdown(),
        }
