---
name: deep-research-lane
description: Use when the user wants more than a quick source shortlist. Especially relevant for deep web research, multi-source triangulation, long-form synthesis, thesis/anti-thesis construction, paper-plus-news cross-checking, implementation implications, and cases where a basic Tavily scan feels too shallow.
---

# Deep Research Lane

Use this skill when quick current-web scanning is not enough.

## Role in the agent structure

- **Primary role**: long-form research synthesis
- **Works after**: research lane shortlist or an explicitly deep research request
- **Not the first step** for simple fact lookup or quick source discovery

## What this lane owns

- multi-source triangulation
- thesis vs anti-thesis construction
- contradiction checks across sources
- paper / blog / news / docs cross-reading
- implementation implications for strategy, tooling, or workflow
- uncertainty mapping

## When to use

Use this lane when:
- the user asks for deep research / 심층 리서치
- the topic needs more than one-pass search
- source quality matters as much as source discovery
- a conclusion must include counterpoints and limitations
- implementation consequences must be translated from research findings

## When not to use

Do not use this lane when:
- the user only wants a quick shortlist
- a fast current-awareness check is enough
- the task is mostly code or repo editing
- browser/Tavily evidence is already sufficient for the decision

## Default workflow

1. Start with a narrow question.
2. Build an initial shortlist via the research lane.
3. Expand only the strongest sources.
4. Cross-check for disagreement.
5. Separate:
   - established facts
   - plausible interpretation
   - open uncertainty
6. Translate findings into operational implications.
7. Return the standard structure:
   - conclusion
   - key evidence
   - source tier
   - risk / uncertainty
   - next action

## Output discipline

Deep research responses should usually include:
- thesis
- counter-thesis / failure case
- strongest supporting sources
- weakest assumption
- what would change the conclusion

## Handoff rule

Typical handoff path:
- Research lane finds sources
- Deep research lane synthesizes and challenges them
- Reviewer lane checks for overclaiming when stakes are high
