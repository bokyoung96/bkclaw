# Tavily Research Lane

## Goal

Use Tavily as a specialized search lane for current web research without turning every research task into an expensive or noisy workflow.

## Role of Tavily

Tavily should be used when:
- current web coverage matters
- richer search answer mode helps
- quick domain-targeted source gathering is needed
- a research shortlist should be built before deeper reading

## When not to use Tavily

Do not default to Tavily for:
- tiny fact lookups already answered by existing search tools
- full-page deep reading when top snippets are enough
- repetitive high-volume fanout without budget control

## Recommended flow

1. user question enters orchestrator
2. research lane decides whether web_search is enough
3. if richer/current search is needed, use Tavily in balanced mode first
4. return:
   - conclusion
   - evidence
   - source tier
   - risk / uncertainty
   - next action

## Budget posture

Default posture:
- Tavily balanced mode first
- small result count
- fetch only a few pages
- source tiering before expansion

## Artifact policy

Outputs should remain structured:
- markdown report under `reports/`
- raw json under `outputs/`

## Integration note

Tavily belongs to the research lane, not the coding lane.
Coding lane joins only when the research task turns into implementation or prototyping.
