# Git Channel Notifications

## Goal

Important git operations should be visible in a dedicated Discord channel without spamming the main conversation.

## Channel

- git channel target: `channel:1483989656470294548`

## Rules

Notify this channel when a meaningful git milestone completes:
- branch created for a new refactor cycle
- commit batch completed
- push completed
- PR created
- merge completed
- conflict resolved

## Helper

- `scripts/notify_git_channel.sh`

## Message style

Keep messages short and operational:
- branch name
- action
- PR number/link when relevant
- merge result when relevant
