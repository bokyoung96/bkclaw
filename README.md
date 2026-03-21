# Quant Research Workspace

Python 기반 퀀트 리서치 워크스페이스이자, 가재(OpenClaw 기반 연구 에이전트)의 운영 저장소다.

이 저장소는 단순 코드 모음이 아니라 아래 세 가지를 함께 관리한다:
- 퀀트 리서치 / 백테스트 코드
- OpenClaw / OMX / Codex 운영 런타임
- Discord / GitHub 연동을 포함한 실제 운영 절차

---

## 1. Workspace 목적

이 저장소는 다음 용도를 가진다:
- 외부 데이터 적재
- 논문 아이디어 구현
- 백테스트 / 평가
- dev / research-lab / paper-flow 보고 루프 연결
- OpenClaw 기반 연구 에이전트 운영
- Docker rebuild 이후에도 반복 가능한 운영 상태 유지

---

## 2. 현재 런타임 구조

이 workspace는 **Python 리서치 런타임**과 **Node 기반 Codex/OMX 런타임**이 분리되어 있다.

### A. Python / backtest lane
- 시스템 인터프리터:
  - `python3` (운영 런타임 내부 기본 제공)
- workspace 실행환경:
  - `~/.openclaw/workspace/.venv`
- 용도:
  - 백테스트
  - 데이터 검증
  - 리서치/리포팅 Python 실행
  - Quant DB / 데이터 파이프라인 Python 실행
- 대표 진입점:
  - `scripts/run_backtest.py`
  - `scripts/run_experiment.py`
  - `scripts/validate_data.py`

중요:
- 운영 보고에서 `python이 없다`고 단정하지 않는다.
- 먼저 아래 층위를 분리해서 본다:
  1. 운영 런타임에 `python3`가 있는가
  2. workspace `.venv`가 있는가
  3. 특정 프로젝트 전용 env/Dockerfile이 별도로 필요한가

### B. Codex CLI lane
- 전역 설치 위치:
  - binary: `/usr/local/bin/codex`
- 인증 홈:
  - `CODEX_HOME=$HOME/.local/share/codex`
- 용도:
  - 실제 agent 실행 엔진
  - non-interactive exec
  - OMX가 감싸는 기본 실행기

### C. OMX lane
- 기본 진입점:
  - `./bin/omx`
  - `./bin/ralph`
- 실행 우선순위:
  1. `~/.local/bin/omx` (global npm install)
  2. PATH 상의 `omx`
  3. repo-local fallback `external/oh-my-codex`
- 용도:
  - Codex orchestration
  - prompt/skill/MCP/runtime state wiring
  - team / ralph / explore / session / hud

### D. OpenClaw lane
- 용도:
  - 형과의 실제 채팅 인터페이스
  - cross-session messaging
  - Discord / other provider routing
  - exec / file / web / image / memory 도구 사용

한 줄로 정리하면:
- **Python `.venv`** → 연구/백테스트
- **Codex CLI** → 실행 엔진
- **OMX** → Codex orchestration layer
- **OpenClaw** → 형과 가재를 연결하는 운영 인터페이스

---

## 3. Repository layout

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
  - `omx`
  - `ralph`
- `scripts/`
  - build / restart / validation / git / gh / notify helpers
- `scripts/discord/`
  - Discord operational dispatch entrypoints
- `src/`
  - backtest / reporting / data_sources / workflows / common
- `docs/refactor/`
  - refactor principles, cleanup policy, git notification rules, docker runtime rules
- `external/oh-my-codex/`
  - repo-local OMX fallback runtime

---

## 4. Protected files

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

## 5. Environment and credentials

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
- `CODEX_HOME`

초기화:
```bash
cp ~/.openclaw/workspace/.env.example ~/.openclaw/workspace/.env
```

권장 Codex home:
```bash
export CODEX_HOME="$HOME/.local/share/codex"
```

---

## 6. User-facing operational commands

루트가 아니라 `bin/`을 사용한다.

### 이미지 빌드
```bash
./bin/build_gaejae_image
```

### 퀀트 DB 확인
```bash
./bin/check_gaejae_db
```

