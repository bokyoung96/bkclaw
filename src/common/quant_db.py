from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from src.common.env import load_workspace_env


@dataclass(frozen=True)
class QuantDBCredentials:
    user: str
    password: str


def load_quant_db_credentials(root: str | Path) -> QuantDBCredentials:
    load_workspace_env(root)
    user = os.getenv("QUANT_DB_USER")
    password = os.getenv("QUANT_DB_PASSWORD")
    if not user or not password:
        raise RuntimeError("QUANT_DB_USER / QUANT_DB_PASSWORD not found")
    return QuantDBCredentials(user=user, password=password)
