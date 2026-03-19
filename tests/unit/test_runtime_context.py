from src.backtest.models import BacktestSpec
from src.common.runtime import resolve_runtime_context


def test_runtime_context_fast_mode_defaults() -> None:
    ctx = resolve_runtime_context(mode="fast", purpose="research", tags=("alpha",))

    assert ctx.mode == "fast"
    assert ctx.purpose == "research"
    assert ctx.policy.validate_strictly is False
    assert ctx.policy.send_dev_notifications is True
    assert ctx.to_dict()["tags"] == ["alpha"]


def test_backtest_spec_embeds_runtime_context() -> None:
    spec = BacktestSpec(
        strategy_name="spy_momentum_top10",
        hypothesis="momentum persists",
        universe="SPY members",
        mode="deep",
    )

    payload = spec.to_dict()

    assert payload["runtime_context"]["mode"] == "deep"
    assert payload["runtime_context"]["purpose"] == "backtest"
    assert payload["runtime_context"]["policy"]["validate_strictly"] is True
