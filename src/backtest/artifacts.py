from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


ArtifactKind = Literal["plot", "dataset", "note", "summary", "validation", "raw"]
DeliveryIntent = Literal["internal", "dev", "research_lab"]


@dataclass(frozen=True)
class ArtifactSpec:
    name: str
    kind: ArtifactKind
    relative_path: str
    delivery_intent: DeliveryIntent = "internal"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


CANONICAL_ARTIFACT_SPECS: dict[str, ArtifactSpec] = {
    "cumulative_return_and_drawdown.png": ArtifactSpec(
        name="cumulative_return_and_drawdown",
        kind="plot",
        relative_path="plots/cumulative_return_and_drawdown.png",
        delivery_intent="research_lab",
    ),
    "return_distributions.png": ArtifactSpec(
        name="return_distributions",
        kind="plot",
        relative_path="plots/return_distributions.png",
        delivery_intent="research_lab",
    ),
    "return_histograms.png": ArtifactSpec(
        name="return_distributions",
        kind="plot",
        relative_path="plots/return_distributions.png",
        delivery_intent="research_lab",
    ),
    "daily_portfolio_series.csv": ArtifactSpec(
        name="daily_portfolio_series",
        kind="dataset",
        relative_path="data/daily_portfolio_series.csv",
    ),
    "daily_returns.csv": ArtifactSpec(
        name="daily_portfolio_series",
        kind="dataset",
        relative_path="data/daily_portfolio_series.csv",
    ),
    "monthly_portfolio_returns.csv": ArtifactSpec(
        name="monthly_portfolio_returns",
        kind="dataset",
        relative_path="data/monthly_portfolio_returns.csv",
    ),
    "monthly_returns.csv": ArtifactSpec(
        name="monthly_portfolio_returns",
        kind="dataset",
        relative_path="data/monthly_portfolio_returns.csv",
    ),
    "last_holdings.csv": ArtifactSpec(
        name="last_holdings",
        kind="dataset",
        relative_path="data/last_holdings.csv",
        delivery_intent="dev",
    ),
    "turnover.csv": ArtifactSpec(
        name="turnover",
        kind="dataset",
        relative_path="data/turnover.csv",
    ),
    "nav_drawdown.csv": ArtifactSpec(
        name="nav_drawdown",
        kind="dataset",
        relative_path="data/nav_drawdown.csv",
    ),
    "progress_note.md": ArtifactSpec(
        name="progress_note",
        kind="note",
        relative_path="notes/progress_note.md",
        delivery_intent="dev",
    ),
    "summary.json": ArtifactSpec(
        name="raw_summary",
        kind="raw",
        relative_path="raw_summary.json",
        delivery_intent="internal",
    ),
}


def resolve_artifact_spec(source_name: str) -> ArtifactSpec | None:
    return CANONICAL_ARTIFACT_SPECS.get(source_name)


def build_artifact_manifest(copied: dict[str, str], *, run_dir: Path) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    for source_name, absolute_dest in copied.items():
        spec = resolve_artifact_spec(source_name)
        if spec is None:
            continue
        dest = Path(absolute_dest)
        manifest.append(
            {
                "source_name": source_name,
                "name": spec.name,
                "kind": spec.kind,
                "delivery_intent": spec.delivery_intent,
                "relative_path": str(dest.relative_to(run_dir)),
            }
        )
    return sorted(manifest, key=lambda item: item["relative_path"])
