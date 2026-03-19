from pathlib import Path


def test_git_notify_helper_uses_structured_action_arguments() -> None:
    root = Path(__file__).resolve().parents[2]
    content = (root / "scripts" / "notify_git_channel.sh").read_text(encoding="utf-8")

    assert 'ACTION="${1:-}"' in content
    assert 'BRANCH="${2:-}"' in content
    assert 'DETAIL="${3:-}"' in content
    assert 'push-complete' in content
    assert 'merge-complete' in content
