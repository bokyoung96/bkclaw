from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run_legacy_script(script_name: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    python = str(ROOT / ".venv" / "bin" / "python") if (ROOT / ".venv" / "bin" / "python").exists() else sys.executable
    command = [python, str(ROOT / "scripts" / script_name)]
    return subprocess.run(command, cwd=ROOT, env=env, check=True, text=True, capture_output=True)


def load_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
