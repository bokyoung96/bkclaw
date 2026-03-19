from __future__ import annotations

from pathlib import Path
import sys


EXPECTED_ROOT_FILES = {
    ".env.example",
    ".gitignore",
    "AGENTS.md",
    "Dockerfile.gaejae",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "README.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
    "pyproject.toml",
    "requirements.txt",
}

ALLOWED_ROOT_PREFIXES = (
    ".",
    "avatars",
    "bin",
    "dags",
    "docs",
    "memory",
    "scripts",
    "src",
    "tests",
)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    extras: list[str] = []
    for path in root.iterdir():
        name = path.name
        if name == ".git":
            continue
        if path.is_dir():
            if name.startswith(ALLOWED_ROOT_PREFIXES):
                continue
            extras.append(name)
            continue
        if name in EXPECTED_ROOT_FILES:
            continue
        if name.startswith(ALLOWED_ROOT_PREFIXES):
            continue
        extras.append(name)

    if extras:
        print("[workspace-layout] unexpected root entries detected:")
        for entry in sorted(extras):
            print(f"- {entry}")
        return 1

    print("[workspace-layout] ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
