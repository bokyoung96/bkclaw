# Refactor Principles: Research Workspace

## Why this exists

The current workspace has grown by accretion: scripts, reporting helpers, data-source code,
and ad-hoc operational rules now live side by side. That is normal for a fast-moving research
workspace, but the next phase needs stronger boundaries so new code does not continue to pile
onto the same implicit patterns.

This document defines the rules that future refactors should follow.

## Five-step refactor plan

### Step 1 — Define architectural boundaries
Separate code by responsibility, not by the order in which it was added.

Primary layers:
- `src/common`: environment, runtime context, paths, shared helpers
- `src/backtest`: domain models, strategy registry, output normalization
- `src/data_sources`: integrations with external market/data providers
- `src/reporting`: human-facing summaries, notices, reports
- `src/validation`: checks and validation policies
- `src/workflows`: orchestrated jobs/pipelines
- `scripts/`: thin entrypoints only

Rule:
- Business logic should not live in scripts when it can live under `src/`.

### Step 2 — Encode operating modes explicitly
The workspace already distinguishes between:
- fast experiment mode
- deep validation mode

That distinction must be first-class in code, not just remembered in chat.

Rule:
- runtime mode, run purpose, and execution policy must be declared in a shared runtime object.

### Step 3 — Standardize artifacts
Backtest outputs, plots, tables, validation results, and notes should follow a shared artifact contract.

Rule:
- generated files should have a clear artifact type, canonical relative path, and delivery intent.

### Step 4 — Unify reporting
Developer summaries, progress notes, and research/lab updates should be generated from structured
report objects rather than bespoke string builders.

Rule:
- string formatting should sit at the edge; data should be modeled first.

### Step 5 — Protect the architecture with tests
The workspace needs lightweight guardrails so future additions do not regress into one-off rules.

Rule:
- new shared contracts should have unit tests before more scripts depend on them.

## Working rules

1. Thin scripts, thicker `src/` modules.
2. Shared policy belongs in `src/common` or a domain package, not in chat memory alone.
3. Outputs should be reproducible and traceable to a run directory.
4. Reporting should consume structured models.
5. Every new rule worth remembering should be encoded in code or tests.

## Definition of done for this refactor

A refactor is only "done" when it leaves behind:
- a stable shared abstraction,
- at least one concrete caller using it,
- and tests that make the rule harder to accidentally break.
