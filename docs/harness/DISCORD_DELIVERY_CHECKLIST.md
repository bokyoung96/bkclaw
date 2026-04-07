# Discord Delivery Checklist

## Before Send
- [ ] Channel/target is correct
- [ ] Message format matches context (notice / report / backtest / git update)
- [ ] If chart/file must be visible, artifact is staged in allowed media path
- [ ] If long-running task, at least one progress update was already sent

## Send
- [ ] Summary message sent
- [ ] Media attached if requested
- [ ] CLI/API returned success
- [ ] Returned message id / response captured

## After Send
- [ ] Delivery proof recorded in completion proof
- [ ] Final response does not say “sent” unless send succeeded
- [ ] If send failed, failure + retry status is reported separately

## Long Task Reporting
- [ ] Start message sent
- [ ] Mid-progress message(s) sent when task was long
- [ ] Final result message sent without waiting for user to ping again
