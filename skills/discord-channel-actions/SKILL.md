---
name: discord-channel-actions
description: Use when working with Discord messages, replies, media attachments, git-channel updates, notices/announcements, or channel-targeted operational sends in this workspace. Especially relevant when the user wants something actually visible in Discord, when using reply-to ids, when staging media, or when formatting notice messages with labels like **[공지]** and **[개선]**.
---

# Discord Channel Actions

Use this skill when Discord delivery details matter.

## Core rules

1. Distinguish **current-channel reply**, **cross-session routing**, and **real provider delivery**.
   - current-channel reply = normal reply in the current session
   - `sessions_send` = routing/injection into another session
   - `openclaw message send` = real Discord provider delivery

2. Distinguish **internal inspection** from **real delivery**.
   - `read(image)` is internal inspection only.
   - If the user wants the image/file visible in Discord, use actual message/media sending.

3. Prefer real OpenClaw delivery paths when completion proof matters.
   - Use `openclaw message send` for real sends.
   - For media, use `--media` and confirm success before saying it was sent.
   - Treat `messageId` or actual visible delivery as the strongest completion proof.

4. Respect local media path policy.
   - Files under `workspace-*` may be rejected for upload.
   - Preferred local staging path: `~/.openclaw/media/`

5. Reuse real Discord identifiers.
   - Replies should use the current message id when appropriate.
   - Channel sends should use `channel:<id>` targets.

## Workspace channel defaults

- `dev` → `channel:1482514790768447590`
- `research-lab` → `channel:1481841620868530337`
- `paper-flow` → `channel:1481841598185738402`
- `news-flow` → `channel:1481841550299365549`
- `kis-collector` → `channel:1483695008912638012`
- `git-notify` → `channel:1483989656470294548`
- `notice` → `channel:1481805554157359327`
- notice thread/context → `1484048004779474995`

## Notice formatting

When helping with notices/announcements, prefer:
- **[공지]** 📢
- **[개선]** ✨
- **[점검]** 🛠️
- **[정리]** 🧹
- **[변경]** 🔁

Keep notice titles short, bold, and operational.

If the user explicitly asks for a notice rewrite (for example "공지로 정리해줘"), do **not** answer in regular assistant prose first. Return the notice draft directly.
See also: `skills/notice-channel-formatting/`.

## Delivery completion rules

- Do not treat `sessions_send` ack alone as proof of Discord-visible delivery.
- For git channel and new/unstable channels, prefer direct Discord send when completion proof matters.
- Split reporting into:
  - config changed
  - session routed
  - provider-visible delivery confirmed/unconfirmed

## Git channel formatting

For git operational updates, keep messages short and structured:
- emoji
- branch
- action
- detail
- PR/issue/link when relevant

## When to use

Use this skill for:
- sending charts/images/files into Discord
- replying to a specific Discord message
- deciding whether a file path response is enough or a real upload is needed
- Discord operational notifications and summaries
- formatting notice posts consistently
- checking why a Discord media send failed
