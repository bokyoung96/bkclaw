# Backtest / Result Verification Checklist

## Run Assumptions
- [ ] Strategy name is fixed
- [ ] Universe is fixed
- [ ] Test period is fixed
- [ ] Benchmark is fixed or marked N/A
- [ ] Transaction cost/slippage is fixed
- [ ] Rebalance cadence is fixed
- [ ] Long-only / long-short structure is fixed

## Output Integrity
- [ ] Metrics file exists
- [ ] Chart/image file exists
- [ ] Holdings/output table exists if expected
- [ ] Artifact paths are recorded
- [ ] Timestamps are recorded

## Metric Verification
- [ ] CAGR checked against source
- [ ] Volatility checked against source
- [ ] Sharpe checked against source
- [ ] MDD checked against source
- [ ] Calmar checked against source
- [ ] Win rate checked against source
- [ ] Turnover checked against source

## Interpretation Safety
- [ ] No metric is invented
- [ ] Missing values marked `확인 필요`
- [ ] Strategy explanation matches actual implementation
- [ ] Current holdings summary is based on output, not guesswork

## Delivery Readiness
- [ ] Discord summary block prepared
- [ ] Charts are ready for media upload if requested
- [ ] Completion proof references the same metrics/artifacts
