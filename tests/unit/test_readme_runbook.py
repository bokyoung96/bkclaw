from pathlib import Path


def test_readme_mentions_restart_commands_and_bin_layout() -> None:
    root = Path(__file__).resolve().parents[2]
    readme = (root / "README.md").read_text(encoding="utf-8")

    assert "./bin/restart_gaejae" in readme
    assert "./bin/build_gaejae_image" in readme
    assert "openclaw gateway restart" in readme
    assert "channel:1483989656470294548" in readme
