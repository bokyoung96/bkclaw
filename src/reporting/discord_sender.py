from __future__ import annotations

import subprocess
from dataclasses import dataclass

from src.reporting.channel_targets import resolve_discord_target


@dataclass(frozen=True)
class DiscordSendResult:
    channel_name: str
    target: str
    ok: bool


def send_discord_message(channel_name: str, message: str) -> DiscordSendResult:
    target = resolve_discord_target(channel_name)
    if target.startswith("channel:REPLACE_"):
        raise RuntimeError(f"channel id not configured for: {channel_name}")

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
    return DiscordSendResult(channel_name=channel_name, target=target, ok=True)
