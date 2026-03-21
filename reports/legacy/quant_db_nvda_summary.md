# 퀀트 DB - NVDA 요약

## 사용 테이블
- public.daily_adjusted_time_series_data_stock
- public.daily_adjusted_time_series_data_index
- public.macro_time_series

## 식별자
- ticker: NVDA
- sedol: 2379504

## 사용 필드
- stock: close_pr, close_tr, dollar_volume, marketcap_security
- benchmark: SPX Index / close_tr
- risk free: US Benchmark Bill - 3 Month / ytm

## 분석 기간
- 2020-01-01 ~ 2026-03-13

## 결과 파일
- plot: /home/node/.openclaw/workspace/outputs/figures/nvda_cumret_drawdown.png
- this note: /home/node/.openclaw/workspace/datas/quant_db_nvda_summary.md

## RiskReturnProfile
          CAGR(%) STD_annualized(%) Weekly Hit Ratio(%) Sharpe_Ratio MDD(%)    MDD시점 UnderWaterPeriod(년) 1M Ret(%) 3M Ret(%) 6M Ret(%) 1Y Ret(%) 3Y Ret(%) BM_ret excess_return(%) tracking_error(%) Information_Ratio BM대비주간승률(%) BM대비최대손실(%) BM대비최대손실시점 BM_ret Max Underwater(년)
NVDA         70.6              51.7                57.7        1.267  -66.3  2022-10                 1.5      -3.6       1.4       2.3      58.0     566.0                    55.1              40.2             1.371        57.7       -54.1    2022-10                      1.4
Benchmark    13.6              20.3                55.9        0.513  -33.8  2020-03                 2.0      -2.2      -1.6       1.2      18.0      68.0                       -                 -                 -           -           -          -                        -
