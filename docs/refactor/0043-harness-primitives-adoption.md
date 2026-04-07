# 0043 — Initial adoption of harness primitives

## Summary

`awesome-harness-engineering`에서 지금 환경에 바로 효용이 큰 프리미티브만 골라,
문서 과증식보다 **체크리스트 / helper / proof template** 위주로 도입한다.

## Adopted first

### 1. Specs / workflow design -> intake lock
- 이미 있던 `quant-team/QUANT_TEAM_ENTRY.md` 와 `INTAKE_GATE_CHECKLIST.md`를 유지
- 큰 작업은 scope lock 질문을 먼저 하도록 canonical anchor와 연결

### 2. Evals / observability -> backtest verification checklist
- 신규: `quant-team/BACKTEST_VERIFICATION_CHECKLIST.md`
- 목적: 성과 요약 전에 assumptions / metrics / robustness / deployability / delivery를 분리 확인

### 3. Constraints / guardrails -> Tavily readiness helper
- 신규: `bin/check_tavily_ready`
- 목적: key/config -> runtime env -> smoke call 순으로 preflight를 고정

## Why these first

현재 반복되는 실제 문제와 바로 연결되기 때문이다.
- Tavily를 preflight 없이 `안 된다`고 말하는 문제
- 백테스트 결과를 검증 부족 상태로 완료처럼 말하는 문제
- 형이 선호하는 questioning/spec-first 작업 방식을 문서에서 실제 운영 artifact로 내리는 문제

## Deferred

다음 단계에서 검토할 것:
- Discord media delivery helper
- completion proof template
- trace/eval log schema
- research verification checklist
