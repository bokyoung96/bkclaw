---
name: browser-research-lane
description: Legacy compatibility shim for browser-heavy research requests. Use when older workspace references explicitly call this skill, but prefer `research-lane` as the primary skill. Browser choice should usually be made inside `research-lane` as a verification/escalation step, not by treating browser use as its own top-level research lane.
---

# Browser Research Lane

This skill is retained mainly for backward compatibility.

## Canonical direction
- Primary research skill: `research-lane`
- Browser work: verification / escalation step inside that lane
- Do not treat browser usage alone as sufficient reason to create a separate research lane

## Use this skill only when
- an existing doc, workflow, or historical reference explicitly points here, and
- you need a reminder that browser work is a follow-up verification path, not the default search path

## What to do
1. Read `/home/node/.openclaw/workspace/skills/research-lane/SKILL.md` first.
2. Use normal web search/fetch or Tavily before browser escalation unless direct interaction is clearly required from the start.
3. Treat browser evidence as targeted confirmation, navigation, or UI-state inspection.

## Anti-duplication note
Detailed browser-escalation logic should live in `research-lane`, not here.
