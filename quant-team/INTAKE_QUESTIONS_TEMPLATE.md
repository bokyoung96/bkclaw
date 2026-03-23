# INTAKE_QUESTIONS_TEMPLATE.md

## 목적
형이 `가재야 전략 만들어줘`, `전략 구현해줘` 또는 유사 요청을 했을 때,
첫 응답부터 바로 실행/제안하지 않고 먼저 확인해야 할 질문 세트를 고정한다.

---

## 1) run-policy 먼저 확인
1. 이번에 몇 라운드(iteration)까지 볼까요?
2. 한 라운드에 전략 몇 개까지 볼까요?
3. 중간보고 주기는 어떻게 할까요?
4. 어떤 조건이면 탈락/중단할까요?
5. git 반영 / 보고 채널 범위는 어디까지 볼까요?

## 2) 그 다음 실행 가정 확인
1. 자산군 / 유니버스는 무엇입니까?
   - 예: US equities / KRX large cap / crypto perps

2. 테스트 기간은 어떻게 잡을까요?
   - 예: 2020-01-01 ~ 현재

3. 벤치마크는 무엇으로 둘까요?
   - 예: SPY / BTC / equal-weight universe

4. 거래비용 가정은 어떻게 둘까요?
   - 예: 10bp / 15bp / 20bp
   - crypto면 maker/taker/funding 포함 여부 확인

5. 리밸런싱 주기는 어떻게 할까요?
   - daily / weekly / monthly

6. 전략 구조는 무엇입니까?
   - long-only / long-short / market-neutral

7. 최대 허용 MDD 또는 리스크 제약은 있습니까?

8. 성과 우선 / 실전성 우선 / 단순성 우선 중 무엇이 더 중요합니까?

9. 과최적화 허용도는 어느 정도입니까?
   - 낮음 / 보통 / 높음

10. 최종 산출물 범위는 어디까지입니까?
   - 보고만 / 차트 포함 / git 반영 / merge까지

---

## 응답 템플릿
형, 먼저 이번 라운드 운영 조건부터 잠그겠습니다.

1. iteration / rounds:
2. strategies per round:
3. reporting cadence:
4. stop conditions:
5. git / reporting scope:

그 다음 실행 가정도 같이 확인하겠습니다.

6. 자산군 / 유니버스:
7. 테스트 기간:
8. 벤치마크:
9. 거래비용 가정:
10. 리밸런싱 주기:
11. 전략 구조(long-only / long-short / market-neutral):
12. 최대 허용 MDD 또는 리스크 제약:
13. 성과 우선순위(성과 / 실전성 / 단순성):
14. 과최적화 허용도(낮음 / 보통 / 높음):
15. 최종 산출물 범위(보고 / 차트 / git / merge):

확인되면 그 기준으로 mandate를 잠그고 라운드를 시작하겠습니다.
