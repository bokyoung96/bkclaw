# Long Task Progress and Alive Check

## Problem

For long-running work, the user cannot easily tell whether the agent is:
- still working
- blocked
- waiting on an external step
- or dead/stalled

## Rule

For tasks expected to exceed roughly 10 minutes:
1. send a start acknowledgment with the planned stages
2. write at least one mid-task progress update
3. state explicitly whether the task is:
   - IN_PROGRESS
   - BLOCKED
   - WAITING_ON_USER
   - DONE
4. do not stay silent for the whole run unless the user explicitly prefers that

## Progress artifact

Use the helper:

```bash
./bin/progress_note "optional detail text"
```

Environment variables:
- `TASK_NAME`
- `STATUS`
- `STEP`
- `BLOCKER`

This writes:
- `logs/progress/<task>.latest.md`
- `logs/progress/<task>.jsonl`

## Reporting posture

For long tasks, progress should separate:
- current phase
- what finished
- what is still running
- whether a blocker exists
- whether the user must do anything

## Why

This does not create a tqdm bar, but it gives an operator-visible heartbeat for long tasks and reduces ambiguity between slow progress and silent failure.


## Active reporting helper

For tasks where the operator wants proactive status updates in chat, use:

```bash
TARGET=channel:<id> TASK_NAME=my_task STEP="research" INTERVAL_SECONDS=600 ./bin/long_task_watch <command ...>
```

Behavior:
- sends a start message
- sends periodic in-progress messages while the command is alive
- sends DONE or BLOCKED on exit
- also writes `logs/progress/<task>.latest.md` and `.jsonl`

Use this for genuinely long-running work where silence would otherwise look like a stall or crash.
