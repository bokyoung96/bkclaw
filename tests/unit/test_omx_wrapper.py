from pathlib import Path


def test_omx_wrapper_exists_in_bin() -> None:
    root = Path(__file__).resolve().parents[2]
    wrapper = root / "bin" / "omx"
    content = wrapper.read_text(encoding="utf-8")

    assert wrapper.exists()
    assert "oh-my-codex" in content
    assert "node bin/omx.js" in content
