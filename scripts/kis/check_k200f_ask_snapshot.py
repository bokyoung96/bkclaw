from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_sources.kis.client import KISClient
from src.data_sources.kis.config import KISConfig


def main() -> None:
    cfg = KISConfig.from_env()
    client = KISClient(cfg)
    body = client.inquire_domestic_future_asking_price(market_code="F", symbol="A01606")
    print(json.dumps(body, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
