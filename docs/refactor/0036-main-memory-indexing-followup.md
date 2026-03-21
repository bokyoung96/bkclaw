# Main Memory Indexing Follow-up

## Status

The research memory store indexes normally, but the main memory store still reports:
- Indexed: 0/N files
- Dirty: yes

This remained true even after forcing a main-agent reindex attempt.

## What is already known

- memory source files exist under `workspace/memory/`
- vector/FTS backends are ready
- research agent memory store indexes successfully
- main agent memory store does not complete the same way

## Interpretation

This is no longer a lane-structure issue.
It looks like a main-agent memory indexing/runtime wiring issue that should be debugged separately from the Discord/Tavily/harness refactors.

## Recommended next step

Treat this as a focused follow-up task:
1. inspect main-agent memory/index logs
2. compare main vs research memory workspace resolution
3. verify whether the main agent points at the intended workspace/memory roots during indexing
