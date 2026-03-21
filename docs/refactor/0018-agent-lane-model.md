# Agent Lane Model

## Goal

Define a clean role split for ongoing use of Codex/OpenClaw agents in this workspace.

## Default lanes

### 1. Orchestrator lane
Owns:
- routing
- priority
- branch / PR / merge decisions
- final user report

### 2. Research lane
Owns:
- web research
- paper scouting
- source shortlisting
- Tavily / web search usage
- currentness checks

### 3. Coding lane
Owns:
- file edits
- refactors
- scripts
- tests
- repo structure improvements

### 4. Reviewer lane
Owns:
- merge readiness
- regression checks
- edge-case pushback
- quality gates when changes are meaningful

### 5. Ops lane
Owns:
- restart / health / runtime checks
- Discord operational sends
- git channel notifications
- image/runtime drift checks

## Handoff standard

Every meaningful handoff should include:
- what was done
- where the artifacts are
- how to verify
- what remains
- risks or known gaps

## Branch policy

- one purpose per branch
- merged branches should be deleted by default
- git channel should receive short operational updates at meaningful milestones


## Practical handoff rules

### Research -> OMX handoff
Use this when:
- the question has moved from source discovery to implementation planning
- a shortlist and thesis already exist
- file changes or structured execution are now required

Required handoff payload:
- conclusion / thesis
- shortlisted sources
- implementation target
- verification target
- risks / unknowns

### OMX -> Ralph handoff
Use this when:
- the task requires persistent completion
- retries / verification loops are expected
- a one-shot codex run is likely insufficient

Required handoff payload:
- target outcome
- stop condition / definition of done
- verification steps
- retry expectations
- branch/reporting expectations

### Direct Codex vs OMX
Prefer direct Codex only when:
- the change is narrow
- orchestration overhead would be wasteful
- no persistent execution loop is needed

Prefer OMX when:
- prompt/state/skill composition matters
- the task spans multiple artifacts or steps
- you want a reusable execution wrapper
