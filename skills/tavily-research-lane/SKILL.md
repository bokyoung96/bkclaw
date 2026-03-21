---
name: tavily-research-lane
description: Use when the task is a current-web research question where Tavily should be the primary search lane before deeper reading or coding work. Especially relevant for source shortlisting, recent coverage checks, domain-targeted scans, quick landscape reviews, and research-agent tasks where richer search answer mode is more useful than plain web search alone.
---

# Tavily Research Lane

Use this skill when Tavily should be the first-class research tool.

## Role in the lane model

- **Primary role**: current-web research lane
- **Secondary role**: pre-read shortlist building before browser exploration
- **Not a coding tool**: do not treat Tavily as an implementation lane default

## When to use

Use this skill when:
- current web coverage matters
- a quick source shortlist is needed
- richer answer/snippet mode helps
- domain-targeted scans are useful
- the user wants research-agent style web reconnaissance

## When not to use

Do not use this skill when:
- plain `web_search` is enough
- browser interaction is clearly required from the start
- the task is mostly coding/refactoring
- a local file/codebase answer is already available

## Default workflow

1. Confirm the question belongs to the research lane.
2. Use Tavily first when freshness or richer search context matters.
3. Keep the first pass small:
   - balanced/basic depth first
   - low result count
   - fetch only what is needed
4. Tier sources before expanding.
5. Return the standard research structure:
   - conclusion
   - key evidence
   - source tier
   - risk / uncertainty
   - next action

## Readiness rule

Do not claim Tavily is ready just because `.env` contains `TAVILY_API_KEY`.
Treat Tavily as ready only when all are true:
1. the key exists in workspace `.env`
2. the active runtime env reflects it
3. a small smoke search succeeds

## Integration rule

- Tavily finds.
- Browser exploration confirms.
- Coding/OMX/Ralph starts only after the task turns into implementation.

## Output discipline

When Tavily is used, mention:
- why Tavily was chosen over plain web search
- what query/search angle was used
- what sources were shortlisted
- what remains uncertain
