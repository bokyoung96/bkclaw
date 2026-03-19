import json
from pathlib import Path

from src.backtest.output_standardizer import copy_standard_outputs


def test_copy_standard_outputs_writes_artifact_manifest(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    run_dir = tmp_path / "run"
    source_dir.mkdir()
    run_dir.mkdir()

    (source_dir / "return_distributions.png").write_text("png", encoding="utf-8")
    (source_dir / "last_holdings.csv").write_text("ticker,weight\nSPY,1.0\n", encoding="utf-8")
    (source_dir / "summary.json").write_text('{"ok": true}', encoding="utf-8")

    copied = copy_standard_outputs(source_dir, run_dir)

    assert "return_distributions.png" in copied
    manifest = json.loads((run_dir / "artifact_manifest.json").read_text(encoding="utf-8"))
    assert [item["name"] for item in manifest] == ["last_holdings", "return_distributions", "raw_summary"]
    assert manifest[0]["delivery_intent"] == "dev"
    assert manifest[1]["delivery_intent"] == "research_lab"
