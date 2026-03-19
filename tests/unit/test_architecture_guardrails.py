from src.backtest.artifacts import CANONICAL_ARTIFACT_SPECS
from src.common.runtime import resolve_runtime_context


def test_canonical_artifact_paths_are_unique_per_source_name() -> None:
    seen: set[tuple[str, str]] = set()
    for source_name, spec in CANONICAL_ARTIFACT_SPECS.items():
        key = (source_name, spec.relative_path)
        assert key not in seen
        seen.add(key)


def test_research_lab_artifacts_are_plots_only() -> None:
    research_lab_specs = [
        spec for spec in CANONICAL_ARTIFACT_SPECS.values() if spec.delivery_intent == "research_lab"
    ]

    assert research_lab_specs
    assert all(spec.kind == "plot" for spec in research_lab_specs)


def test_deep_mode_policy_is_strict() -> None:
    ctx = resolve_runtime_context(mode="deep", purpose="backtest")

    assert ctx.policy.validate_strictly is True
    assert ctx.policy.persist_artifacts is True
