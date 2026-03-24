---
name: agent-team-orchestration
description: Use when coordinating multiple agent lanes such as orchestrator, research, coding, reviewer, and ops. Especially relevant when deciding which lane should own a task, how handoffs should work, how Tavily/research work should differ from OMX/Codex execution work, or how branch/PR/reporting workflows should be split cleanly.
---

# Agent Team Orchestration

Use this skill when one agent should not do everything.

## Core stance

Treat the operating structure as three separate layers:
1. **agent** = role ownership
2. **mcp / tool capability** = external interaction and execution capability
3. **skills** = workflow and decision policy

Do **not** solve every new capability need by creating another agent.
First ask whether the need belongs to:
- an existing role agent,
- a capability/tool layer,
- or a workflow/skill update.

## Default role map for this workspace

### 1. Coordinator
- `main`
- owns routing, prioritization, and final user-facing report

### 2. Specialists
- `research` → web research, source shortlist, deep synthesis entry
- `reviewer` → quality check, overclaim guard, merge/readiness review
- `backtest` → strategy implementation / experiment / backtest
- `performance-review` → performance interpretation / risk / reporting

### 3. External harness
- ACP
- Codex CLI
- OMX
- exec / shell runtime

These are **execution harnesses**, not specialist roles.

## Tavily rule

Treat Tavily as a **research capability**, not its own agent.
Default classification:
- role owner: `research`
- layer: mcp / tool capability
- policy owner: research-lane / deep-research-lane skills

Only consider a separate Tavily-heavy lane if research becomes long-lived,
thread-bound, or operationally distinct enough to justify a new role.

## Handoff rules

Every meaningful handoff should say:
- what was done
- where artifacts are
- how to verify
- what remains
- known risks

## When to read canonical references

If you need the detailed current structure, read these canonical docs:
- `/home/node/.openclaw/workspace/docs/agents/inventory.md`
- `/home/node/.openclaw/workspace/docs/agents/orchestration.md`
- `/home/node/.openclaw/workspace/docs/agents/discord-entrypoints.md`
- `/home/node/.openclaw/workspace/docs/agents/harness-architecture.md`

Read them when:
- deciding whether to add a new agent,
- checking where Tavily/browser/ACP/Codex belong,
- reasoning about Discord entry points like `/agents` or `/agent_team_orchestration`,
- auditing duplication between docs, runtime state, and skills.

## Workspace-specific reminders
- short-lived branches; merged branches deleted by default
- important git milestones notify the git channel
- persona/operating-rule files are protected unless the user explicitly asks to change them
