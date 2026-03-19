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

## 2026-03-19
- Context:
  - Memory lookup was needed for prior decisions and todo recall during live Discord operations.
- Failure:
  - `memory_search` was unavailable because the embeddings backend returned quota exhaustion (`429 insufficient_quota`).
- Suspected cause:
  - The configured embeddings provider had no remaining quota / billing headroom.
- Fix / next step:
  - Track this as an operational dependency failure, keep manual fallback via session history + repo docs, and later verify provider/billing or switch embeddings backend.
- Status: pending
