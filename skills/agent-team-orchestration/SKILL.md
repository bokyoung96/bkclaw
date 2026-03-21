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
- owns Tavily, web search, source shortlist, deep synthesis, and browser escalation
- primary skill: `skills/research-lane/`
- runs in quick scan mode by default, then deepens only when needed

### 3. Coding lane
- owns file edits, refactors, scripts, tests, repo layout improvements

### 4. Reviewer lane
- checks merge readiness, regression risk, overclaiming, and missing edge cases
- primary skill: `skills/reviewer-lane/`

### 5. Ops lane
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




## Recommended research flow

1. Research lane starts in quick scan mode.
2. If the question needs more depth, the same research lane escalates into deep research mode.
3. Browser work is used only if direct interaction is required.
4. Reviewer lane challenges the conclusion when confidence/risk is high.
