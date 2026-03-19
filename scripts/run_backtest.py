from __future__ import annotations

import argparse
import json

from src.backtest.runner import load_backtest_spec, run_backtest


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest runner")
    parser.add_argument("--spec-file", type=str, help="Path to JSON spec file")
    args = parser.parse_args()

    if not args.spec_file:
        raise SystemExit("--spec-file is required")

    spec = load_backtest_spec(args.spec_file)
    result = run_backtest(spec)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
