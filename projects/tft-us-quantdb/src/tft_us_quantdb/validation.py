from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from tft_us_quantdb.config.core import ProjectConfig, UniverseConfig
from tft_us_quantdb.data.adapters import RealQuantDbAdapter
from tft_us_quantdb.data.dataset import DatasetBuilder, rolling_windows


@dataclass(frozen=True)
class ValidationResult:
    name: str
    passed: bool
    detail: str


def _default_config() -> ProjectConfig:
    return ProjectConfig(
        universe=UniverseConfig(
            symbols=(),
            benchmark="SPY-US",
            start_date="2022-01-01",
            end_date="2024-12-31",
        )
    )


def _sample_level_members(panel, target_dates: pd.Index) -> dict[pd.Timestamp, tuple[str, ...]]:
    out: dict[pd.Timestamp, tuple[str, ...]] = {}
    for ts in target_dates:
        row = panel.universe_mask.loc[pd.Timestamp(ts)]
        out[pd.Timestamp(ts)] = tuple(symbol for symbol, is_member in row.items() if bool(is_member))
    return out


def validate_quantdb_pipeline(config: ProjectConfig | None = None) -> list[ValidationResult]:
    cfg = config or _default_config()
    adapter = RealQuantDbAdapter.from_env(cfg)
    builder = DatasetBuilder(config=cfg, adapter=adapter)
    panel = adapter.load_panel_data(list(cfg.universe.symbols), builder.feature_registry)
    window = rolling_windows(cfg)[0]
    batch = builder.build_batch(panel, window.train_slice)

    results: list[ValidationResult] = []

    daily_index_ok = isinstance(panel.universe_mask.index, pd.DatetimeIndex) and panel.universe_mask.index.equals(panel.observed_panel.index)
    results.append(
        ValidationResult(
            name="daily_universe_mask_alignment",
            passed=bool(daily_index_ok),
            detail=f"mask_rows={len(panel.universe_mask)} observed_rows={len(panel.observed_panel)} first={panel.universe_mask.index.min()} last={panel.universe_mask.index.max()}",
        )
    )

    anchor_date = batch.dates[-1]
    expected_symbols = tuple(symbol for symbol, is_member in panel.universe_mask.loc[anchor_date].items() if bool(is_member))
    results.append(
        ValidationResult(
            name="asof_constituent_selection",
            passed=batch.symbols == expected_symbols,
            detail=f"anchor_date={anchor_date.date()} batch_symbols={len(batch.symbols)} expected_symbols={len(expected_symbols)}",
        )
    )

    shape_ok = (
        batch.observed_past.shape[0] == len(batch.symbols)
        and batch.observed_past.shape[1] == cfg.model.context_length + cfg.model.prediction_length
        and batch.known_future.shape[0] == len(batch.symbols)
        and batch.target.shape[0] == len(batch.symbols)
        and batch.target.shape[1] == cfg.model.prediction_length
    )
    results.append(
        ValidationResult(
            name="tensor_shape_consistency",
            passed=bool(shape_ok),
            detail=(
                f"observed={tuple(batch.observed_past.shape)} known={tuple(batch.known_future.shape)} "
                f"target={tuple(batch.target.shape)} static={tuple(batch.static_real.shape)}"
            ),
        )
    )

    prior_date = batch.dates[0]
    anchor_count = int(panel.universe_mask.loc[anchor_date].sum())
    prior_count = int(panel.universe_mask.loc[prior_date].sum())
    no_leakage = set(batch.symbols).issubset(set(panel.universe_mask.columns[panel.universe_mask.loc[anchor_date]]))
    results.append(
        ValidationResult(
            name="no_ever_member_leakage_at_batch_selection",
            passed=bool(no_leakage),
            detail=f"anchor_date={anchor_date.date()} anchor_constituents={anchor_count} prior_date={prior_date.date()} prior_constituents={prior_count}",
        )
    )

    non_empty = (
        batch.observed_past.abs().sum().item() > 0
        and batch.known_future.abs().sum().item() > 0
        and batch.static_real.numel() > 0
    )
    results.append(
        ValidationResult(
            name="feature_panels_populated",
            passed=bool(non_empty),
            detail=f"observed_nonzero={float(batch.observed_past.abs().sum().item()):.2f} known_nonzero={float(batch.known_future.abs().sum().item()):.2f}",
        )
    )

    # sample-level review: each target date T has its own as-of constituent set
    target_dates = pd.DatetimeIndex(batch.dates[-cfg.model.prediction_length :])
    sample_members = _sample_level_members(panel, target_dates)
    distinct_counts = {len(v) for v in sample_members.values()}
    all_equal_to_anchor = all(tuple(v) == batch.symbols for v in sample_members.values())
    varying_membership = len({v for v in sample_members.values()}) > 1
    results.append(
        ValidationResult(
            name="sample_level_asof_sets_computed",
            passed=bool(sample_members) and all(len(v) > 0 for v in sample_members.values()),
            detail=(
                f"sample_dates={len(sample_members)} min_members={min(len(v) for v in sample_members.values())} "
                f"max_members={max(len(v) for v in sample_members.values())} distinct_member_counts={sorted(distinct_counts)[:5]}"
            ),
        )
    )
    results.append(
        ValidationResult(
            name="sample_level_differs_from_single_anchor_batch",
            passed=bool(varying_membership and not all_equal_to_anchor),
            detail=(
                f"anchor_date={anchor_date.date()} anchor_members={len(batch.symbols)} "
                f"sample_level_unique_sets={len({v for v in sample_members.values()})}"
            ),
        )
    )

    return results


def main() -> None:
    results = validate_quantdb_pipeline()
    overall = all(result.passed for result in results)
    print(f"overall={'PASS' if overall else 'FAIL'}")
    for result in results:
        status = 'PASS' if result.passed else 'FAIL'
        print(f"[{status}] {result.name}: {result.detail}")


if __name__ == "__main__":
    main()
