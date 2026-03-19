---
name: workspace-self-improvement
description: Use when logging mistakes, corrections, recurring failures, feature requests, or operational learnings in this workspace. Especially relevant after errors, user corrections, repeated workflow friction, config/auth failures, or when deciding whether a learning belongs in the retrospective log, AGENTS/TOOLS/SOUL, or a more structured backlog file.
---

# Workspace Self-Improvement

Use this skill to extend the current retrospective system instead of introducing a separate parallel memory silo.

## Purpose

This workspace already has:
- retrospective log entries in `docs/refactor/`
- operating rules in `AGENTS.md`, `TOOLS.md`, `SOUL.md`
- durable memory files under `memory/`

This skill adds structure for:
- errors
- learnings
- feature requests
- promotion rules

## Canonical files

Use `.learnings/` under the workspace repo:
- `.learnings/ERRORS.md`
- `.learnings/LEARNINGS.md`
- `.learnings/FEATURE_REQUESTS.md`

These do **not** replace the retrospective log.
They complement it.

## How to choose where to write

### Use retrospective log when:
- a mistake changed how the assistant should operate in the future
- the lesson has narrative value
- the fix should be understood in context

### Use `.learnings/ERRORS.md` when:
- a command, integration, or automation path failed
- the failure is concrete and reproducible enough to track

### Use `.learnings/LEARNINGS.md` when:
- the user corrected a misunderstanding
- a better pattern was discovered
- a reusable operational insight should be tracked

### Use `.learnings/FEATURE_REQUESTS.md` when:
- the user wants a missing feature or smoother workflow
- a repeated wish should become backlog rather than chat-only memory

## Promotion rules

Promote broadly applicable learnings to:
- `AGENTS.md` for workflow rules
- `TOOLS.md` for tool/integration gotchas
- `SOUL.md` for behavioral principles
- `docs/refactor/` when the result becomes a lasting operational or structural rule

## Minimal logging style

Keep entries short and useful.
Each entry should answer:
- what happened
- why it matters
- what to change

## Anti-sprawl rule

Do not create multiple competing learning systems.
This skill should strengthen the current workspace structure, not fragment it.
