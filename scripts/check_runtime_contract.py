from __future__ import annotations

from pathlib import Path
import os
import sys

REQUIRED_ENV_KEYS = [
    "GITHUB_TOKEN",
    "GITHUB_USERNAME",
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    env_file = root / ".env"
    print(f"[runtime-check] root={root}")
    print(f"[runtime-check] env_file_exists={env_file.exists()}")

    missing = [key for key in REQUIRED_ENV_KEYS if not os.getenv(key)]
    if missing:
        print(f"[runtime-check] missing_env={','.join(missing)}")
        return 1

    print("[runtime-check] credential_env=ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
