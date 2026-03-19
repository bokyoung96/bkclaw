from src.reporting.discord_sender import DiscordSendResult


def test_discord_send_result_shape() -> None:
    result = DiscordSendResult(channel_name="dev", target="channel:123", ok=True)

    assert result.channel_name == "dev"
    assert result.target == "channel:123"
    assert result.ok is True
