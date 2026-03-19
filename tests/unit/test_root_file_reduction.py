from pathlib import Path


def test_root_operational_wrappers_were_moved_into_bin() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "build_gaejae_image").exists()
    assert not (root / "check_gaejae_db").exists()
    assert not (root / "restart_gaejae").exists()
    assert (root / "bin" / "build_gaejae_image").exists()
    assert (root / "bin" / "check_gaejae_db").exists()
    assert (root / "bin" / "restart_gaejae").exists()


def test_dispatch_script_lives_under_scripts_discord() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "dispatch_discord.py").exists()
    assert (root / "scripts" / "discord" / "dispatch_discord.py").exists()
