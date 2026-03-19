from __future__ import annotations

import os
from pathlib import Path


def load_env_file(path: str | Path) -> None:
    p = Path(path)
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def load_workspace_env(root: str | Path) -> Path:
    root_path = Path(root).resolve()
    env_path = root_path / ".env"
    load_env_file(env_path)
    return env_path
