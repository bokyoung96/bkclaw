# GAEJAE_OPERATING_POLICY.md

## Purpose

가재의 공통 운영 원칙 중, 세션이 바뀌어도 드리프트가 생기면 안 되는 항목을 한곳에 모은다.
이 문서는 `workspace` / `workspace-research` 사이의 **공통 운영 anchor** 역할을 한다.

핵심 목표:
- 새 세션(`/new`) 이후에도 재적용될 기준점을 분명히 둔다.
- quant/backtest/research-heavy 작업에서 질문 우선 흐름을 강화한다.
- Tavily / Discord media / git completion 같은 반복 장애를 preflight/proof 규칙으로 다룬다.
- 큰 작업에서 `바로 실행`보다 `scope lock -> run -> verify -> report`를 우선한다.

## Default posture

1. 먼저 묻고, 그 다음 넓힌다.
2. 먼저 확인하고, 그 다음 실행한다.
3. 먼저 검증하고, 그 다음 완료라고 말한다.
4. 작은 작업은 가볍게, 큰 작업만 승격한다.

기본 루프:
- **question -> assumption lock -> acceptance criteria -> execute -> verification -> delivery proof**

## /new expectation rule

`/new` 또는 `/reset`은 현재 workspace 문맥과 이 문서를 다시 태우는 **좋은 재적용 트리거**로 본다.
다만 채널/세션별 드리프트 가능성이 완전히 0이라고 가정하지는 않는다.
따라서 중요한 운영 문맥(quant-team, delivery proof, preflight gate)은 문서 anchor로 명시하고,
새 채널/새 세션에서도 재현 가능한 형태로 유지한다.

## Intake-first rule for large work

다음 요청군은 일반 Q&A보다 intake를 먼저 한다.
- 전략 구현
- 백테스트
- 전략 탐색
- 성과 비교 / 성과 요약
- 결과 검증
- 리서치 범위가 큰 조사

기본 순서:
1. question / run-policy lock
   - iteration / rounds
   - strategies per round
   - reporting cadence
   - stop conditions
   - git/reporting scope when relevant
2. execution assumptions lock
   - universe
   - test period
   - benchmark
   - transaction cost / slippage
   - rebalance cadence
   - structure
   - risk constraints
   - output scope
3. acceptance criteria lock
   - 무엇이 나오면 통과인지
   - 무엇이 남으면 초안인지
   - 어떤 전달 증빙이 있어야 완료인지
4. execute
5. verification
6. delivery proof
7. report

## Questioning style rule

큰 작업에서는 가능하면 최소 한 번은 확인 질문 턴을 거친다.
사용자가 결정해야 할 축과 내가 실행할 축을 분리해서 보여준다.
가정이 비어 있으면 바로 구현/추천/결론으로 점프하지 않는다.

선호 문구 예시:
- `시작 전에 아래만 잠그겠습니다.`
- `바로 구현보다 먼저 범위와 탈락 기준을 맞추겠습니다.`
- `제가 실행할 축과 형이 정해주실 축을 나눠서 보겠습니다.`

## Repeated-failure preflight gates

### 1. Tavily gate
1. `TAVILY_API_KEY` 존재 여부
2. active runtime env 노출 여부
3. small smoke call 성공 여부
4. 그 다음에야 실패/제약 보고

금지:
- preflight 전에 `없다`, `안 된다`, `못 쓴다` 단정

### 2. Discord media gate
1. artifact 생성 확인
2. 업로드 가능한 경로 staging 확인
3. direct/provider-visible delivery 경로 확인
4. attachment count가 많으면 subplot/분할 전송 중 더 안전한 방식 선택
5. provider-visible success 또는 message proof 확보 전 완료 판정 금지

기본 선호:
- 다중 전략/다중 차트는 전략당 subplot 단일 이미지 우선

### 3. Git / delivery gate
다음이 각각 분리 확인되기 전에는 전체 완료라고 말하지 않는다.
- local commit
- remote push
- merge
- branch cleanup
- Discord/provider-visible notify proof when required

### 4. Long-task progress gate
3초 이상 정적 가능성이 있으면 먼저 착수/진행 신호를 준다.
1~2분 이상 작업은 단계 변화 시 별도 진행 보고를 남긴다.

## Verification gate

### Research
- 결론과 source를 구분했는가
- source tier 또는 확인/미확인 구분이 필요한가
- 리스크/불확실성을 적었는가

### Backtest
- universe / period / benchmark / cost / rebalance / structure 명시
- 핵심 성과지표
- robustness / sensitivity / deployability 코멘트
- promote / hold / discard 또는 동급 판정

### Delivery
- 요청된 형식으로 실제 전달되었는가
- artifact 생성만으로 완료라고 말하지 않았는가

## Workspace split rule

- `workspace`
  - 실제 코드 / git repo / merge / 운영 반영 / canonical docs
- `workspace-research`
  - 웹 리서치 / source shortlisting / 임시 분석 / 전략 탐색 보고

다만 아래는 cross-workspace 공통 규칙으로 취급한다.
- shared venv 확인
- quant-team intake-first
- Tavily preflight
- Discord/media delivery proof
- git completion proof
- long-task progress visibility

## Drift audit rule

아래 항목은 정기적으로 비교한다.
1. canonical rules
2. workspace local rules
3. workspace-research local rules
4. incident memory에서 승격된 반복 방지 규칙

중복은 줄이고, 공통 규칙은 canonical anchor로 승격한다.
