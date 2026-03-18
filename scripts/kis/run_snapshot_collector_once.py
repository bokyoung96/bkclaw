from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.collectors.kis_snapshot_collector import collect_domestic_future_asking_price, load_symbol_specs
from src.reporting.kis_collector_notifier import notify_kis_snapshot


def main() -> None:
    for spec in load_symbol_specs():
        symbol = spec["symbol"]
        market_code = spec.get("market_code", "F")
        snapshot, raw_path, norm_path = collect_domestic_future_asking_price(symbol=symbol, market_code=market_code)
        notify_kis_snapshot(symbol, snapshot, raw_path, norm_path)
        print(raw_path)
        print(norm_path)


if __name__ == "__main__":
    main()
