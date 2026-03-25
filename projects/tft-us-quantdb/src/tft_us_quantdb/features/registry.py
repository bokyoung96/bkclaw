from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from tft_us_quantdb.config.core import DataDomain, FeatureRole


@dataclass(frozen=True)
class FeatureSpec:
    name: str
    role: FeatureRole
    domain: DataDomain
    dimension: int = 1
    description: str = ""
    point_in_time: bool = False


DEFAULT_FEATURES: tuple[FeatureSpec, ...] = (
    FeatureSpec(
        "gics_level1_sector",
        FeatureRole.STATIC,
        DataDomain.FUNDAMENTAL,
        description="Latest known GICS sector bucket",
        point_in_time=True,
    ),
    FeatureSpec(
        "gics_level2_industry_group",
        FeatureRole.STATIC,
        DataDomain.FUNDAMENTAL,
        description="Latest known GICS industry group bucket",
        point_in_time=True,
    ),
    FeatureSpec("dow_sin", FeatureRole.KNOWN_FUTURE, DataDomain.MACRO, description="Day-of-week sine"),
    FeatureSpec("dow_cos", FeatureRole.KNOWN_FUTURE, DataDomain.MACRO, description="Day-of-week cosine"),
    FeatureSpec("month_sin", FeatureRole.KNOWN_FUTURE, DataDomain.MACRO, description="Month-of-year sine"),
    FeatureSpec("month_cos", FeatureRole.KNOWN_FUTURE, DataDomain.MACRO, description="Month-of-year cosine"),
    FeatureSpec("close_return_1d", FeatureRole.OBSERVED_PAST, DataDomain.PRICE, description="1-day close return"),
    FeatureSpec("log_dollar_volume", FeatureRole.OBSERVED_PAST, DataDomain.PRICE, description="Log dollar volume"),
    FeatureSpec("log_marketcap", FeatureRole.OBSERVED_PAST, DataDomain.PRICE, description="Log market cap"),
    FeatureSpec("forward_return_bucket", FeatureRole.TARGET, DataDomain.PRICE, description="Forward return bucket"),
)


@dataclass(frozen=True)
class FeatureRegistry:
    features: tuple[FeatureSpec, ...]

    def __post_init__(self) -> None:
        names = [feature.name for feature in self.features]
        dupes = sorted({name for name in names if names.count(name) > 1})
        if dupes:
            raise ValueError(f"Duplicate feature names detected: {dupes}")

    @classmethod
    def default(cls) -> "FeatureRegistry":
        return cls(features=DEFAULT_FEATURES)

    def by_role(self, role: FeatureRole) -> tuple[FeatureSpec, ...]:
        return tuple(feature for feature in self.features if feature.role == role)

    def by_domain(self, domain: DataDomain) -> tuple[FeatureSpec, ...]:
        return tuple(feature for feature in self.features if feature.domain == domain)

    def names(self, features: Iterable[FeatureSpec]) -> tuple[str, ...]:
        return tuple(feature.name for feature in features)

    def total_dimension(self, role: FeatureRole) -> int:
        return sum(feature.dimension for feature in self.by_role(role))
