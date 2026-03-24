# Research File Boundaries

## 목적
`workspace-research`의 핵심 md 파일들이 서로 어떤 역할을 맡는지 명확히 고정한다.
이 문서는 **human-managed canonical boundary note**이며, drift를 줄이기 위한 기준 문서다.

---

## 1. `SOUL.md`
**담당:** 성격 / 가치관 / 응답 태도

여기에 둘 것:
- 근거 우선
- 과장 금지
- 짧고 정확한 톤
- 대답의 기본 태도

여기에 두지 말 것:
- workspace 구조
- 사용자 배경
- tool 운용 절차

---

## 2. `IDENTITY.md`
**담당:** agent 역할 정의

여기에 둘 것:
- 이름
- 역할
- 핵심 책임
- 어떤 종류의 일을 담당하는지

여기에 두지 말 것:
- 세부 운영 절차
- orchestration 책임 배분
- 사용자 선호 상세

---

## 3. `USER.md`
**담당:** 사용자 context / 선호 / 기대 산출물

여기에 둘 것:
- 사용자의 작업 배경
- 선호하는 응답 구조
- 중요하게 보는 출력 형식

여기에 두지 말 것:
- agent persona 정의
- 시스템 구조

---

## 4. `AGENTS.md`
**담당:** 시스템 구조 / lane 규칙 / 운영 discipline

여기에 둘 것:
- workspace scope
- output rule
- quant/reporting override
- git/reporting discipline
- cross-workspace sync note

여기에 두지 말 것:
- 감정적 말투 정의
- persona 서술
- 사용자 취향 설명

핵심 원칙:
- `AGENTS.md`는 **persona file**이 아니라 **system/lane file**이다.

---

## 5. `TOOLS.md`
**담당:** 환경 특화 운영 노트 / tool preflight / 전달 규칙

여기에 둘 것:
- 런타임별 경로
- 미디어 업로드 규칙
- Discord/git 전달 proof 규칙
- Python/shared venv 기준

여기에 두지 말 것:
- agent 역할 정체성
- 사용자 페르소나

---

## 6. `WORKING_RULES.md`
**담당:** 작업 순서 / preflight / repo-vs-research 판단

여기에 둘 것:
- 어떤 작업에서 어떤 폴더를 먼저 볼지
- git preflight 순서
- 도구/연결 preflight 순서

여기에 두지 말 것:
- persona 설명
- tone 설명

---

## 7. `RESEARCH_SCOPE.md`
**담당:** research workspace의 scope / not-scope / posture

여기에 둘 것:
- 이 workspace가 무엇을 위한 곳인지
- 무엇의 기본 홈이 아닌지
- posture의 짧은 요약

여기에 두지 말 것:
- 세부 운영 절차
- 반복되는 reporting rule 상세

---

## 8. Practical rule

짧게 요약하면:
- `SOUL.md` = how to sound
- `IDENTITY.md` = who this agent is
- `USER.md` = who the user is / what they prefer
- `AGENTS.md` = how the lane/system operates
- `TOOLS.md` = env/tool-specific operating notes
- `WORKING_RULES.md` = execution order and preflight
- `RESEARCH_SCOPE.md` = what this workspace is for

---

## 9. Anti-duplication stance

중복을 줄이기 위한 기준:
1. persona 문장은 `SOUL.md` / `IDENTITY.md` 우선
2. 사용자 배경은 `USER.md` 우선
3. 시스템/lane 규칙은 `AGENTS.md` 우선
4. tool/env 노트는 `TOOLS.md` 우선
5. 작업 순서/preflight는 `WORKING_RULES.md` 우선
6. scope 선언은 `RESEARCH_SCOPE.md` 우선
