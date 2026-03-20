# Gaejae Retrospective Log

## Goal

Record operational mistakes, misreads, false starts, and recoveries so future work becomes faster, calmer, and less repetitive.

This file is not for blame. It is for pattern recognition.

## How to use

Add entries when one of these happens:
- claimed something was sent/done when it was not actually confirmed
- used the wrong repo / branch / remote
- misread a runtime capability
- forgot an operational rule that should have been encoded
- discovered a recurring failure mode worth turning into code, docs, or tests

## Entry template

```markdown
## YYYY-MM-DD — short title
- Context:
- What went wrong:
- Root cause:
- Fix applied:
- New rule:
- Follow-up hardening:
```

---

## 2026-03-19 — Image send vs internal image read
- Context:
  - The user asked for an image/diagram to be actually visible in Discord.
- What went wrong:
  - The workflow stopped at internal file generation / inspection and I responded as if the image had been attached.
- Root cause:
  - I treated local file existence as equivalent to successful channel delivery.
  - I also underestimated the difference between `read(image)` and real Discord media upload.
- Fix applied:
  - Confirmed that Discord-visible delivery must use `openclaw message send --media`.
  - Confirmed local media must often be staged under `~/.openclaw/media/` because `workspace-*` paths can be rejected.
- New rule:
  - Never say an image/file was sent until the actual send command returns success.
  - `read(image)` is internal inspection only.
- Follow-up hardening:
  - Added Discord/media delivery rules to workspace operating notes and local Discord skill guidance.

## 2026-03-19 — Wrong repo selected for git work
- Context:
  - A refactor was supposed to land in the user's working repo (`bkclaw`).
- What went wrong:
  - I first cloned upstream `openclaw/openclaw` and started planning there.
- Root cause:
  - I inferred the target repo from upstream metadata instead of checking the actual workspace git remote first.
- Fix applied:
  - Located the real workspace repo at `~/.openclaw/workspace` and confirmed its remote was `bokyoung96/bkclaw`.
- New rule:
  - Before repo work, check the real workspace repo / branch / remote first.
  - Do not assume upstream source repo is the intended destination.
- Follow-up hardening:
  - Added repo-aware git helpers, worktree-based refactor flow, and git channel notifications.

## 2026-03-19 — Push failed because env-backed auth was not loaded
- Context:
  - Git push should have worked because credentials already existed in `.env`.
- What went wrong:
  - Push initially failed and I misinterpreted it as missing GitHub auth.
- Root cause:
  - The credential helper depended on `GITHUB_TOKEN`, but the shell/process used for push had not loaded `.env`.
- Fix applied:
  - Loaded `.env`, verified credential helper behavior, and later added shared env-loading helpers and git wrappers.
- New rule:
  - Treat auth failures as two separate questions:
    1. does the credential exist?
    2. is it actually loaded into the current runtime?
- Follow-up hardening:
  - Added env helpers, git push wrapper, GitHub CLI helpers, and documentation.

## 2026-03-19 — PR automation blocked by token scope mismatch
- Context:
  - Git push worked, but `gh pr create` failed.
- What went wrong:
  - I had working repo auth for push but not enough GitHub API permission for PR creation.
- Root cause:
  - The personal access token had insufficient GraphQL/PR write permission for `createPullRequest`.
- Fix applied:
  - Replaced the token with one that supports repository contents + pull request write access.
- New rule:
  - Verify both git transport auth and GitHub API/GraphQL auth when introducing `gh` automation.
- Follow-up hardening:
  - Added `gh` helpers and repo-specific GitHub CLI automation docs.

## 2026-03-19 — Layout assumptions need executable checks
- Context:
  - Repository cleanup reduced root clutter, but intended structure could drift again later.
- What went wrong:
  - Layout expectations remained mostly implicit until a self-check was added.
- Root cause:
  - Structural cleanliness was documented, but not yet enforced by a quick executable check.
- Fix applied:
  - Added `scripts/check_workspace_layout.py` and documented allowed root directories.
- New rule:
  - If a cleanup rule matters operationally, encode it as a helper or test.
- Follow-up hardening:
  - Keep the layout check updated when the intended root structure evolves.

## 2026-03-19 — Memory quota failure needs an explicit ops breadcrumb
- Context:
  - Prior-decision recall was needed during live Discord troubleshooting and issue follow-up.
- What went wrong:
  - `memory_search` failed during the session, forcing manual fallback through transcripts and repo files.
- Root cause:
  - The embeddings backend hit quota exhaustion (`429 insufficient_quota`), so memory recall was unavailable even though the rest of the runtime was still alive.
- Fix applied:
  - Logged the failure as an explicit operational dependency issue and continued with manual fallback.
- New rule:
  - Treat memory recall outages as first-class ops incidents: record them, keep a manual fallback path, and avoid assuming prior-state recovery is available.
- Follow-up hardening:
  - Add a durable error/feature tracking entry so future debugging starts with provider quota/billing verification.

## 2026-03-20 — Tool/runtime preflight must happen before claiming something is missing
- Context:
  - Live Discord work exposed repeated failures around Tavily, GitHub CLI / git auth, and research performance-report formatting.
- What went wrong:
  - I said tools were unavailable or work could not proceed before checking the current runtime properly.
  - After the user reminded me that Tavily keys, `gh`, and git token setup already existed, I then confirmed they were in fact configured or recoverable.
  - I also drifted away from the agreed research-lab performance summary/reporting format and improvised output instead of following the established template.
- Root cause:
  - I treated the first negative signal in the current shell as ground truth instead of separating:
    1. installation/runtime visibility,
    2. PATH exposure,
    3. token/env injection,
    4. host vs container path differences,
    5. existing skills / operating rules,
    6. existing reporting format requirements.
  - I also allowed response speed and ad-hoc phrasing to override the saved operating format.
- Fix applied:
  - Added startup verification rules so `gh`, Tavily, and token-backed tools are checked first after Docker restart / new session / runtime reset.
  - Restored memory-search functionality through the Ollama embedding provider path.
  - Hardened Ollama bootstrap/install path handling so recall does not silently break on next restart.
  - Recommitted to the fixed research/backtest/performance reporting template instead of ad-hoc formatting.
- New rule:
  - Never tell the user a previously-provisioned tool is missing until runtime visibility, PATH, env/token presence, host/container path differences, and related skills/config have all been checked.
  - Never improvise the research-lab performance summary format when an agreed template/rule already exists.
  - When uncertain, report `현재 런타임에서 아직 확인되지 않았습니다` first, then verify.
- Follow-up hardening:
  - Keep preflight checks ahead of conclusion statements.
  - Keep reporting format checks ahead of writing performance summaries.
  - Treat recurrence of this class of mistake as a process failure, not a one-off slip.
