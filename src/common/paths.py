from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def configs(self) -> Path:
        return self.root / "configs"

    @property
    def outputs(self) -> Path:
        return self.root / "outputs"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    @property
    def dags(self) -> Path:
        return self.root / "dags"


def get_project_paths(root: str | Path = ".") -> ProjectPaths:
    return ProjectPaths(root=Path(root).resolve())
