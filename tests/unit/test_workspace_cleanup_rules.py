from pathlib import Path


def test_cleanup_rules_do_not_target_persona_files() -> None:
    root = Path(__file__).resolve().parents[2]
    doc = (root / "docs" / "refactor" / "0005-workspace-cleanup-rules.md").read_text(encoding="utf-8")

    assert "SOUL.md" in doc
    assert "IDENTITY.md" in doc
    assert "USER.md" in doc
    assert "AGENTS.md" in doc
