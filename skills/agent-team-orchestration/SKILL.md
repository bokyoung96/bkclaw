---
name: agent-team-orchestration
description: Use when coordinating multiple agent lanes such as orchestrator, research, coding, reviewer, and ops. Especially relevant when deciding which lane should own a task, how handoffs should work, how Tavily/research work should differ from OMX/Codex execution work, or how branch/PR/reporting workflows should be split cleanly.
---

# Agent Team Orchestration

Use this skill when one agent should not do everything.

## Default lanes for this workspace

### 1. Orchestrator lane
- owns routing, priority, and final user report
- owns branch / PR / merge decisions for repo work

### 2. Research lane
- owns Tavily, web search, paper scouting, source shortlist, currentness checks
- is optimized for fast scan / shortlist / freshness

### 3. Deep research lane
- owns multi-source triangulation, long-form synthesis, thesis vs anti-thesis, and uncertainty mapping
- should be used when a basic research pass feels too shallow

### 4. Browser research lane
- supports research/ops when direct page interaction is required
- is not the default first step

### 5. Coding lane
- owns file edits, refactors, scripts, tests, repo layout improvements

### 6. Reviewer lane
- checks merge readiness, regression risk, overclaiming, and missing edge cases
- primary skill: `skills/reviewer-lane/`

### 7. Ops lane
- handles restart checks, Discord sends, git notifications, health/status summaries

## Core task flow

Inbox -> Assigned -> In Progress -> Review -> Done | Failed

## Handoff rules

Every meaningful handoff should say:
- what was done
- where artifacts are
- how to verify
- what remains
- known risks

## Workspace-specific rules

- short-lived branches; merged branches deleted by default
- important git milestones notify the git channel
- root-level clutter should be reduced aggressively
- persona/operating-rule files are protected unless the user explicitly asks to change them


## Recommended deep-research flow

For research-heavy tasks, prefer:

1. Research lane
   - gather shortlist
   - rank source quality
   - identify likely strongest paths

2. Deep research lane
   - expand strongest sources
   - cross-check claims
   - build thesis / anti-thesis
   - translate implications

3. Reviewer lane
   - check overclaiming, missing counterevidence, and weak assumptions when needed
