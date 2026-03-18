from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from src.data_sources.kis.client import KISClient
from src.data_sources.kis.config import KISConfig

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "kis" / "raw"
NORM_DIR = ROOT / "data" / "kis" / "normalized"
SYMBOL_CONFIG = ROOT / "configs" / "kis" / "symbols.json"


def _day_dirs(ts: datetime) -> tuple[Path, Path]:
    day = ts.strftime("%Y-%m-%d")
    raw_dir = RAW_DIR / day
    norm_dir = NORM_DIR / day
    raw_dir.mkdir(parents=True, exist_ok=True)
    norm_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, norm_dir


def _append_parquet(path: Path, row: dict) -> None:
    new_df = pd.DataFrame([row])
    if path.exists():
        old_df = pd.read_parquet(path)
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df
    df.to_parquet(path, index=False)


def load_symbol_specs() -> list[dict]:
    payload = json.loads(SYMBOL_CONFIG.read_text(encoding="utf-8"))
    return [item for item in payload.get("symbols", []) if item.get("enabled", True)]


def collect_domestic_future_asking_price(symbol: str = "A01606", market_code: str = "F") -> tuple[dict, str, str]:
    cfg = KISConfig.from_env()
    client = KISClient(cfg)
    snapshot = client.inquire_domestic_future_asking_price(market_code=market_code, symbol=symbol)

    ts = datetime.now(UTC)
    raw_dir, norm_dir = _day_dirs(ts)
    raw_path = raw_dir / f"{symbol}.jsonl"
    norm_path = norm_dir / f"{symbol}.parquet"

    out1 = snapshot.get("output1", {})
    out2 = snapshot.get("output2", {})

    raw_record = {
        "collected_at_utc": ts.isoformat(),
        "symbol": symbol,
        "market_code": market_code,
        "snapshot": snapshot,
    }
    with raw_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(raw_record, ensure_ascii=False) + "\n")

    normalized = {
        "collected_at_utc": ts.isoformat(),
        "symbol": symbol,
        "market_code": market_code,
        "name": out1.get("hts_kor_isnm"),
        "timestamp_hhmmss": out2.get("aspr_acpt_hour"),
        "last_price": out1.get("futs_prpr"),
        "change": out1.get("futs_prdy_vrss"),
        "change_pct": out1.get("futs_prdy_ctrt"),
        "volume": out1.get("acml_vol"),
        "ask1": out2.get("futs_askp1"),
        "ask2": out2.get("futs_askp2"),
        "ask3": out2.get("futs_askp3"),
        "ask4": out2.get("futs_askp4"),
        "ask5": out2.get("futs_askp5"),
        "bid1": out2.get("futs_bidp1"),
        "bid2": out2.get("futs_bidp2"),
        "bid3": out2.get("futs_bidp3"),
        "bid4": out2.get("futs_bidp4"),
        "bid5": out2.get("futs_bidp5"),
        "ask1_size": out2.get("askp_rsqn1"),
        "ask2_size": out2.get("askp_rsqn2"),
        "ask3_size": out2.get("askp_rsqn3"),
        "ask4_size": out2.get("askp_rsqn4"),
        "ask5_size": out2.get("askp_rsqn5"),
        "bid1_size": out2.get("bidp_rsqn1"),
        "bid2_size": out2.get("bidp_rsqn2"),
        "bid3_size": out2.get("bidp_rsqn3"),
        "bid4_size": out2.get("bidp_rsqn4"),
        "bid5_size": out2.get("bidp_rsqn5"),
        "total_ask_size": out2.get("total_askp_rsqn"),
        "total_bid_size": out2.get("total_bidp_rsqn"),
        "total_ask_count": out2.get("total_askp_csnu"),
        "total_bid_count": out2.get("total_bidp_csnu"),
    }
    _append_parquet(norm_path, normalized)
    return snapshot, str(raw_path), str(norm_path)
