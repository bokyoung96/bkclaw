# Quant Research Workspace

Python 기반 퀀트 리서치 워크스페이스이자, 가재(OpenClaw 기반 연구 에이전트)의 운영 저장소다.

이 저장소는 단순 코드 모음이 아니라 아래 세 가지를 함께 관리한다:
- 퀀트 리서치/백테스트 코드
- OpenClaw 운영 스크립트 및 Docker 런타임 규칙
- Discord/GitHub 연동을 포함한 실제 운영 절차

---

## 1. Workspace 목적

이 저장소는 다음 용도를 가진다:
- 외부 데이터 적재
- 논문 아이디어 구현
- 백테스트/평가
- dev / research-lab / paper-flow 보고 루프 연결
- OpenClaw 기반 연구 에이전트 운영
- Docker rebuild 이후에도 반복 가능한 운영 상태 유지

---

## 2. Repository layout

루트는 가능한 한 **프로젝트 정의와 운영 규칙**만 남기고, 실행 파일은 하위 폴더로 정리한다.

### Top-level philosophy
- `bin/` → 사람이 직접 치는 운영 명령
- `scripts/` → 구현용 스크립트
- `src/` → 재사용 가능한 Python 로직
- `docs/refactor/` → 리팩토링 규칙과 운영 원칙
- 루트 → README, Dockerfile, `.env.example`, persona/operating-rule 파일

### Important directories
- `bin/`
  - `build_gaejae_image`
  - `check_gaejae_db`
  - `restart_gaejae`
- `scripts/`
  - build / restart / validation / git / gh / notify helpers
- `scripts/discord/`
  - Discord operational dispatch entrypoints
- `src/`
  - backtest / reporting / data_sources / workflows / common
- `docs/refactor/`
  - refactor principles, cleanup policy, git notification rules, docker runtime rules

---

## 3. Protected files

아래 파일들은 **cleanup 대상이 아니다**. 이 파일들은 가재의 정체성/운영 규칙에 해당한다.

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `TOOLS.md`

정리 원칙:
- 불필요한 operational clutter는 줄인다
- 그러나 persona / operating-rule 파일은 사용자의 명시적 요청 없이는 건드리지 않는다

---

## 4. Environment and credentials

### `.env` 원칙
- credential/config 값은 `.env`에서 관리
- Dockerfile, shell script 본문, 채팅 본문에 하드코딩하지 않음
- 형이 전달한 비밀값은 가능하면 가재가 직접 `.env`에 반영하고, 채팅에는 재노출하지 않음

### 주요 환경변수 예시
- `QUANT_DB_USER`
- `QUANT_DB_PASSWORD`
- `GITHUB_USERNAME`
- `GITHUB_TOKEN`
- `DEV_CHANNEL_TARGET`
- `GIT_NOTIFY_CHANNEL_TARGET`
- `CLOUDFLARED_VERSION`

초기화:
```bash
cp ~/.openclaw/workspace/.env.example ~/.openclaw/workspace/.env
```

---

## 5. User-facing operational commands

루트가 아니라 `bin/`을 사용한다.

### 이미지 빌드
```bash
./bin/build_gaejae_image
```

### 퀀트 DB 확인
```bash
./bin/check_gaejae_db
```

### 가재/OpenClaw 재시작 + 검증 + 요약 리포트
```bash
./bin/restart_gaejae
```

### baseline 갱신
```bash
./scripts/mark_image_baseline.sh
```

---

## 6. 형이 나를 재시작할 때 보는 명령어

가재/OpenClaw 운영에서 가장 중요한 재시작 경로는 아래 순서다.

### A. 빠른 재시작 (workspace 기준)
```bash
cd ~/.openclaw/workspace
./bin/restart_gaejae
```

이 명령은:
- 이미지 태깅
- docker compose down/up
- 컨테이너 health 확인
- `openclaw status` 확인
- Quant DB 확인
- drift/baseline 비교
- dev 채널 요약 전송
까지 한 번에 수행한다.

### B. OpenClaw gateway 상태 확인
```bash
openclaw gateway status
```

### C. gateway 재시작만 필요할 때
```bash
openclaw gateway restart
```

### D. Docker image 다시 빌드 후 재시작
```bash
cd ~/.openclaw/workspace
./bin/build_gaejae_image
./bin/restart_gaejae
```

### E. 새 이미지/환경이 안정화된 뒤 baseline 갱신
```bash
cd ~/.openclaw/workspace
./scripts/mark_image_baseline.sh
```

---

## 7. Docker 운영 원칙

### 역할 분리
- `Dockerfile.gaejae`
  - 시스템 레벨 의존성
  - cloudflared 같은 OS 레벨 바이너리
  - runtime PATH 기본값
