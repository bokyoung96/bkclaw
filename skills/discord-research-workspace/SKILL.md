---
name: discord-research-workspace
description: Design, organize, and operationalize a Discord workspace for research workflows. Use when the user wants research-oriented Discord channels, category structure, channel purposes, startup messages, operating rules, or a migration path from one main assistant into multiple channel-based research lanes. Especially relevant for workflows like news monitoring, paper scouting, strategy research, backtesting, data engineering, and archive/knowledge management.
---

# Discord Research Workspace

Create a practical Discord workspace structure for ongoing research work.

## Core workflow

1. Clarify the research operating model.
   - Identify what should stay in the main channel.
   - Separate intake, exploration, implementation, and archive functions.
   - Prefer a small number of channels first.

2. Propose a phased channel structure.
   - Start with the channels that already exist and reflect the real workspace before proposing new ones.
   - Add implementation or archive channels only after the current set proves useful.
   - Prefer channel roles over premature multi-agent splits.

3. Check execution constraints before claiming automation.
   - Verify whether the currently exposed OpenClaw tools/CLI can actually create Discord channels.
   - If direct creation is unavailable, say so plainly.
   - Do not pretend a channel was created when only a plan or message template was produced.

4. Produce ready-to-use outputs.
   - Channel list
   - Purpose for each channel
   - Suggested ordering
   - First pinned/startup message for each channel
   - Operating rules
   - Suggested first tasks to seed the workspace

5. If the user approves implementation, execute what is actually possible.
   - If channel creation is available, create channels carefully and report progress.
   - If not available, hand the user the minimum manual steps and continue with all post-creation setup text.

## Current workspace pattern

Prefer the real current channel structure before proposing a smaller default template.

Current active channels in this workspace include:

- `#main`
  - shared lounge / common space
- `#dev`
  - private dev/debug/ops channel for the user and assistant
- `#news-flow`
  - news, filings, macro/event interpretation
- `#paper-flow`
  - paper scouting, summaries, implementation value triage
- `#research-lab`
  - hypotheses, signal ideas, strategy discussion, experiment design
- `#kis-collector`
  - collector/runtime operational lane
- notice / announcement channels
  - for structured operating notices such as **[공지]** / **[개선]** / **[점검]** / **[정리]** / **[변경]**
- git notification channel
  - short repo operational updates only

If starting from scratch for another user, a 4-channel starter may still be reasonable, but this workspace should be described from its actual current structure first.

## Design rules

- Prefer one main assistant with channel specialization before creating many real OpenClaw agents.
- Treat internal sub-agents as thinking modes unless separate workspaces/routing are clearly needed.
- Keep channel count low when starting fresh, but keep existing useful channels if they already have clear roles.
- Separate collection channels from decision channels.
- Keep notice / announcement channels stylistically consistent.
- Write startup messages so the user can understand each channel instantly.
- For research users, optimize for signal-to-noise, not completeness.

## Output format

When giving a workspace plan, prefer this structure:

- Goal
- Proposed channels
- Purpose of each channel
- Operating rules
- What to seed first
- What not to automate yet
- Next implementation step

## Direct execution constraints

When working inside OpenClaw:

- Check the currently exposed CLI/tooling before saying channel creation is possible.
- If `openclaw message channel` only exposes `list/info`, state that direct creation is not currently available through the exposed interface.
- If actual creation is blocked, still finish the useful work: produce names, descriptions, startup messages, and an operating model.

## Reference files

Read these only when needed:

- `references/channel-templates.md` for reusable channel descriptions and startup messages
- `references/operating-model.md` for phased rollout and migration guidance
