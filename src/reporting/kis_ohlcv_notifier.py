from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DISPATCH = ROOT / "dispatch_discord.py"


def _dispatch(channel_name: str, message: str) -> None:
    payload = {
        "action": "dispatch_discord_message",
        "channel_name": channel_name,
        "message": message,
    }
    subprocess.run([sys.executable, str(DISPATCH)], input=json.dumps(payload), text=True, check=True, cwd=ROOT)


def _fmt_num(v: object) -> str:
    if v in (None, "", "-"):
        return "-"
    return str(v)


def notify_airflow_event(status: str, dag_id: str, detail: str, level_emoji: str) -> None:
    message = (
        f"{level_emoji} **Airflow | {status}**\n\n"
        f"### 🧭 DAG\n"
        f"- **dag_id**: `{dag_id}`\n"
        f"- **detail**: {detail}"
    )
    _dispatch("kis-collector", message)


def notify_kis_ohlcv(symbol: str, payload: dict, raw_path: str, norm_path: str, row_count: int) -> None:
    output1 = payload.get("output1", {}) or {}
    rows = payload.get("output2", []) or []
    latest = rows[0] if rows else {}

    message = (
        f"🕯️ **KIS OHLCV 수집 완료**\n\n"
        f"### 🧾 종목 정보\n"
        f"- **심볼**: `{symbol}`\n"
        f"- **이름**: {_fmt_num(output1.get('hts_kor_isnm'))}\n"
        f"- **현재가**: {_fmt_num(output1.get('futs_prpr'))}\n"
        f"- **전일대비**: {_fmt_num(output1.get('futs_prdy_vrss'))} ({_fmt_num(output1.get('futs_prdy_ctrt'))}%)\n"
        f"- **누적거래량**: {_fmt_num(output1.get('acml_vol'))}\n\n"
        f"### 📊 최신 1분봉\n"
        f"- **일자**: {_fmt_num(latest.get('stck_bsop_date'))}\n"
        f"- **시각**: {_fmt_num(latest.get('stck_cntg_hour'))}\n"
        f"- **Open**: {_fmt_num(latest.get('futs_oprc'))}\n"
        f"- **High**: {_fmt_num(latest.get('futs_hgpr'))}\n"
        f"- **Low**: {_fmt_num(latest.get('futs_lwpr'))}\n"
        f"- **Close**: {_fmt_num(latest.get('futs_prpr'))}\n"
        f"- **Volume**: {_fmt_num(latest.get('cntg_vol'))}\n\n"
        f"### 📦 수집 요약\n"
        f"- **row_count**: {row_count}\n"
        f"- **symbol_day_file**: `{Path(norm_path).name}`\n\n"
        f"### 💾 저장 경로\n"
        f"- **raw(JSONL)**: `{raw_path}`\n"
        f"- **normalized(Parquet)**: `{norm_path}`"
    )
    _dispatch("kis-collector", message)
