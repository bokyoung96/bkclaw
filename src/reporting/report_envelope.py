from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReportEnvelope:
    title: str
    bullets: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [self.title]
        if self.tags:
            lines.append(f"- tags: {', '.join(self.tags)}")
        lines.extend(f"- {bullet}" for bullet in self.bullets)
        return "\n".join(lines)