### 운영 런타임 / workspace 층위 점검
```bash
./bin/check_runtime_layers
```

### Tavily research lane 점검
```bash
./scripts/check_tavily_research_lane.sh
```

Tavily 사용 원칙:
- Tavily가 research lane의 기본 current-web 탐색기다.
- browser automation은 Tavily/web_search로 충분하지 않을 때만 follow-up으로 쓴다.

### 가재/OpenClaw 재시작 + 검증 + 요약 리포트
```bash
./bin/restart_gaejae
```

### baseline 갱신
```bash
./scripts/mark_image_baseline.sh
```

### 백테스트 packet (Markdown + PDF) 생성
```bash
./bin/generate_backtest_packet reports/backtests/<run_dir>
```

원칙:
- packet 생성은 가능하면 workspace `.venv` Python을 우선 사용한다.
- system `python3`와 `.venv`의 라이브러리 구성이 다를 수 있으므로, 보고 전에 interpreter를 먼저 확인한다.

### 장기 작업 progress note 기록
```bash
TASK_NAME=my_task STATUS=IN_PROGRESS STEP="research" ./bin/progress_note "현재 research 단계 진행 중"
```

원칙:
- 10분 이상 걸릴 가능성이 있는 작업은 시작/중간/완료 상태를 분리해서 기록한다.
- 가능하면 `logs/progress/<task>.latest.md` 와 `.jsonl`에 남긴다.

### trusted elevated 정책 검증
```bash
python3 scripts/check_trusted_elevated_policy.py
```

### OMX / Ralph 실행
```bash
./bin/omx --version
./bin/omx doctor
./bin/ralph "fix the scoped task with persistent verification"
./bin/ralph --prd "ship the operator workflow with acceptance criteria"
```

---

## 7. Lane model (무엇을 언제 쓰는가)

형과 가재가 이 workspace에서 기본적으로 쓰는 lane은 아래처럼 나눈다.

### Lane A. Research lane
- 목적:
  - 현재성 높은 자료 탐색
  - 논문/기사/source shortlisting
  - source tier 정리
  - 빠른 current-awareness 확보
- 기본 도구:
  - OpenClaw research agent
  - Tavily research (workspace `.env`의 `TAVILY_API_KEY` 기준)
  - primary skill: `skills/tavily-research-lane/`
  - browser follow-up: `skills/browser-research-lane/`
  - web search / fetch
  - memory / session lookup
- 기본 출력:
  - 결론
  - 핵심 근거
  - source tier
  - 리스크/불확실성
  - 다음 액션

Tavily 운영 원칙:
- Tavily는 **research agent 전용 research lane**으로 본다.
- `TAVILY_API_KEY`가 `.env`에 있어도, active runtime 반영 여부와 실제 search smoke test는 별도로 확인한다.
- `키 존재`와 `실제 검색 성공`을 같은 것으로 취급하지 않는다.
- 이 lane은 기본적으로 **빠른 탐색/shortlisting** 쪽에 최적화한다.

### Lane A-2. Deep research lane
- 목적:
  - 심층 리서치
  - source triangulation
  - thesis / anti-thesis 정리
  - paper / article / docs / news cross-check
  - 구현 관점 번역
- 기본 skill:
  - `skills/deep-research-lane/`
- 사용할 때:
  - 형이 `심층 리서치`, `깊게`, `자세히`, `반대 근거도`, `리스크까지` 같은 요구를 할 때
  - 단순 shortlist보다 해석/반론/제약조건이 중요할 때
- 기본 출력 추가 요소:
  - thesis
  - counter-thesis
  - weakest assumption
  - what would change the conclusion


### Lane A-3. Reviewer lane
- 목적:
  - 과장 방지
  - 약한 가정 점검
  - 반대 근거/검증 누락 확인
- 기본 skill:
  - `skills/reviewer-lane/`
- 사용할 때:
  - deep research 결과를 바로 채택하기 전에 한 번 더 점검할 때
  - 형이 `리스크도`, `반대 근거도`, `검토해봐` 같은 요청을 할 때

### Lane B. Python backtest lane
- 목적:
  - 전략 구현
  - 데이터 검증
  - 실험/백테스트 실행
