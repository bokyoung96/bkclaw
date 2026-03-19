import os
from pathlib import Path

from src.common.quant_db import load_quant_db_credentials


def test_load_quant_db_credentials_reads_from_workspace_env(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("QUANT_DB_USER=tester\nQUANT_DB_PASSWORD=secret\n", encoding="utf-8")
    os.environ.pop("QUANT_DB_USER", None)
    os.environ.pop("QUANT_DB_PASSWORD", None)

    creds = load_quant_db_credentials(tmp_path)

    assert creds.user == "tester"
    assert creds.password == "secret"
