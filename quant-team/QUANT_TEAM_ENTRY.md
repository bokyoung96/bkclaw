# QUANT_TEAM_ENTRY.md

## Canonical Entry Rule

전략 / 백테스트 / 성과 / 탐색 요청은 이 문서를 **quant-team 진입 기준의 단일 canonical entry**로 본다.
다른 문서의 관련 규칙이 흩어져 있더라도, 진입 동작은 이 문서를 우선 적용한다.

## Trigger Phrases

아래 표현 또는 유사 표현이 들어오면 **첫 응답부터 일반 답변 모드로 바로 들어가지 않는다.**
형이 quant-team을 다시 상기시키기 전이라도, 먼저 intake를 수행하고 mandate를 잠근 뒤 round를 시작한다.

- `전략 만들어줘`
- `전략 짜줘`
- `전략 구현해줘`
- `전략 검토해줘`
- `백테스트 해줘`
- `탐색해줘`
- `퀀트팀으로`
- `성과 요약해줘`
- `정리해서 보내줘` (전략/성과 문맥)
- `성과도 같이`
- `성과 요약도 부탁해`

## First-Request Lock

형이 처음 전략 요청을 했을 때부터 이 규칙을 적용한다.
즉, `전략 만들어줘` 같은 첫 요청에 대해:
- 바로 전략 아이디어를 제안하지 않는다
- 바로 feasibility/plan부터 설명하지 않는다
- 먼저 intake 질문으로 진입한다
- 이후 mandate lock을 거쳐서만 round 설계로 넘어간다

## Mandatory Entry Sequence

1. intake questions
2. mandate lock
3. round start
4. milestone reporting
5. review
6. retry / stop / promote 판단

## Intake-First Rule

최소한 아래 항목은 먼저 잠근다.

### 1) run-policy items first
1. iterations / rounds
2. strategies per round
3. reporting cadence / channel
4. stop conditions
5. git scope when relevant

### 2) then execution assumptions
1. universe
2. test period
3. benchmark
4. transaction cost assumptions
5. rebalance cadence
6. structure (long-only / long-short / market-neutral)
7. risk constraints

즉, 첫 응답에서 바로 전략 아이디어나 feasibility 설명으로 들어가지 않고, **이번 라운드 실험 계획표**를 먼저 잠근 뒤 세부 가정으로 내려간다.

## Output Default

전략/백테스트/성과 요청은 기본적으로 아래 우선순위로 정리한다.

1. 전략 정의
2. 데이터 / 유니버스 / 구현 가정
3. 핵심 성과지표
4. 리스크 / 오버피팅 / 실전성 검토
5. 실행 가능한 다음 액션

자유 형식 감상문보다 위 구조를 우선한다.

## Discord / Performance Reporting

Discord 전송용 성과 보고는 `TOOLS.md`의 Backtest / Performance Reporting Rules와
`quant-team/PERFORMANCE_REPORT_TEMPLATE.md`를 따른다.

## Test Checklist After /new

새 세션 또는 새 채널에서 전략 요청 테스트 시 아래를 확인한다.

- 시작 인사가 짧은가
- 내부 절차 설명을 하지 않는가
- 전략 요청에 바로 제안하지 않고 intake부터 시작하는가
- mandate lock을 요구하는가
- quant-team 기준의 구조로 답하는가
- 성과/리스크/다음 액션이 빠지지 않는가
