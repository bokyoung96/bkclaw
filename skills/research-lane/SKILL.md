---
name: research-lane
description: Unified research lane for fast web scanning, Tavily-led source discovery, deep synthesis, and browser escalation when necessary. Use for current-web research, source shortlisting, paper/blog/news cross-checking, long-form synthesis, and implementation-oriented research translation. This is the default research skill for the workspace.
---

# Research Lane

Use this as the default research skill.

## Role

This skill unifies what used to be split across:
- Tavily-first scanning
- deep research synthesis
- browser follow-up for interactive pages

## Default operating modes

### 1. Quick scan mode
Use when the user wants:
- a fast shortlist
- current awareness
- quick source discovery
- a compact answer

Primary tools:
- Tavily
- normal web search/fetch

### 2. Deep research mode
Use when the user wants:
- 심층 리서치
- deeper evidence
- thesis vs anti-thesis
- stronger implementation implications
- risks and counterarguments

Primary tools:
- Tavily-first shortlist
- selective deep reading
- cross-source comparison

### 3. Browser escalation mode
Use only when:
- search snippets are insufficient
- a docs/app page must be navigated directly
- interaction/screenshot/UI state matters

Browser work is an escalation path, not the default research entry.

## Research workflow

1. Start narrow.
2. Use Tavily first when freshness and richer web context matter.
3. Build a shortlist.
4. Decide whether the task ends as:
   - quick answer
   - deep research synthesis
   - browser escalation
5. Return the standard structure:
   - conclusion
   - key evidence
   - source tier
   - risk / uncertainty
   - next action

## Deep research expectations

When the user explicitly asks for deep research, include when useful:
- thesis
- counter-thesis
- strongest supporting sources
- weakest assumption
- what would change the conclusion
- clean source link list

## Browser rule

Do not start with browser automation by default.
Use it only after Tavily/search/fetch stop being enough.

## Tavily rule

Treat Tavily as the default current-web discovery layer.
Readiness still requires:
1. `.env` key exists
2. active runtime env reflects it
3. smoke search succeeds

## Output discipline

Deep research should be more detailed than quick scan mode.
When possible, keep a clean link section at the end.
