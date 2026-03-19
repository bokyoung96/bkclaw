import os
import subprocess
import sys
from pathlib import Path


def test_runtime_contract_script_succeeds_with_required_env() -> None:
    root = Path(__file__).resolve().parents[2]
    script = root / "scripts" / "check_runtime_contract.py"
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = "test-token"
    env["GITHUB_USERNAME"] = "test-user"

    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, env=env)

    assert result.returncode == 0
    assert "credential_env=ok" in result.stdout
