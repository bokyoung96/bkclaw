from dataclasses import dataclass


@dataclass
class DevReport:
    experiment_name: str
    status: str
    summary: str
    next_action: str

    def to_markdown(self) -> str:
        return (
            f"[dev] {self.experiment_name}\n"
            f"- status: {self.status}\n"
            f"- summary: {self.summary}\n"
            f"- next_action: {self.next_action}"
        )
