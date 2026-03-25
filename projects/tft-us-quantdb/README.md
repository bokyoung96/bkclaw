# tft-us-quantdb

PyTorch scaffold for a US equities Temporal Fusion Transformer (TFT) workflow with quant DB adapter abstractions.

## What this is

This project re-frames the backbone ideas commonly used in `bokyoung96/Grads SP500/tft`-style equity TFT research into a cleaner, maintainable scaffold for US equities research:

- no runtime dependency on the original repository
- explicit quant DB interfaces instead of direct Excel/parquet coupling
- typed config, schema, feature registry, batch contracts, and rolling-split definitions
- modular model backbone with static context, variable selection, encoder/decoder LSTM, attention, and classifier head
- rolling train/evaluate/score skeleton for research iteration
- future extension path for fundamental data, alternative features, and richer adapters

## Architecture

```text
src/tft_us_quantdb/
  config/     dataclasses + enums for experiment/model/train/universe/rolling config
  data/       adapter protocol, mock adapter, batch slices, dataset builder, rolling windows
  features/   typed feature registry and role/domain contracts with duplicate guards
  models/     TFT-inspired classifier backbone
  pipeline/   rolling train/evaluate/score loop skeleton
  cli/        local demo entry point
```

### Core design choices

1. **Quant DB boundary first**
   - `QuantDbAdapter` defines the contract for loading static, known-future, observed-past, and target tensors.
   - `MockQuantDbAdapter` gives a runnable local demo without production data dependencies.
   - Real DB integrations can implement the same protocol using SQL, Arrow, feature stores, or internal APIs.

2. **Typed research contracts**
   - `ProjectConfig`, `ModelConfig`, `TrainConfig`, `RollingConfig`, `UniverseConfig` use dataclasses.
   - `DataDomain`, `FeatureRole`, `LabelKind` use enums.
   - `FeatureRegistry`, `FeatureSpec`, `BatchSlice`, `WindowedBatch`, and `RollingWindowDefinition` make shape/role assumptions explicit.

3. **Clean TFT backbone, not code lift**
   - The model keeps the conceptual flow:
     - static embedding/context
     - temporal feature projection
     - variable selection
     - LSTM encoder/decoder
     - attention fusion
     - classifier head
   - The implementation is intentionally compact and maintainable rather than a line-for-line port.

4. **Future-proofing for fundamentals**
   - `DataDomain.FUNDAMENTAL` is already part of the feature registry.
   - Static features currently include placeholder sector/size buckets.
   - Feature specs expose a `point_in_time` flag so later PIT joins can be handled intentionally rather than ad hoc.
   - Real adapters can add point-in-time fundamentals or lagged restatement-safe features behind the same contracts.

## Migration / refactor rationale

Compared with a research repo that may tightly couple feature loading to local files and notebook assumptions, this scaffold separates concerns:

- **data access** becomes adapter-driven
- **feature semantics** become registry-driven
- **model logic** stays independent of storage format
- **rolling evaluation** is encoded as a pipeline module rather than ad-hoc notebook cells
- **extension points** are visible up front for productionization or deeper research

This makes it easier to:

- swap parquet/Excel/local files for a quant database
- add fundamentals without rewriting the full model
- test shape contracts with mock data
- keep model code focused on architecture rather than IO

## Extension points

- replace `MockQuantDbAdapter` with a production adapter
- add point-in-time validation rules for fundamentals
- add richer feature metadata such as normalization policy, currency handling, or missing-value handling
- upgrade `BatchSlice` / `RollingWindowDefinition` into trading-calendar-aware range builders sourced from the quant DB
- replace the placeholder training loop with DataLoaders, real rolling splits, metrics, logging, and checkpointing
- add probabilistic heads, quantile outputs, ranking losses, or portfolio construction modules

## Quickstart

### Install

```bash
python -m pip install -e .
```

### Run the mock pipeline

```bash
python -m tft_us_quantdb
# or
python -m tft_us_quantdb.cli.main
# or
`tft-us-quantdb`
```

Expected output is a small rolling-window summary with mock train loss, validation accuracy, and score values.

### Run tests

```bash
pytest
```

## Notes

- This repository is a scaffold, not a finished production strategy.
- The mock adapter intentionally uses synthetic tensors to validate contracts and wiring.
- Rolling windows are currently illustrative year-based slices; real production usage should replace them with actual trading-calendar-aware splits.
