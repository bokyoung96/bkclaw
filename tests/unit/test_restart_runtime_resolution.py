from pathlib import Path


def test_restart_script_resolves_runtime_controller() -> None:
    root = Path(__file__).resolve().parents[2]
    content = (root / 'scripts' / 'restart_and_verify_openclaw.sh').read_text(encoding='utf-8')

    assert 'resolve_compose_file' in content
    assert 'openclaw gateway restart' in content
    assert 'Runtime Controller:' in content
    assert 'COMPOSE_FILE=' in content
