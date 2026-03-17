from dataclasses import dataclass
from pathlib import Path

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None


@dataclass
class DataValidationResult:
    exists: bool
    row_count: int | None
    column_count: int | None
    message: str


class DataValidator:
    def validate_tabular_file(self, path: str | Path) -> DataValidationResult:
        file_path = Path(path)
        if not file_path.exists():
            return DataValidationResult(False, None, None, f"missing: {file_path}")

        if pd is None:
            return DataValidationResult(True, None, None, "pandas not installed; existence only checked")

        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(file_path)
        elif suffix == ".parquet":
            df = pd.read_parquet(file_path)
        else:
            return DataValidationResult(True, None, None, f"exists but unsupported suffix: {suffix}")

        return DataValidationResult(
            exists=True,
            row_count=len(df),
            column_count=len(df.columns),
            message="ok",
        )
