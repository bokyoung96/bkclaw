#!/usr/bin/env python3
import json
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
TRUSTED_USER = "530011557837406218"
TRUSTED_GUILD = "1481805553129750640"
TRUSTED_CHANNELS = {
    "1481805554157359327": "#main",
    "1482514790768447590": "#dev",
    "1484048004779474995": "announcement-thread",
}


def get(d, *path, default=None):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def check(name, ok, actual, expected):
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {name}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    return ok


def main() -> int:
    if not CONFIG_PATH.exists():
        print(f"[FAIL] config missing: {CONFIG_PATH}")
        return 1

    config = json.loads(CONFIG_PATH.read_text())
    checks = []

    checks.append(
        check(
            "agents.defaults.elevatedDefault",
            get(config, "agents", "defaults", "elevatedDefault") == "full",
            get(config, "agents", "defaults", "elevatedDefault"),
            "full",
        )
    )

    checks.append(
        check(
            "tools.elevated.enabled",
            get(config, "tools", "elevated", "enabled") is True,
            get(config, "tools", "elevated", "enabled"),
            True,
        )
    )

    discord_allow = get(config, "tools", "elevated", "allowFrom", "discord", default=[])
    checks.append(
        check(
            "tools.elevated.allowFrom.discord contains trusted operator",
            TRUSTED_USER in discord_allow,
            discord_allow,
            f"contains {TRUSTED_USER}",
        )
    )

    exec_approvers = get(config, "channels", "discord", "execApprovals", "approvers", default=[])
    checks.append(
        check(
            "channels.discord.execApprovals.approvers contains trusted operator",
            TRUSTED_USER in exec_approvers,
            exec_approvers,
            f"contains {TRUSTED_USER}",
        )
    )

    checks.append(
        check(
            "channels.discord.execApprovals.target",
            get(config, "channels", "discord", "execApprovals", "target") == "dm",
            get(config, "channels", "discord", "execApprovals", "target"),
            "dm",
        )
    )

    guild_channels = get(config, "channels", "discord", "guilds", TRUSTED_GUILD, "channels", default={})
    for channel_id, label in TRUSTED_CHANNELS.items():
        checks.append(
            check(
                f"trusted channel allowlist {label} ({channel_id})",
                get(guild_channels, channel_id, "allow") is True,
                get(guild_channels, channel_id),
                {"allow": True},
            )
        )

    if all(checks):
        print("\nTrusted elevated policy is configured durably.")
        print("This does not guarantee every model call succeeds, but it does prove the persistent config path is present.")
        return 0

    print("\nTrusted elevated policy is NOT fully configured.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
