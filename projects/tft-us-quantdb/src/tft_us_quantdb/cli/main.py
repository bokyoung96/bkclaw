from __future__ import annotations

from tft_us_quantdb.config.core import ProjectConfig
from tft_us_quantdb.pipeline.rolling import run_quantdb_pipeline


def main() -> None:
    summary = run_quantdb_pipeline(ProjectConfig())
    print("tft-us-quantdb quant-db pipeline complete")
    for result in summary.results:
        print(
            f"window={result.window_index} train_loss={result.train_loss:.4f} "
            f"validation_accuracy={result.validation_accuracy:.4f} "
            f"score_mean_class={result.score_mean_class:.4f} "
            f"n_symbols={result.n_symbols} n_dates={result.n_dates}"
        )


if __name__ == "__main__":
    main()
