from pathlib import Path


def test_integrated_skills_exist_without_root_sprawl() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / 'skills' / 'browser-research-lane' / 'SKILL.md').exists()
    assert (root / 'skills' / 'workspace-self-improvement' / 'SKILL.md').exists()
    assert (root / '.learnings' / 'ERRORS.md').exists()
    assert (root / '.learnings' / 'LEARNINGS.md').exists()
    assert (root / '.learnings' / 'FEATURE_REQUESTS.md').exists()
