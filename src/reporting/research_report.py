from dataclasses import dataclass


@dataclass
class ResearchReport:
    title: str
    period: str
    result_summary: str
    risk_note: str
    next_action: str

    def to_markdown(self) -> str:
        return (
            f"[research-lab] {self.title}\n"
            f"- period: {self.period}\n"
            f"- result_summary: {self.result_summary}\n"
            f"- risk_note: {self.risk_note}\n"
            f"- next_action: {self.next_action}"
        )
