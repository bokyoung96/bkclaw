DISCORD_CHANNEL_ALLOWLIST = {
    "news-flow": "channel:1481841550299365549",
    "paper-flow": "channel:1481841598185738402",
    "research-lab": "channel:1481841620868530337",
    "dev": "channel:1482514790768447590",
    "kis-collector": "channel:1483695008912638012",
}


def resolve_discord_target(channel_name: str) -> str:
    try:
        return DISCORD_CHANNEL_ALLOWLIST[channel_name]
    except KeyError as exc:
        raise KeyError(f"channel not allowed: {channel_name}") from exc
