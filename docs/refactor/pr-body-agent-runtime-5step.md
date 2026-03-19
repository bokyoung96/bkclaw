## Summary

This PR starts a five-step cleanup of the research workspace so repeated operational behavior is encoded as shared rules instead of remaining scattered across scripts and chat memory.

## What changed

1. Added a five-step architecture/refactor principles document.
2. Added a shared runtime context model for execution mode and purpose.
3. Standardized backtest artifact metadata and artifact manifest generation.
4. Refactored dev reporting toward structured report envelopes.
5. Added guardrail tests and documented refactor rules in the README.
6. Added an ops-focused rule document for credentials/config/repeated runtime issues.

## Why

The workspace has accumulated logic across scripts, reports, backtest outputs, and operational conventions. This PR starts enforcing a cleaner structure around:

- shared runtime mode/policy
- canonical artifact rules
- structured reporting
- lightweight architectural guardrails
- durable handling of recurring config/credential issues

## Key files

- `docs/refactor/0001-architecture-principles.md`
- `docs/refactor/0002-ops-config-and-credential-rules.md`
- `src/common/runtime.py`
- `src/backtest/artifacts.py`
- `src/backtest/output_standardizer.py`
- `src/reporting/report_envelope.py`
- `src/reporting/dev_report.py`
- `src/reporting/dev_notifier.py`
- `tests/unit/test_runtime_context.py`
- `tests/unit/test_artifact_manifest.py`
- `tests/unit/test_dev_reporting.py`
- `tests/unit/test_architecture_guardrails.py`

## Validation

Environment note: `pytest` was not available directly on PATH in the current container, so validation for this phase used Python import/assert smoke checks against the new shared contracts.

## Next steps

Follow-up refactors should continue by:

1. making scripts thinner,
2. centralizing env/config loading,
3. extracting reusable workflow services,
4. standardizing notifications/delivery entrypoints,
5. adding stronger automated test coverage.

## Operations note

This branch now also includes workspace-level ops rules for recurring credential/config issues and helper scripts that load `.env` consistently for git/runtime-sensitive operations.
