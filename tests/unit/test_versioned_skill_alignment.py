from pathlib import Path


def test_versioned_workspace_skills_cover_current_core_operating_areas() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / 'skills' / 'discord-research-workspace' / 'SKILL.md').exists()
    assert (root / 'skills' / 'discord-channel-actions' / 'SKILL.md').exists()
    assert (root / 'skills' / 'agent-team-orchestration' / 'SKILL.md').exists()


def test_discord_skill_mentions_notice_and_git_channels() -> None:
    root = Path(__file__).resolve().parents[2]
    content = (root / 'skills' / 'discord-channel-actions' / 'SKILL.md').read_text(encoding='utf-8')
    assert '1483989656470294548' in content
    assert '1481805554157359327' in content
    assert '**[공지]**' in content