- 기본 실행기:
  - `~/.openclaw/workspace/.venv`
- 사용할 때:
  - Python 코드 수정/실험/리포트 생성
  - DuckDB / connectorx / lightgbm / pandas 계열 실행

### Lane C. OMX orchestration lane
- 목적:
  - Codex에 prompt/skill/MCP/state를 입혀서 더 구조적으로 실행
- 기본 진입점:
  - `./bin/omx`
- 사용할 때:
  - Codex를 그냥 단발 호출하는 것보다
  - prompt catalog / skill / session / team / ralph를 같이 쓰고 싶을 때

### Lane D. Ralph lane
- 목적:
  - "끝까지 해", "verify까지 포함해서 해", "중간에 멈추지 마" 같은 persistent execution
- 기본 진입점:
  - `./bin/ralph`
- 사용할 때:
  - 구현 + 검증 + 재시도 루프가 필요한 작업
  - PRD 기반 작업
  - architect-style sign-off를 포함한 장기 실행

### Lane E. Direct Codex lane
- 목적:
  - 간단한 non-interactive exec
  - 빠른 smoke / 짧은 수정 / 즉시 응답형 테스트
- 기본 진입점:
  - `codex exec ...`
- 사용할 때:
  - Ralph/team까지는 과한데 Codex 자체 실행은 필요할 때

### agent 구조 제안
- `main`
  - 운영 총괄 / 일반 대화 / 최종 보고
- `research`
  - quick + deep research를 모두 담당하는 통합 research agent
- `reviewer`
  - 과장 방지 / 반대 근거 / 품질 검토
- `backtest` (추천 추가 후보)
  - 전략 구현 / 실험 / 백테스트 실행
  - run artifact 생성
- `performance-review` (추천 추가 후보)
  - 성과 해석 / 보고 포맷 / 리스크 점검
  - economic rationale / source links / PDF packet 정리

### 기본 운영 원칙
- research 질의 → **Research lane 우선**
- Python 전략/백테스트 → **Python backtest lane 우선**
- Codex orchestration 필요 → **OMX lane**
- persistent completion 필요 → **Ralph lane**
- 짧은 codex smoke/test → **Direct Codex lane**

### handoff 규칙
- **Research → OMX**: source shortlisting과 thesis가 끝나고, 실제 구현/파일 작업이 시작될 때 넘긴다.
- **OMX → Ralph**: persistent execution, retry loop, verify 포함 완료가 필요할 때 넘긴다.
- **Direct Codex**는 좁은 smoke/짧은 수정에 한정하고, multi-step 작업은 OMX 이상으로 올린다.

---

## 8. 형이 나를 재시작할 때 보는 명령어

가재/OpenClaw 운영에서 가장 중요한 재시작 경로는 아래 순서다.

### A. 빠른 재시작 (host/local workspace 기준)
```bash
cd ~/.openclaw/workspace
./bin/restart_gaejae
```

또는 repo가 `~/openclaw`에 있다면:
```bash
cd ~/openclaw
./bin/restart_gaejae
```

중요:
- `/home/node/.openclaw/workspace` 는 **컨테이너 내부 경로**다.
- Mac/host 터미널에서는 이 경로를 직접 쓰지 않는다.
- host에서는 보통 `~/.openclaw/workspace` 또는 `~/openclaw`에서 실행한다.

기본적으로 아래 경로들도 자동 탐색한다:
- `~/openclaw/docker-compose.yml`
- repo root 인근 compose 파일

이 명령은:
- 기본 이미지 `gaejae-openclaw:latest`를 기준으로 태깅
- `OPENCLAW_IMAGE`를 compose에 주입하여 docker compose down/up 수행
- 컨테이너 health 확인
- 컨테이너 내부 Ollama 기동/모델 준비 확인
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

이 경로는 다음이 바뀌었을 때 특히 필요하다:
- OpenClaw CLI 버전
- Ollama / cloudflared 같은 이미지 레벨 바이너리
- entrypoint / PATH / bootstrap 로직

### E. 새 이미지/환경이 안정화된 뒤 baseline 갱신
```bash
cd ~/.openclaw/workspace
./scripts/mark_image_baseline.sh
```

