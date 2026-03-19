from pathlib import Path


def test_root_wrappers_use_repo_entrypoint_helper() -> None:
    root = Path(__file__).resolve().parents[2]
    for name in ["build_gaejae_image", "check_gaejae_db", "restart_gaejae"]:
        content = (root / name).read_text(encoding="utf-8")
        assert "scripts/lib/entrypoint.sh" in content
        assert "run_repo_script" in content
