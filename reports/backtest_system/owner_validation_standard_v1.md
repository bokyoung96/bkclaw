# Owner Validation Standard v1

## 목적
가재가 완료한 백테스트/전략 검증 결과를 형이 직접 재현·검토·승인할 수 있도록 표준 검증 패키지를 남긴다.

## 원칙
- `가재 검증`과 `형 검증`을 분리한다.
- 모든 백테스트는 최소한 동일 입력으로 재실행 가능한 형태여야 한다.
- 결과 요약만이 아니라, 전략 정의 / 데이터 / 비용 / 검증 상태를 함께 남긴다.

## 백테스트 결과와 함께 남길 것
1. 실행 스펙 (`spec.json`)
   - 전략/가설
   - 유니버스
   - 데이터 소스
   - 기간
   - 리밸런싱
   - 비용/슬리피지
   - 모드
2. 핵심 결과 (`summary.json`)
   - CAGR, Vol, Sharpe, MDD, Turnover 등
3. 검증 결과 (`validation.json`)
   - PASS / WARN / FAIL
   - 각 체크 항목별 메시지
4. 진행 로그 (`run.log`)
5. 재현 명령 (`reproduce.sh`)
6. 시각화 산출물 (`plots/*.png`)
7. owner check note (`owner_checklist.md`)

## 형이 확인할 체크리스트
- 전략 정의가 요청과 일치하는가?
- 사용 데이터/유니버스가 의도와 일치하는가?
- 비용/슬리피지가 반영되었는가?
- 리밸런싱 규칙이 자연스러운가?
- validation 결과에 FAIL이 없는가?
- WARN이 있다면 수용 가능한가?
- 그래프/요약 수치가 상식적으로 타당한가?
- 동일 스펙으로 재실행 가능한가?

## Validation 등급
- PASS: 실무상 문제 없음
- WARN: 해석 시 주의 필요
- FAIL: 결과를 신뢰하면 안 됨 / 재작업 필요

## 최소 validation 체크
- 전략 정의 누락 여부
- 기간/유니버스 누락 여부
- 비용 설정 누락 여부
- 리밸런싱 규칙 누락 여부
- 결과 시계열 비어 있음 여부
- turnover 비정상 여부
- max drawdown / sharpe NaN 여부
- 재현 명령 생성 여부

## dev 채널 알림 원칙
- START: 실행 시작
- INFO: 단계 진행
- WARNING: validation warning
- ERROR: validation fail / 실행 에러
- DONE: 산출물 생성 완료

## 승인 규칙
- 빠른 실험 모드: 형이 결과를 참고용으로 사용 가능
- 깊은 검증 모드: validation 패키지까지 보고 형이 승인/보류/재실행 판단
