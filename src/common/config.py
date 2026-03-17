from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class YamlConfigLoader:
    path: Path

    def load(self) -> dict[str, Any]:
        content = self.path.read_text(encoding="utf-8")
        data: dict[str, Any] = {}
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        return data
