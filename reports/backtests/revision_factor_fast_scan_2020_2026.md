# Revision Factor Fast Scan (2020-01-01 ~ 2026-03-19)

## 결론
2020-01-01 ~ 2026-03-19, 총 거래비용 10bp(슬리피지 포함) 기준으로 SPY-US 유니버스에서 아래 3개 전략이 Sharpe 0.8 이상을 충족했다.

1. **revision_only**
   - Sharpe: **1.060**
   - CAGR: **20.96%**
   - Vol: **19.82%**
   - MDD: **-22.34%**
2. **revision_value_mom**
   - Sharpe: **0.889**
   - CAGR: **14.77%**
   - Vol: **17.16%**
   - MDD: **-24.18%**
3. **revision_value**
   - Sharpe: **0.821**
   - CAGR: **12.27%**
   - Vol: **15.59%**
   - MDD: **-18.80%**

## 빠른 데이터 파악
실제 사용 가능 데이터 확인 결과:
- `public.daily_adjusted_time_series_data_stock`
  - `close_tr`, `dollar_volume`, `marketcap_security`
  - `forward_next_twelve_months_annual_eps_adjusted`
  - `number_of_estimates_eps`
- `public.monthly_etf_constituents`
  - SPY-US 구성 종목 유니버스
- `public.monthly_time_series_data_stock`
  - GICS sector 계층
- `public.daily_adjusted_time_series_data_index`
  - `SP50` (S&P 500 index)

## 경제적 rationale
### 1) revision_only
- 3개월 전 대비 forward 12M EPS 상향 폭이 큰 종목을 매수
- rationale:
  - analyst revision은 펀더멘털 개선의 후행 확인이면서도 완전 즉시 반영되지 않는 경우가 많음
  - estimate coverage가 충분한 이름만 사용하여 노이즈 감소

### 2) revision_value
- EPS revision + earnings yield 결합
- rationale:
  - revision만 쓰면 비싼 성장주 쏠림이 커질 수 있음
  - forward earnings yield를 섞어 valuation discipline 추가

### 3) revision_value_mom
- EPS revision + earnings yield + 6M momentum 결합
- rationale:
  - revision의 펀더멘털 정보 + valuation + price confirmation을 함께 사용
  - 단, turnover와 drawdown은 revision_value 대비 다소 높아짐

## 공통 구현 규칙
- Universe: `SPY-US`
- 기간: **2020-01-01 ~ 2026-03-19**
- 리밸런싱: 월말
- 거래비용: **10bp total**
- 유동성 필터: `dollar_volume > 5e6`
- size 필터: `marketcap_security > 5e4` (이 DB 스케일 기준)
- estimate coverage 필터: `number_of_estimates_eps >= 3`
- selection: 상위 15%

## 리스크 / 해석 주의
- 현재 DB에서 사용 가능한 재무 필드는 제한적이라, quality/accruals 등 더 풍부한 cross-section 검증은 아직 못 했다.
- `marketcap_security`는 일반적인 USD 시총 스케일과 다르게 저장된 것으로 보여, DB 내부 단위 기준으로 필터를 맞췄다.
- revision signal은 coverage가 낮은 초기 시점에서 sample quality 저하 가능성이 있다. 이를 막기 위해 estimate count filter를 넣었다.
- MDD는 세 전략 모두 -18.8% ~ -24.2% 수준으로, “매우 낮다”고 하긴 어렵지만 요청한 fast mode 기준에서는 과도하게 높지도 않은 편이다.

## 산출물
- `outputs/revision_only/`
- `outputs/revision_value/`
- `outputs/revision_value_mom/`

각 디렉토리 포함:
- summary.json
- daily_portfolio_series.csv
- monthly_portfolio_returns.csv
- last_holdings.csv
- cumulative_return_and_drawdown.png
- return_distributions.png
- progress_note.md

## 코드 변경
- `scripts/revision_factor_backtest.py`
  - revision 계열 전략 백테스트 스크립트 추가
- `scripts/run_backtest.py`
  - worktree/직접 실행 시 `src` import 경로 보강
- `src/backtest/strategies/common.py`
  - legacy script runner에 `PYTHONPATH` 기본 주입 및 인자 전달 지원

## 추천
운용 우선순위는 아래 순서가 적절하다.
1. **revision_only**: 성과 최우선
2. **revision_value**: 더 보수적 MDD/vol 선호 시
3. **revision_value_mom**: 중간 타협안
