# Skill Integration: Browser Research + Self-Improvement

## Goal

Integrate two useful external skill ideas without introducing redundant clutter.

## Integrated skills

### 1. Browser Research Lane
Source idea: browser automation / page-interaction workflows

Integrated as:
- `skills/browser-research-lane/`

Design choice:
- browser automation is treated as a **conditional research-lane tool**
- Tavily/search remains the default first step
- browser interaction is used only when navigation or UI interaction is necessary

### 2. Workspace Self-Improvement
Source idea: self-improving / learning logs

Integrated as:
- `skills/workspace-self-improvement/`
- `.learnings/ERRORS.md`
- `.learnings/LEARNINGS.md`
- `.learnings/FEATURE_REQUESTS.md`

Design choice:
- this extends the existing retrospective + memory + operating-rule system
- it does not replace the current retrospective log
- it gives concrete places for errors, learnings, and feature requests

## Why this is better than raw installation

- avoids creating a second competing structure for learnings
- avoids making browser automation the default search path
- keeps repo layout aligned with current refactor rules
- preserves the existing operator-facing documentation model

## Follow-up expectation

If these integrations prove useful, they can later be wired into:
- README / operator docs
- Tavily + OMX experiments
- issue and retrospective workflows
