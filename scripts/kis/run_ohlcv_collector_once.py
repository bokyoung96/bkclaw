from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.collectors.kis_ohlcv_collector import collect_all_symbols
from src.reporting.kis_ohlcv_notifier import notify_airflow_event, notify_kis_ohlcv

DAG_ID = "kis_ohlcv_collector"


def main() -> None:
    notify_airflow_event("START", DAG_ID, "OHLCV collector run started", "🚀")
    try:
        for symbol, payload, raw_path, norm_path, row_count in collect_all_symbols():
            notify_kis_ohlcv(symbol, payload, raw_path, norm_path, row_count)
            print(raw_path)
            print(norm_path)
            print(row_count)
        notify_airflow_event("DONE", DAG_ID, "OHLCV collector run completed", "✅")
    except Exception as exc:
        notify_airflow_event("ERROR", DAG_ID, str(exc), "❌")
        raise


if __name__ == "__main__":
    main()
