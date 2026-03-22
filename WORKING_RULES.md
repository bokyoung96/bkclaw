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
전략 구현 / 백테스트 / 탐색 / 성과 요약 요청의 canonical entry는 `quant-team/QUANT_TEAM_ENTRY.md`를 따른다.
이 경우 일반 답변으로 바로 들어가지 않고, 해당 문서 기준으로 intake → mandate lock → round 시작 순서를 적용한다.
