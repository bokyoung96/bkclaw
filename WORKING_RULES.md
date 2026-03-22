# WORKING_RULES.md

## 폴더 우선 확인 원칙

### 1. 리서치 / 초안 / 웹 조사
먼저 보는 폴더:
- `/home/node/.openclaw/workspace-research`

용도:
- 웹 리서치
- 문서 초안
- 조사 메모
- 임시 분석

### 2. 실제 코드 / git / 운영 반영
먼저 보는 폴더:
- `/home/node/.openclaw/workspace`

용도:
- `bkclaw` 실제 git repo
- branch / commit / push / merge
- 운영 문서 반영
- 실제 코드 수정

## git preflight 원칙
git 작업 요청 시 항상 아래를 먼저 확인한다.
1. repo 루트
2. remote
3. 현재 branch
4. working tree status
5. 필요 시 env / credential 경로
6. 완료 판정은 아래를 각각 분리 확인
   - local commit
   - remote push
   - merge
   - branch cleanup
   - git channel delivery

## quant-team intake 우선 원칙
전략 구현 / 백테스트 / 탐색 요청이 들어오면 일반 답변으로 바로 들어가지 않는다.
특히 아래 표현은 intake-first 트리거로 취급한다.
- `전략 구현해줘`
- `백테스트 해줘`
- `탐색해줘`
- `퀀트팀으로`

이 경우 항상 먼저 아래를 잠근다.
1. universe
2. test period
3. benchmark
4. transaction cost assumptions
5. rebalance cadence
6. structure
7. risk constraints
8. iterations / reporting / git scope / stop conditions

그 뒤에만 mandate lock 및 round 시작을 진행한다.
