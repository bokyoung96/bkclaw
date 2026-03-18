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
    subprocess.run(
        [sys.executable, str(DISPATCH)],
        input=json.dumps(payload),
        text=True,
        check=True,
        cwd=ROOT,
    )


def notify_kis_snapshot(symbol: str, snapshot: dict, raw_path: str, norm_path: str) -> None:
    out1 = snapshot.get("output1", {})
    out2 = snapshot.get("output2", {})
    message = (
        f"📡 **KIS Collector | Snapshot 저장 완료**\n\n"
        f"### 🧾 종목 정보\n"
        f"- **심볼**: `{symbol}`\n"
        f"- **이름**: {out1.get('hts_kor_isnm', '-')}\n"
        f"- **호가 시각**: {out2.get('aspr_acpt_hour', '-')}\n\n"
        f"### 💹 현재가 요약\n"
        f"- **현재가**: {out1.get('futs_prpr', '-')}\n"
        f"- **전일대비**: {out1.get('futs_prdy_vrss', '-')} ({out1.get('futs_prdy_ctrt', '-')}%)\n"
        f"- **누적거래량**: {out1.get('acml_vol', '-')}\n\n"
        f"### 📚 1호가 요약\n"
        f"- **매도1**: {out2.get('futs_askp1', '-')} / 잔량 {out2.get('askp_rsqn1', '-')}\n"
        f"- **매수1**: {out2.get('futs_bidp1', '-')} / 잔량 {out2.get('bidp_rsqn1', '-')}\n\n"
        f"### 💾 저장\n"
        f"- **raw(JSONL)**: `{raw_path}`\n"
        f"- **normalized(Parquet)**: `{norm_path}`"
    )
    _dispatch("kis-collector", message)
