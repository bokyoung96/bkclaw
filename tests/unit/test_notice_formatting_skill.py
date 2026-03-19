from pathlib import Path


def test_notice_formatting_skill_exists_and_has_hard_rule() -> None:
    root = Path(__file__).resolve().parents[2]
    skill = root / 'skills' / 'notice-channel-formatting' / 'SKILL.md'
    content = skill.read_text(encoding='utf-8')

    assert skill.exists()
    assert '공지로 정리해줘' in content
    assert 'do not' in content.lower()
    assert '**[공지]**' in content
