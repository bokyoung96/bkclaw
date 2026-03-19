import pytest

from src.reporting.channel_targets import resolve_discord_target


def test_resolve_discord_target_known_channel() -> None:
    assert resolve_discord_target("dev").startswith("channel:")


def test_resolve_discord_target_rejects_unknown_channel() -> None:
    with pytest.raises(KeyError):
        resolve_discord_target("unknown-room")
