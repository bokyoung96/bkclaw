# Notice Formatting Failure and Fix

## Problem

A user explicitly asked for a notice-style rewrite, but the response still came back as normal assistant prose.

## Root cause

- The workspace had operating notes about notice channels and preferred labels.
- However, there was no strong versioned skill or hard rule saying that an explicit request like "공지로 정리해줘" must override normal conversational response style.
- Result: the assistant could acknowledge the rule without actually switching output mode.

## Fix

- Added `skills/notice-channel-formatting/`
- Strengthened `skills/discord-channel-actions/` with an anti-failure rule
- Clarified that explicit notice rewrite intent should produce the notice draft directly

## Expected result

When the user explicitly requests a notice rewrite, the assistant should immediately answer in notice format instead of explanatory prose.