---

## 9. Docker 운영 원칙

### 역할 분리
- `Dockerfile.gaejae`
  - 시스템 레벨 의존성
  - cloudflared, ollama 같은 OS 레벨 바이너리
  - OpenClaw CLI 버전 고정 설치
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
- `omx`, `gh` 같은 user-space CLI 유지

### Ollama 메모리 복구 메모
- 이미지 레벨 재현성은 `Dockerfile.gaejae`가 담당한다.
- 현재 세션에서 바로 복구할 때는:
  ```bash
  cd ~/.openclaw/workspace
  ./scripts/install_ollama_user.sh
  ./scripts/start_local_ollama.sh
  ```
- 재빌드 후 컨테이너를 다시 올린 뒤에는 `ollama` 바이너리는 이미지에 포함된다.
- 이미지/사용자 설치 경로 차이를 흡수하도록 `scripts/start_local_ollama.sh`가 아래 경로들을 자동 탐색한다:
  - `~/.local/bin/ollama`
  - `~/.local/lib/ollama/bin/ollama`
  - `/usr/local/bin/ollama`
  - `/usr/local/ollama`
- 다만 `127.0.0.1:11434` 서버는 런타임에서 실제로 띄워져야 하므로, 필요 시 `./scripts/start_local_ollama.sh`를 한 번 실행한다.

### 운영 런타임 상태 판정 규칙
`없다 / 안 된다`는 표현은 아래 확인 전에 쓰지 않는다.

1. 바이너리 존재 여부
2. PATH 노출 여부
3. 환경변수/토큰 주입 여부
4. 호스트 ↔ 컨테이너 경로 차이
5. 사용자가 이미 제공한 운영 맥락/Dockerfile/이미지 전제

특히 아래 3층을 분리해서 보고한다:
- **운영 런타임**: 현재 OpenClaw 컨테이너 전체 상태
- **workspace 실행환경**: `.venv`, shared scripts, env
- **프로젝트 실행환경**: 특정 repo의 local env / Dockerfile / 개별 검증 상태

---

## 10. Git / GitHub 운영 원칙

