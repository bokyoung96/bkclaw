from pathlib import Path


def test_restart_script_resolves_runtime_controller() -> None:
    root = Path(__file__).resolve().parents[2]
    content = (root / 'bin' / 'restart_gaejae').read_text(encoding='utf-8')

    assert 'resolve_compose_file' in content
    assert 'OPENCLAW_IMAGE' in content
    assert 'docker compose down' in content
    assert 'docker compose up -d' in content
