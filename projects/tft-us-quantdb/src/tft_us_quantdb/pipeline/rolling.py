from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn

from tft_us_quantdb.config.core import ProjectConfig
from tft_us_quantdb.data.adapters import RealQuantDbAdapter
from tft_us_quantdb.data.dataset import DatasetBuilder, rolling_windows
from tft_us_quantdb.data.contracts import WindowedBatch
from tft_us_quantdb.features.registry import FeatureRegistry
from tft_us_quantdb.models.tft import TemporalFusionClassifier


@dataclass(frozen=True)
class WindowResult:
    window_index: int
    train_loss: float
    validation_accuracy: float
    score_mean_class: float
    n_symbols: int
    n_dates: int


@dataclass(frozen=True)
class PipelineSummary:
    results: list[WindowResult]


def _train_one_epoch(
    model: TemporalFusionClassifier,
    batch: WindowedBatch,
    *,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    output_dim: int,
) -> float:
    model.train()
    logits = model(batch).logits.reshape(-1, output_dim)
    targets = batch.target.reshape(-1)
    loss = criterion(logits, targets)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return float(loss.item())


def _evaluate_accuracy(model: TemporalFusionClassifier, batch: WindowedBatch) -> float:
    model.eval()
    with torch.no_grad():
        logits = model(batch).logits
        predictions = logits.argmax(dim=-1)
        accuracy = (predictions == batch.target).float().mean().item()
    return float(accuracy)


def _score_mean_class(model: TemporalFusionClassifier, batch: WindowedBatch) -> float:
    model.eval()
    with torch.no_grad():
        logits = model(batch).logits
        scores = torch.softmax(logits, dim=-1)[..., -1].mean().item()
    return float(scores)


def run_quantdb_pipeline(config: ProjectConfig, feature_registry: FeatureRegistry | None = None) -> PipelineSummary:
    registry = feature_registry or FeatureRegistry.default()
    adapter = RealQuantDbAdapter.from_env(config)
    builder = DatasetBuilder(config=config, adapter=adapter, feature_registry=registry)

    results: list[WindowResult] = []
    for window_index, window in enumerate(rolling_windows(config), start=1):
        split = builder.build_split(window)
        model = TemporalFusionClassifier(
            config=config.model,
            static_dim=split.train.static_real.shape[-1],
            known_future_dim=split.train.known_future.shape[-1],
            observed_dim=split.train.observed_past.shape[-1],
        )
        optimizer = torch.optim.Adam(model.parameters(), lr=config.train.learning_rate)
        criterion = nn.CrossEntropyLoss()

        train_loss = 0.0
        for _ in range(config.train.epochs):
            train_loss = _train_one_epoch(
                model,
                split.train,
                optimizer=optimizer,
                criterion=criterion,
                output_dim=config.model.output_dim,
            )
        accuracy = _evaluate_accuracy(model, split.validation)
        score_mean = _score_mean_class(model, split.test)
        results.append(
            WindowResult(
                window_index=window_index,
                train_loss=train_loss,
                validation_accuracy=accuracy,
                score_mean_class=score_mean,
                n_symbols=len(split.train.symbols),
                n_dates=len(split.train.dates),
            )
        )
    return PipelineSummary(results=results)
