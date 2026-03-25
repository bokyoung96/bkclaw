from tft_us_quantdb.config.core import ProjectConfig
from tft_us_quantdb.data.dataset import rolling_windows
from tft_us_quantdb.features.registry import FeatureRegistry, FeatureSpec


def test_rolling_windows_exist() -> None:
    config = ProjectConfig()
    windows = rolling_windows(config)
    assert windows
    assert all(window.train_slice.context_length == config.model.context_length for window in windows)


def test_feature_registry_rejects_duplicates() -> None:
    dup = FeatureSpec(name="dup", role=FeatureRegistry.default().features[0].role, domain=FeatureRegistry.default().features[0].domain)
    try:
        FeatureRegistry(features=(dup, dup))
    except ValueError as exc:
        assert "Duplicate feature names" in str(exc)
    else:
        raise AssertionError("Expected duplicate feature names to fail")
