#!/usr/bin/env python3
import json
import subprocess
import sys

ALLOWLIST = {
    "news-flow": "channel:1481841550299365549",
    "paper-flow": "channel:1481841598185738402",
    "research-lab": "channel:1481841620868530337",
    "dev": "channel:1482514790768447590",
    "kis-collector": "channel:1483695008912638012",
}


def main():
    payload = json.load(sys.stdin)

    if payload.get("action") != "dispatch_discord_message":
        raise SystemExit("invalid action")

    channel_name = payload["channel_name"]
    message = payload["message"]

    if channel_name not in ALLOWLIST:
        raise SystemExit(f"channel not allowed: {channel_name}")

    target = ALLOWLIST[channel_name]
    if target.startswith("channel:REPLACE_"):
        raise SystemExit(f"channel id not configured for: {channel_name}")

    subprocess.run(
        [
            "openclaw",
            "message",
            "send",
            "--channel",
            "discord",
            "--target",
            target,
            "--message",
            message,
            "--json",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
