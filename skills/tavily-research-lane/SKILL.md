---
name: tavily-research-lane
description: Legacy compatibility shim for Tavily-heavy research requests. Use when older workspace references explicitly call this skill, but prefer `research-lane` as the primary research skill. Tavily should usually be treated as a capability choice inside the research lane rather than a standalone top-level lane.
---

# Tavily Research Lane

This skill is retained mainly for backward compatibility.

## Canonical direction
- Primary research skill: `research-lane`
- Tavily: current-web discovery capability inside that lane
- Do not create a separate top-level research lane only because Tavily is the preferred discovery tool

## Use this skill only when
- an existing doc, workflow, or historical reference explicitly points here, and
- you need a reminder that Tavily is a capability decision, not a role boundary

## What to do
1. Read `/home/node/.openclaw/workspace/skills/research-lane/SKILL.md` first.
2. Use Tavily when freshness or richer web discovery matters.
3. Keep Tavily selection as an internal research-lane tool decision whenever possible.

## Readiness reminder
Do not mark Tavily ready only from `.env`. Confirm:
1. key exists
2. active runtime sees it
3. smoke search succeeds

## Anti-duplication note
Detailed Tavily-first workflow should live in `research-lane`, not here.
