---
name: browser-research-lane
description: Use when web work requires direct page interaction rather than search snippets alone. Especially relevant for docs sites, app dashboards, authenticated web UIs, form-driven exploration, click/scroll/snapshot workflows, and cases where Tavily/search results are not enough. This skill is a browser-exploration complement to the research lane, not a replacement for Tavily or normal web search.
---

# Browser Research Lane

Use this skill to absorb the useful parts of agent-browser into the current workspace without turning browser automation into the default search path.

## Role in the lane model

- **Primary role**: research-lane support
- **Secondary role**: ops-lane support for UI verification
- **Not the default**: do not start with browser automation when Tavily or normal web search is enough

## When to use

Use this skill when:
- a docs site must be navigated interactively
- a site has search/filter UI that must be operated directly
- the answer depends on clicking through live pages
- screenshots/snapshots of current UI state matter
- an authenticated dashboard or app UI must be inspected

## When not to use

Do not use this skill when:
- Tavily/web search already gives enough high-quality results
- a quick source shortlist is all that is needed
- the task is primarily code or repo work
- deep browser interaction would be overkill

## Default workflow

1. Start with Tavily or normal web search.
2. Build a shortlist of likely pages.
3. Only escalate to browser exploration if interaction is required.
4. Capture the minimum browser-derived evidence needed.
5. Return to the normal response structure:
   - conclusion
   - key evidence
   - source tier
   - risk / uncertainty
   - next action

## Integration rule

Treat browser automation as a **follow-up tool**, not the first tool.
Tavily finds. Browser exploration confirms or navigates.

## Output discipline

When browser work is used, mention:
- which page(s) were explored
- what interaction was required
- what was learned that search snippets alone did not reveal

## Cleanup principle

Do not let browser-specific notes or one-off commands sprawl across the repo root.
Any stable browser workflow should live in a skill, helper script, or docs reference.
