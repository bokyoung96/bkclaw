#!/usr/bin/env python3
import json
import sys

from src.reporting.discord_sender import send_discord_message


def main():
    payload = json.load(sys.stdin)

    if payload.get("action") != "dispatch_discord_message":
        raise SystemExit("invalid action")

    send_discord_message(payload["channel_name"], payload["message"])


if __name__ == "__main__":
    main()