### 기본 브랜치 규칙
- **새 git 작업은 항상 branch에서 시작한다**
- 형이 명시적으로 요구하지 않는 한 `main`에서 직접 작업하지 않는다
- 목적별 짧은 branch를 만들고, merge 후 정리한다

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
./scripts/notify_git_channel.sh push-complete <branch> "commits=... focus=..."
```

push 전에 추천:
```bash
./scripts/pre_push_refactor_check.sh
```

### GitHub CLI
이 저장소는 `gh` 기반 운영을 전제로 한다.

주요 helper:
- `scripts/git_configure_auth.sh`
- `scripts/git_push_current.sh`
- `scripts/gh_pr_create.sh`
- `scripts/gh_pr_merge.sh`

추천 초기화:
```bash
cd ~/.openclaw/workspace
./scripts/git_configure_auth.sh
```

---

## 11. Discord 운영 원칙

### 현재 채널 답장 vs 다른 채널 전송
- 현재 채널에서의 일반 답장은 OpenClaw의 기본 라우팅을 따른다.
- 다른 채널 전송은 아래 둘을 분리한다:
  1. `sessions_send` → **세션 주입 / 라우팅 확인용**
  2. `openclaw message send --channel discord --target ...` → **실제 Discord direct send**

완료 판정 규칙:
- `sessions_send`의 내부 ack만으로는 실제 Discord 전송 완료로 보지 않는다.
- 가능하면 `messageId` 또는 **실제 Discord 가시 메시지**를 완료 근거로 사용한다.
- git 채널과 새/불안정 채널은 **direct send 우선**이다.

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

## 12. Reporting / notification channels

주요 채널:
- `dev` → `channel:1482514790768447590`
- `research-lab` → `channel:1481841620868530337`
- `paper-flow` → `channel:1481841598185738402`
- `news-flow` → `channel:1481841550299365549`
- `crypto` → `channel:1484724388065706054`
- `git notify` → `channel:1483989656470294548`

채널 운용 메모:
- `git notify`는 `sessions_send` 대신 direct Discord send를 우선 사용한다.
- `crypto` 채널은 현재 사용 가능 대상으로 보되, 완료 판정은 **실제 visible message 확인** 기준을 우선한다.

---

## 13. Logs and reports

### restart reports
- `logs/openclaw_restart_reports/`

### runtime state
- `logs/openclaw_runtime_state/`

### backtest outputs
- `reports/backtests/`
- `outputs/` (legacy outputs remain while migration is ongoing)

---

## 14. Refactor status

현재까지 정리된 축:
- runtime / execution mode 구조화
- ops / credential / env helper 정리
- GitHub CLI 자동화 경로 확보
- Discord send / channel target / git notify 규칙 정리
- artifact / report 구조화 시작
- legacy script env/path/db 중복 제거 시작
- root file reduction (`bin/`, `scripts/` 중심)
- Docker runtime PATH 반영
- README / restart runbook / workspace layout self-check 추가
- retrospective log 도입
- trusted elevated baseline 검증 경로 추가
- OMX / Ralph wrapper 경로 추가
- Codex home을 `~/.local/share/codex`로 정규화

남은 큰 축:
- 남은 legacy scripts 추가 공통화
- delivery / notification 계층 추가 통합
- validation policy 세분화
- outputs / reports 경로 일원화
- Tavily active-runtime 반영 + smoke test 자동화
- 운영 런타임 / workspace env / 프로젝트 env 상태 판정 분리
- 채널별 direct-send / sessions_send 정책 표준화
- Tavily research lane와 OMX orchestration lane의 실제 운용 결합 정교화
- Ralph / team lane를 실제 리팩토링 작업 플로우에 더 자연스럽게 연결

---

## 15. Reading order for operators

처음 볼 때 추천 순서:
1. `README.md`
2. `.env.example`
3. `Dockerfile.gaejae`
4. `docs/refactor/0001-*.md` ~ 최신 문서
5. `bin/` and `scripts/`
6. `src/`

---

## 16. Refactor references

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
- `docs/refactor/0013-restart-runbook.md`
- `docs/refactor/0014-readme-standard.md`
- `docs/refactor/0015-workspace-layout-check.md`
- `docs/refactor/0016-final-ops-baseline.md`
- `docs/refactor/0017-retrospective-log.md`
- `docs/refactor/0018-agent-lane-model.md`
- `docs/refactor/0019-tavily-research-lane.md`
- `docs/refactor/0020-omx-baseline.md`
- `docs/refactor/0021-branch-cleanup-policy.md`
- `docs/refactor/0022-tavily-omx-readiness.md`
- `docs/refactor/0023-git-runtime-hardening.md`
- `docs/refactor/0024-research-agent-smoke-test.md`
- `docs/refactor/0025-git-notify-format-and-preflight.md`
- `docs/refactor/0026-build-runtime-guarantees.md`
- `docs/refactor/0027-skill-integration-browser-and-self-improve.md`
- `docs/refactor/0028-skill-refresh-and-alignment.md`
- `docs/refactor/0029-notice-formatting-failure-and-fix.md`
- `docs/refactor/0030-restart-runtime-resolution.md`
- `docs/refactor/0031-trusted-elevated-policy.md`
- `docs/refactor/0032-gaejae-omx-ralph-launch.md`
- `docs/refactor/0033-runtime-verification-and-channel-delivery.md`
- `docs/refactor/0034-openclaw-cli-version-pinning.md`
- `docs/refactor/0035-output-and-artifact-path-conventions.md`
- `docs/refactor/0036-main-memory-indexing-followup.md`
- `docs/refactor/0037-long-task-progress-and-alive-check.md`
- `skills/research-lane/SKILL.md`
- `skills/reviewer-lane/SKILL.md`

---

## 17. One-line summary

이 저장소는 형의 퀀트 리서치와 가재 운영을 함께 담는 workspace이며,
핵심 원칙은 **연구용 Python lane, Codex 실행 lane, OMX orchestration lane, OpenClaw 운영 lane을 분리하고, 실행 진입점은 `bin/`, 구현은 `scripts/`/`src/`, 운영 규칙은 문서/헬퍼/검증 스크립트로 고정하는 것**이다.
