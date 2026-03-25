from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence


class DataDomain(str, Enum):
    PRICE = "price"
    MACRO = "macro"
    FUNDAMENTAL = "fundamental"


class FeatureRole(str, Enum):
    STATIC = "static"
    KNOWN_FUTURE = "known_future"
    OBSERVED_PAST = "observed_past"
    TARGET = "target"


class LabelKind(str, Enum):
    MULTICLASS = "multiclass"
    BINARY = "binary"
    REGRESSION = "regression"


@dataclass(frozen=True)
class ModelConfig:
    hidden_size: int = 32
    lstm_layers: int = 1
    attention_heads: int = 4
    dropout: float = 0.1
    context_length: int = 60
    prediction_length: int = 20
    output_dim: int = 3


@dataclass(frozen=True)
class RollingConfig:
    train_years: int = 2
    validation_months: int = 6
    score_months: int = 6
    step_years: int = 1
    max_windows: int = 2


@dataclass(frozen=True)
class TrainConfig:
    batch_size: int = 64
    epochs: int = 1
    learning_rate: float = 1e-3
    seed: int = 7
    rolling: RollingConfig = field(default_factory=RollingConfig)


@dataclass(frozen=True)
class UniverseConfig:
    symbols: Sequence[str] = field(default_factory=lambda: ("AAPL", "MSFT", "NVDA", "AMZN"))
    benchmark: str = "SPY-US"
    start_date: str = "2022-01-01"
    end_date: str = "2024-12-31"


@dataclass(frozen=True)
class QuantDbConfig:
    user_env: str = "QUANT_DB_USER"
    password_env: str = "QUANT_DB_PASSWORD"
    local_host: bool = False
    stock_table: str = "public.daily_adjusted_time_series_data_stock"
    sector_table: str = "public.monthly_time_series_data_stock"


@dataclass(frozen=True)
class ProjectConfig:
    experiment_name: str = "us-equities-tft-quantdb"
    label_kind: LabelKind = LabelKind.MULTICLASS
    model: ModelConfig = field(default_factory=ModelConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    universe: UniverseConfig = field(default_factory=UniverseConfig)
    quant_db: QuantDbConfig = field(default_factory=QuantDbConfig)
