# DEFAULT_RUN_POLICY.md

## 목적
형이 `가재야 ~ 전략 구현해줘`라고 요청했을 때 적용할 기본 실행 정책을 고정한다.

---

## 기본 실행 정책
### 보고
- 중간 보고 채널: `<#1481841620868530337>`
- 보고 빈도: `milestone only`
- 보고 상태는 가능하면 `전송 시도 / 전달 확인`을 분리 기록

### git
- 로컬 commit: 자동
- push: 자동
- merge: 자동
- 단, 아래 조건을 만족할 때만 merge 허용:
  - success criteria 충족
  - fitting severe 없음
  - risk veto 없음
  - trader / execution realism에서 최소 hold 이상

### 성공 기준
- turnover는 기본 성공 기준에서 제외
- 기본 검토 축:
  - Sharpe
  - MDD
  - robustness
  - fitting warning
  - deployability

### 라운드 / 종료
- 라운드: 원칙상 계속 가능
- 단, 세션 토큰 사용량이 50% 이상이면 자동 종료 및 중간 정리
- 종료 시 남길 것:
  - 현재 최고 후보
  - 마지막 round 상태
  - 다음 재개 포인트

---

## 실행 전 필수 확인 질문
전략 요청 시 아래를 먼저 확인한다.
1. 자산군 / 유니버스
2. 테스트 기간
3. 벤치마크
4. 거래비용 가정
5. 리밸런싱 주기
6. long-only / long-short / market-neutral
7. 최대 허용 MDD 또는 리스크 제약
8. 실전성 vs 성과 우선순위
9. 과최적화 허용도
10. 최종 산출물 범위

---

## 문서 연결
- 팀 명세: `QUANT_TEAM_SPEC.md`
- 역할 프롬프트: `ROLE_PROMPTS.md`
- 실행 절차: `RUNBOOK.md`
- 실행 템플릿: `EXECUTION_TEMPLATE.md`
- 성과 리뷰 정책: `PERFORMANCE_REVIEW_POLICY.md`
- 성과 보고 템플릿: `PERFORMANCE_REPORT_TEMPLATE.md`
