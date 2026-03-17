# Channel Templates

## Default 4-channel template

### #main
Purpose:
- Main command channel
- Priorities, decisions, direct requests

Startup message:
- This is the main control channel.
- Use this for direct instructions, prioritization, and decisions.
- If research branches out, summaries and decisions should come back here.

### #news-flow
Purpose:
- News, filings, events, macro interpretation

Startup message:
- This channel is for news, filings, and event flow.
- Focus on why the item matters, what to verify, and what the market implication might be.
- Avoid dumping headlines without interpretation.

### #paper-flow
Purpose:
- Paper scouting, summaries, implementation triage

Startup message:
- This channel is for paper discovery and evaluation.
- Classify papers into: worth reading, worth implementing, or park for later.
- Prefer implementation relevance over abstract summary.

### #research-lab
Purpose:
- Hypotheses, signals, strategy ideas, validation planning

Startup message:
- This channel is for strategy and signal research.
- Structure work as hypothesis -> required data -> validation method -> risks.
- Flag weak assumptions early.

## Optional expansion channels

### #backtest-lab
Purpose:
- Code, backtests, audit, execution assumptions

### #data-forge
Purpose:
- Pipelines, schemas, ETL, validation

### #archive
Purpose:
- Distilled conclusions, reusable findings, experiment log
