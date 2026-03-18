from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from src.data_sources.kis.client import KISClient
from src.data_sources.kis.config import KISConfig
from src.collectors.kis_snapshot_collector import load_symbol_specs

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "kis_ohlcv" / "raw"
NORM_DIR = ROOT / "data" / "kis_ohlcv" / "normalized"


def _day_dirs(ts: datetime) -> tuple[Path, Path]:
    day = ts.strftime("%Y-%m-%d")
    raw_dir = RAW_DIR / day
    norm_dir = NORM_DIR / day
    raw_dir.mkdir(parents=True, exist_ok=True)
    norm_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, norm_dir


def _append_parquet(path: Path, df_new: pd.DataFrame) -> None:
    if path.exists():
        old_df = pd.read_parquet(path)
        df = pd.concat([old_df, df_new], ignore_index=True)
        df = df.drop_duplicates()
    else:
        df = df_new
    df.to_parquet(path, index=False)


def collect_domestic_future_ohlcv(symbol: str = "A01606", market_code: str = "F") -> tuple[dict, str, str, int]:
    cfg = KISConfig.from_env()
    client = KISClient(cfg)
    payload = client.inquire_domestic_future_minute_bars(market_code=market_code, symbol=symbol)

    ts = datetime.now(UTC)
    raw_dir, norm_dir = _day_dirs(ts)
    raw_path = raw_dir / f"{symbol}.jsonl"
    norm_path = norm_dir / f"{symbol}.parquet"

    raw_record = {
        "collected_at_utc": ts.isoformat(),
        "symbol": symbol,
        "market_code": market_code,
        "payload": payload,
    }
    with raw_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(raw_record, ensure_ascii=False) + "\n")

    rows = payload.get("output2", []) or []
    df = pd.DataFrame(rows)
    if not df.empty:
        df.insert(0, "collected_at_utc", ts.isoformat())
        df.insert(1, "symbol", symbol)
        df.insert(2, "market_code", market_code)
        _append_parquet(norm_path, df)
    return payload, str(raw_path), str(norm_path), len(df)


def collect_all_symbols() -> list[tuple[str, dict, str, str, int]]:
    out = []
    for spec in load_symbol_specs():
        symbol = spec["symbol"]
        market_code = spec.get("market_code", "F")
        payload, raw_path, norm_path, row_count = collect_domestic_future_ohlcv(symbol=symbol, market_code=market_code)
        out.append((symbol, payload, raw_path, norm_path, row_count))
    return out
