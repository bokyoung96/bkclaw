#!/usr/bin/env python3
import json
import subprocess
import sys

from src.reporting.channel_targets import resolve_discord_target


def main():
    payload = json.load(sys.stdin)

    if payload.get("action") != "dispatch_discord_message":
        raise SystemExit("invalid action")

    channel_name = payload["channel_name"]
    message = payload["message"]
    target = resolve_discord_target(channel_name)
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
