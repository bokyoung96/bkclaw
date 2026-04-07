from pathlib import Path

from src.backtest_bridge import build_discord_payload

ROOT = Path(__file__).resolve().parents[2]


def test_build_discord_payload_from_saved_run() -> None:
    payload = build_discord_payload(ROOT / 'outputs' / 'spy_momentum_top10')
    assert payload.metadata['strategy_name'] == 'spy_momentum_top10'
    assert payload.metadata['source_kind'] == 'saved_run'
    assert payload.metadata['attachment_count'] >= 2
    assert '[성과 요약] 📊' in payload.message_markdown
    assert '**전략:** spy_momentum_top10' in payload.message_markdown
