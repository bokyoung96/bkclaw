from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.validation.check_data import DataValidator


if __name__ == "__main__":
    validator = DataValidator()
    sample_path = Path("data/raw/market/prices.parquet")
    result = validator.validate_tabular_file(sample_path)
    print(result)
