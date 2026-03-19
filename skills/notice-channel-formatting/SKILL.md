---
name: notice-channel-formatting
description: Use when the user wants a message rewritten for a notice/announcement channel, especially in Discord notice contexts. Trigger strongly on phrases like "공지로 정리해줘", "공지문으로", "공지 채널용으로", or when drafting/revising content for notice channel `1481805554157359327` or related thread/context `1484048004779474995`.
---

# Notice Channel Formatting

Use this skill when a message should be transformed into a notice-style output rather than answered conversationally.

## Hard rule

If the user explicitly asks to:
- 공지로 정리해줘
- 공지문으로 바꿔줘
- 공지 채널용으로 써줘
- 개선 공지로 정리해줘

then **do not** reply in normal assistant prose first.
Output the notice draft directly.

## Preferred labels

Use bold labels with emoji:
- **[공지]** 📢
- **[개선]** ✨
- **[점검]** 🛠️
- **[정리]** 🧹
- **[변경]** 🔁

## Selection rule

- Use **[공지]** for announcements, notices, guidance, and broad updates
- Use **[개선]** for improvements, refactors, better flows, UX/workflow upgrades
- Use **[점검]** for checks, temporary downtime, validation, inspection status
- Use **[정리]** for cleanup, restructuring, simplification, archival work
- Use **[변경]** for behavior/config/policy changes

## Output shape

Default notice structure:
1. bold label + emoji + short title
2. 2-5 short bullets or paragraphs
3. concise operational next step if relevant

## Anti-failure rule

If the user asked for a notice rewrite, the response should visibly look like a notice at first glance.
It should not look like a normal chat answer.

## Channel context

Treat these as notice contexts:
- `1481805554157359327`
- `1484048004779474995`
