from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


RunMode = Literal["fast", "deep"]
RunPurpose = Literal["research", "backtest", "collector", "reporting"]


@dataclass(frozen=True)
class RuntimePolicy:
    validate_strictly: bool
    send_dev_notifications: bool
    persist_artifacts: bool

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeContext:
    mode: RunMode
    purpose: RunPurpose
    actor: str = "gaejae"
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def policy(self) -> RuntimePolicy:
        if self.mode == "deep":
            return RuntimePolicy(
                validate_strictly=True,
                send_dev_notifications=True,
                persist_artifacts=True,
            )
        return RuntimePolicy(
            validate_strictly=False,
            send_dev_notifications=True,
            persist_artifacts=True,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "purpose": self.purpose,
            "actor": self.actor,
            "tags": list(self.tags),
            "policy": self.policy.to_dict(),
        }


def resolve_runtime_context(
    mode: RunMode = "fast",
    purpose: RunPurpose = "research",
    *,
    actor: str = "gaejae",
    tags: tuple[str, ...] = (),
) -> RuntimeContext:
    return RuntimeContext(mode=mode, purpose=purpose, actor=actor, tags=tags)
