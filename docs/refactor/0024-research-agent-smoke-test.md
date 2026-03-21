# Research Agent Smoke Test

## Goal

Verify that the research lane is operational without mixing up:
- runtime env readiness
- workspace helper availability
- project-local tooling

## Tavily smoke-test rule

A Tavily-backed research lane should be checked in this order:
1. `TAVILY_API_KEY` exists in workspace `.env`
2. active runtime env reflects the same key after restart
3. one small search succeeds

## Reporting rule

When a smoke test has not yet been run, report:
- `key configured`
- `runtime env pending verification`
- `search execution pending`

Do **not** compress that into `Tavily 없음` or `Tavily 안 됨`.

## Runtime verification posture

Before declaring Python / pip / venv / Docker missing, verify in this order:
1. binary exists
2. PATH exposure
3. env injection
4. host vs container path differences
5. whether the limitation is only project-local

## Interpretation

The research agent should prefer precise status language such as:
- `active runtime에서 아직 확인되지 않았다`
- `project-local Docker validation is pending`
- `workspace .venv exists, but this project path has not been validated yet`

This avoids conflating a local project limitation with a whole-runtime absence.
