import os
from pathlib import Path

from src.common.env import load_env_file, load_workspace_env


def test_load_env_file_sets_missing_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("ALPHA=1\nBETA=two\n", encoding="utf-8")

    os.environ.pop("ALPHA", None)
    os.environ.pop("BETA", None)
    load_env_file(env_file)

    assert os.environ["ALPHA"] == "1"
    assert os.environ["BETA"] == "two"


def test_load_workspace_env_returns_env_path(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("GAMMA=3\n", encoding="utf-8")

    os.environ.pop("GAMMA", None)
    resolved = load_workspace_env(tmp_path)

    assert resolved == env_file.resolve()
    assert os.environ["GAMMA"] == "3"
