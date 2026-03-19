# ERRORS

Track concrete failures that are worth revisiting.

## Template
- Date:
- Context:
- Failure:
- Suspected cause:
- Fix / next step:
- Status: pending | resolved | promoted

## 2026-03-19
- Context:
  - Investigating trusted elevated policy / issue #16 while searching the workspace from chat.
- Failure:
  - A broad grep ran into `.venv` and produced a huge noisy result, which made diagnosis slower and increased the chance of session/tool instability.
- Suspected cause:
  - Search scope was too wide and not repo-aware enough.
- Fix / next step:
  - Prefer `git grep` or explicit excludes for `.venv`, external dependencies, and generated outputs when doing issue diagnosis.
- Status: resolved