- `.env`
  - credential / channel target / runtime knobs
- workspace bind mount
  - `.venv`
  - scripts
  - src
  - memory
  - 리서치 코드/데이터

### rebuild 후에도 유지되는 것
`Dockerfile.gaejae`에는 다음 PATH가 들어간다:
- `/home/node/.openclaw/workspace/bin`
- `/home/node/.local/bin`

이유:
- `bin/` 아래 사용자 명령 유지
- `gh` 같은 user-space CLI 유지

---

## 8. Git / GitHub 운영 원칙

### 기본 브랜치 규칙
- 기본 작업 브랜치: `gaejae`
- main 반영은 PR merge 기준
- 대규모 정리는 별도 refactor branch로 분리

### 자동화 원칙
가재는 다음을 직접 수행할 수 있다:
- branch 생성
- commit / push
- PR 생성
- PR merge
- merge 후 main sync

### Git 채널 알림
다음 이벤트는 Discord git 채널로 알림을 보낸다:
- branch 생성
- commit batch complete
- push complete
- PR created
- merge complete
- conflict resolved

기본 채널:
- `channel:1483989656470294548`

관련 helper:
```bash
./scripts/notify_git_channel.sh "[bkclaw] push complete - branch=..."
```

### GitHub CLI
이 저장소는 `gh` 기반 운영을 전제로 한다.

주요 helper:
- `scripts/git_push_current.sh`
- `scripts/gh_pr_create.sh`
- `scripts/gh_pr_merge.sh`

---

## 9. Discord 운영 원칙

### 실제 업로드 vs 내부 확인
- `read(image)` → 내부 확인용
- 실제 Discord에서 보이게 하려면 → `openclaw message send --media`

### media 업로드 규칙
- `workspace-*` 아래 파일은 직접 업로드가 거절될 수 있음
- 업로드 전 staging 경로 권장:
  - `~/.openclaw/media/`

안전 패턴:
1. artifact 생성
2. `~/.openclaw/media/`로 복사
3. `openclaw message send --media`
4. 성공 확인 후에만 “보냈다”라고 말하기

---

## 10. Reporting / notification channels

주요 채널:
- `dev` → `channel:1482514790768447590`
- `research-lab` → `channel:1481841620868530337`
- `paper-flow` → `channel:1481841598185738402`
- `news-flow` → `channel:1481841550299365549`
- `git notify` → `channel:1483989656470294548`

---

## 11. Logs and reports

### restart reports
- `logs/openclaw_restart_reports/`

### runtime state
- `logs/openclaw_runtime_state/`

### backtest outputs
- `reports/backtests/`
- `outputs/` (legacy outputs remain while migration is ongoing)

---

## 12. Refactor status

현재까지 정리된 축:
- runtime / execution mode 구조화
- ops / credential / env helper 정리
- GitHub CLI 자동화 경로 확보
- Discord send / channel target / git notify 규칙 정리
- artifact / report 구조화 시작
- legacy script env/path/db 중복 제거 시작
- root file reduction (`bin/`, `scripts/` 중심)
- Docker runtime PATH 반영

남은 큰 축:
- 남은 legacy scripts 추가 공통화
- delivery / notification 계층 추가 통합
- validation policy 세분화
- outputs / reports 경로 일원화

---

## 13. Reading order for operators

처음 볼 때 추천 순서:
1. `README.md`
2. `.env.example`
3. `Dockerfile.gaejae`
4. `docs/refactor/0001-*.md` ~ `0012-*.md`
5. `bin/` and `scripts/`
6. `src/`

---

## 14. Refactor references

- `docs/refactor/0001-architecture-principles.md`
- `docs/refactor/0002-ops-config-and-credential-rules.md`
- `docs/refactor/0003-git-and-env-helpers.md`
- `docs/refactor/0004-docker-build-rules.md`
- `docs/refactor/0005-workspace-cleanup-rules.md`
- `docs/refactor/0006-github-cli-automation.md`
- `docs/refactor/0007-legacy-script-cleanup.md`
- `docs/refactor/0008-git-channel-notifications.md`
- `docs/refactor/0009-root-wrapper-policy.md`
- `docs/refactor/0010-root-file-reduction.md`
- `docs/refactor/0011-docker-runtime-paths.md`
- `docs/refactor/0012-operational-layout.md`

---

## 15. One-line summary

이 저장소는 형의 퀀트 리서치와 가재 운영을 함께 담는 workspace이며,
리팩토링 원칙은 **불필요한 루트 clutter를 줄이고, 실행 로직을 `bin/`, `scripts/`, `src/`로 밀어 넣고, 운영 규칙은 문서/테스트/헬퍼로 고정하는 것**이다.
