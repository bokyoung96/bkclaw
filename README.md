# Quant Research Workspace

Python 기반 퀀트 리서치 워크스페이스.

## 목적
- 외부 데이터 적재
- 논문 아이디어 구현
- 백테스트/평가
- dev / research-lab / paper-flow 보고 루프 연결
- Airflow 기반 반복 실행 골격 제공

## 운영 채널
- main: 지시/우선순위
- paper-flow: 논문 intake / 성과 요약 / 구현 가치 평가
- research-lab: 가설 / 실험 설계 / 결과 해석
- dev: 코드 / 디버깅 / 진행상황 / 오류 보고

## 현재 상태
- 프로젝트 골격 생성 완료
- Airflow skeleton 생성 완료
- 실제 데이터 연결 전
- 실제 라이브러리 설치 전

## 다음 단계
1. 데이터 경로 연결
2. 필요한 라이브러리 설치
3. baseline 실험 연결
4. transformer / bayesian 확장

## 운영 명령어
`cd openclaw` 이후 바로 사용할 수 있는 명령:

### 먼저: `.env` 준비
- `~/.openclaw/workspace/.env.example` 를 복사해서 `~/.openclaw/workspace/.env` 생성
- `QUANT_DB_USER`, `QUANT_DB_PASSWORD` 등 credential은 **오직 `.env`에만** 기록
- 앞으로 config/credential 류는 Dockerfile이나 스크립트 본문에 하드코딩하지 않음
- 운영 원칙: 형이 이미 전달한 credential/config 값은 가능하면 가재가 직접 `.env`에 반영하고, 채팅에는 값을 재노출하지 않음

- Dockerfile 기반 가재 이미지 빌드
  - `./build_gaejae_image`
- 전체 재시작 + 검증 + 리포트 저장
  - `./restart_gaejae`
- 퀀트 DB 단독 확인
  - `./check_gaejae_db`
- 현재 환경을 기준 이미지 baseline으로 마킹
  - `./scripts/mark_image_baseline.sh`

### 리포트 위치
- 재시작 리포트: `logs/openclaw_restart_reports/`
- dev 공유용 요약: `logs/openclaw_restart_reports/restart_summary_*.txt`
- 런타임 상태/비교 결과: `logs/openclaw_runtime_state/`

### 이미지 운영 원칙
- `docker commit` 이미지는 그대로 두고, **롤백/스냅샷 용도**로만 사용
- 반복 가능한 운영 기준 이미지는 `Dockerfile.gaejae` + `./build_gaejae_image`로 관리
- 현재 Dockerfile은 **시스템 레벨 의존성**(`cloudflared`)을 재현 가능하게 고정함
- DB id/pw 같은 credential은 **Dockerfile에 넣지 않음**
- workspace `.venv`는 bind mount 구조라 이미지가 아니라 workspace 기준으로 유지됨
- 즉 현재 분리는 이렇게 봐야 함:
  - Dockerfile: cloudflared, 시스템 패키지, OS 레벨 바이너리
  - `.env`: DB 계정/비밀번호, 채널 target, 시간대 같은 설정값
  - workspace: `.venv`, memory, scripts, 연구 코드/데이터

### 이미지 저장 필요 알림 규칙
- `./restart_gaejae` 실행 시 현재 `pip freeze`를 baseline과 비교함
- 차이가 있으면 리포트에 `Image Refresh Needed: YES`로 표시됨
- 새 이미지 저장/검증 완료 후 `./scripts/mark_image_baseline.sh`를 실행해 baseline을 갱신할 것
- 다만 이 비교는 workspace `.venv` 기준이므로, **시스템 패키지 변경**은 Dockerfile 갱신 여부를 별도로 판단해야 함

### dev 채널 전송
- `./restart_gaejae`는 실행 후 dev 요약본을 Discord `channel:1482514790768447590`으로 전송 시도함
- 전송 실패 시 원인은 `logs/openclaw_runtime_state/dev_channel_send_*.log`에 저장됨
- 기본 시간대는 `Asia/Seoul`
- 비활성화: `DEV_CHANNEL_ENABLED=0 ./restart_gaejae`
- 다른 채널로 변경: `DEV_CHANNEL_TARGET=channel:<id> ./restart_gaejae`

### Git 운영
- workspace repo의 기본 작업 브랜치는 `gaejae`
- 가재는 workspace repo에서 직접 수정 및 commit 가능
- push는 형 확인 후 진행
