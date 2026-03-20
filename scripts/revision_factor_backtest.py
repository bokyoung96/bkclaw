from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from urllib.parse import quote_plus

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from topquant_ksk.db.tunnel import kill_tunnel, manage_db_tunnel

from src.common.quant_db import load_quant_db_credentials

ROOT = Path(__file__).resolve().parents[1]

VARIANTS = {
    "revision_only": {
        "output_dir": ROOT / "outputs" / "revision_only",
        "combo": "revision",
        "sector_neutral": False,
        "market_half": False,
        "top_pct": 0.15,
    },
    "revision_value": {
        "output_dir": ROOT / "outputs" / "revision_value",
        "combo": "revision_value",
        "sector_neutral": False,
        "market_half": False,
        "top_pct": 0.15,
    },
    "revision_value_mom": {
        "output_dir": ROOT / "outputs" / "revision_value_mom",
        "combo": "revision_value_mom",
        "sector_neutral": False,
        "market_half": True,
        "top_pct": 0.15,
    },
}

TOTAL_COST_BPS = 10
UNIVERSE = "SPY-US"
START_DATE = "2019-01-01"
LIVE_START = "2020-01-01"
MIN_DOLLAR_VOLUME = 5e6
MIN_MARKETCAP_UNITS = 5e4
MIN_ESTIMATES = 3


def make_engine():
    creds = load_quant_db_credentials(ROOT)
    tunnel = manage_db_tunnel()
    uri = f"postgresql://{creds.user}:{quote_plus(creds.password)}@127.0.0.1:15432/quant_data"
    engine = create_engine(uri)
    return tunnel, engine


def fetch_data(engine):
    with engine.connect() as conn:
        const = pd.read_sql(
            text(
                """
                SELECT time, sedol, ticker, company_name
                FROM public.monthly_etf_constituents
                WHERE universe_name = :universe
                  AND time >= :start_date
                ORDER BY time, sedol
                """
            ),
            conn,
            params={"universe": UNIVERSE, "start_date": START_DATE},
            parse_dates=["time"],
        )
        sedols = sorted(const["sedol"].dropna().unique().tolist())
        if not sedols:
            raise RuntimeError("No constituents found for universe")

        stock = pd.read_sql(
            text(
                """
                SELECT time, sedol, ticker, company_name,
                       close_tr,
                       marketcap_security,
                       dollar_volume,
                       forward_next_twelve_months_annual_eps_adjusted AS fwd_eps,
                       number_of_estimates_eps AS n_est
                FROM public.daily_adjusted_time_series_data_stock
                WHERE sedol = ANY(:sedols)
                  AND time >= :start_date
                ORDER BY time, sedol
                """
            ),
            conn,
            params={"sedols": sedols, "start_date": START_DATE},
            parse_dates=["time"],
        )
        sectors = pd.read_sql(
            text(
                """
                SELECT time, sedol, gics_level1_sector
                FROM public.monthly_time_series_data_stock
                WHERE sedol = ANY(:sedols)
                  AND time >= :start_date
                ORDER BY time, sedol
                """
            ),
            conn,
            params={"sedols": sedols, "start_date": START_DATE},
            parse_dates=["time"],
        )
        benchmark = pd.read_sql(
            text(
                """
                SELECT time, close_tr
                FROM public.daily_adjusted_time_series_data_index
                WHERE ticker = 'SP50'
                  AND time >= :start_date
                ORDER BY time
                """
            ),
            conn,
            params={"start_date": START_DATE},
            parse_dates=["time"],
        )
    return const, stock, sectors, benchmark


def normalize_time_index(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index = pd.to_datetime(df.index, utc=True).tz_localize(None)
    return df


def zscore(series: pd.Series) -> pd.Series:
    series = series.replace([np.inf, -np.inf], np.nan).dropna()
    if len(series) < 5:
        return pd.Series(dtype=float)
    std = series.std(ddof=0)
    if std == 0 or pd.isna(std):
        return pd.Series(dtype=float)
    return (series - series.mean()) / std


def last_on_or_before(sorted_dates: pd.DatetimeIndex, dt: pd.Timestamp):
    pos = sorted_dates.searchsorted(dt, side="right") - 1
    if pos < 0:
        return None
    return sorted_dates[pos]


def compute_metrics(daily_net: pd.Series, turnover: pd.Series) -> dict[str, float | str]:
    daily_net = daily_net[daily_net.index >= pd.Timestamp(LIVE_START)].dropna()
    nav = (1 + daily_net).cumprod()
    dd = nav / nav.cummax() - 1
    monthly = daily_net.resample("ME").apply(lambda x: (1 + x).prod() - 1)
    ann_vol = daily_net.std(ddof=0) * math.sqrt(252)
    sharpe = daily_net.mean() / daily_net.std(ddof=0) * math.sqrt(252) if daily_net.std(ddof=0) > 0 else np.nan
    years = len(daily_net) / 252
    cagr = nav.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    return {
        "start": str(daily_net.index.min().date()),
        "end": str(daily_net.index.max().date()),
        "total_return": float(nav.iloc[-1] - 1),
        "annual_return": float(cagr),
        "annual_vol": float(ann_vol),
        "sharpe": float(sharpe),
        "max_drawdown": float(dd.min()),
        "daily_hit_ratio": float((daily_net > 0).mean()),
        "monthly_hit_ratio": float((monthly > 0).mean()),
        "avg_monthly_turnover": float(turnover.mean()),
        "median_monthly_turnover": float(turnover.median()),
        "rebalance_count": int((turnover > 0).sum()),
    }


def build_score(combo: str, revision: pd.Series, earnings_yield: pd.Series, momentum_6m: pd.Series) -> pd.Series:
    if combo == "revision":
        return zscore(revision)
    if combo == "revision_value":
        return zscore(revision).add(0.5 * zscore(earnings_yield), fill_value=0.0)
    if combo == "revision_value_mom":
        return zscore(revision).add(0.5 * zscore(earnings_yield), fill_value=0.0).add(0.5 * zscore(momentum_6m), fill_value=0.0)
    raise ValueError(f"Unknown combo: {combo}")


def run_variant(variant_name: str) -> dict:
    variant = VARIANTS[variant_name]
    output_dir = variant["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    tunnel = None
    try:
        tunnel, engine = make_engine()
        const, stock, sectors, benchmark = fetch_data(engine)
    finally:
        if tunnel is not None:
            kill_tunnel(tunnel)

    meta = stock[["sedol", "ticker", "company_name"]].drop_duplicates("sedol").set_index("sedol")
    prices = normalize_time_index(stock.pivot_table(index="time", columns="sedol", values="close_tr", aggfunc="last").sort_index())
    mcap = normalize_time_index(stock.pivot_table(index="time", columns="sedol", values="marketcap_security", aggfunc="last").sort_index()).reindex(prices.index).ffill()
    dollar_volume = normalize_time_index(stock.pivot_table(index="time", columns="sedol", values="dollar_volume", aggfunc="last").sort_index()).reindex(prices.index).ffill()
    fwd_eps = normalize_time_index(stock.pivot_table(index="time", columns="sedol", values="fwd_eps", aggfunc="last").sort_index()).reindex(prices.index).ffill()
    n_est = normalize_time_index(stock.pivot_table(index="time", columns="sedol", values="n_est", aggfunc="last").sort_index()).reindex(prices.index).ffill()
    returns = prices.pct_change().fillna(0.0)

    const["time"] = pd.to_datetime(const["time"], utc=True).dt.tz_localize(None)
    sectors["time"] = pd.to_datetime(sectors["time"], utc=True).dt.tz_localize(None)
    membership_map = {dt: grp[["sedol", "ticker", "company_name"]].drop_duplicates("sedol").set_index("sedol") for dt, grp in const.groupby("time")}
    membership_dates = pd.DatetimeIndex(sorted(membership_map.keys()))
    sector_map = {dt: grp.drop_duplicates("sedol").set_index("sedol")["gics_level1_sector"] for dt, grp in sectors.groupby("time")}
    sector_dates = pd.DatetimeIndex(sorted(sector_map.keys()))

    benchmark_series = benchmark.set_index("time")["close_tr"].sort_index()
    benchmark_series.index = pd.to_datetime(benchmark_series.index, utc=True).tz_localize(None)
    benchmark_series = benchmark_series.reindex(prices.index).ffill()
    benchmark_ma200 = benchmark_series.rolling(200).mean()

    month_ends = prices.index.to_series().groupby(prices.index.to_period("M")).max().tolist()
    rebal_dates = [dt for dt in month_ends if dt >= pd.Timestamp(LIVE_START)]
    rebal_set = set(rebal_dates)

    weights_prev = pd.Series(0.0, index=prices.columns)
    portfolio_rets: list[float] = []
    cost_series: list[float] = []
    turnover_series: list[float] = []
    selected_names: dict[pd.Timestamp, pd.DataFrame] = {}

    for i, dt in enumerate(prices.index):
        daily_ret = returns.loc[dt].reindex(weights_prev.index).fillna(0.0)
        gross = float((weights_prev * daily_ret).sum())
        weights_after = weights_prev * (1 + daily_ret)
        gross_nav = weights_after.sum()
        weights_after = weights_after / gross_nav if gross_nav > 0 else weights_after * 0.0

        cost = 0.0
        turnover = 0.0
        if dt in rebal_set and i >= 252:
            const_dt = last_on_or_before(membership_dates, dt)
            sector_dt = last_on_or_before(sector_dates, dt)
            members = pd.Index(membership_map[const_dt].index)
            eligible = members.intersection(prices.columns)

            px = prices.iloc[i - 1].reindex(eligible)
            fwd_now = fwd_eps.iloc[i - 1].reindex(eligible)
            fwd_3m = fwd_eps.iloc[i - 63].reindex(eligible)
            mom_6m = prices.iloc[i - 21].reindex(eligible) / prices.iloc[i - 147].reindex(eligible) - 1
            revision = (fwd_now - fwd_3m) / fwd_3m.abs().replace(0, np.nan)
            earnings_yield = fwd_now / px.replace(0, np.nan)
            score = build_score(variant["combo"], revision, earnings_yield, mom_6m)

            liq = dollar_volume.iloc[i - 1].reindex(eligible)
            cap = mcap.iloc[i - 1].reindex(eligible)
            est = n_est.iloc[i - 1].reindex(eligible)
            score = score.reindex(
                score.index.intersection(liq[liq > MIN_DOLLAR_VOLUME].index)
                .intersection(cap[cap > MIN_MARKETCAP_UNITS].index)
                .intersection(est[est >= MIN_ESTIMATES].index)
            ).dropna()

            target = pd.Series(0.0, index=prices.columns)
            picked = pd.Series(dtype=float)
            if len(score) > 10:
                if variant["sector_neutral"] and sector_dt is not None:
                    sector_series = sector_map[sector_dt].reindex(score.index).dropna()
                    bucket_list: list[pd.Series] = []
                    for sector_name in sorted(sector_series.unique()):
                        sec_scores = score.reindex(sector_series[sector_series == sector_name].index).dropna()
                        if sec_scores.empty:
                            continue
                        k = max(1, int(math.ceil(len(sec_scores) * 0.20)))
                        bucket_list.append(sec_scores.sort_values(ascending=False).head(k))
                    if bucket_list:
                        picked = pd.concat(bucket_list)
                        picked_sector = sector_map[sector_dt].reindex(picked.index)
                        active_sectors = sorted(picked_sector.dropna().unique())
                        for sector_name in active_sectors:
                            names = picked_sector[picked_sector == sector_name].index
                            target.loc[names] = 1.0 / len(active_sectors) / len(names)
                else:
                    k = max(5, int(math.ceil(len(score) * variant["top_pct"])))
                    picked = score.sort_values(ascending=False).head(k)
                    target.loc[picked.index] = 1.0 / len(picked)

                if variant["market_half"] and benchmark_series.loc[dt] <= benchmark_ma200.loc[dt]:
                    target *= 0.5

            turnover = float((target - weights_after).abs().sum())
            cost = turnover * (TOTAL_COST_BPS / 10000.0)
            weights_prev = target

            if not picked.empty:
                info = meta.reindex(picked.index).copy()
                info.insert(0, "weight", target.reindex(picked.index).values)
                info.insert(1, "score", picked.values)
                info.insert(2, "revision_3m", revision.reindex(picked.index).values)
                info.insert(3, "earnings_yield", earnings_yield.reindex(picked.index).values)
                info.insert(4, "momentum_6m", mom_6m.reindex(picked.index).values)
                selected_names[dt] = info.reset_index().rename(columns={"index": "sedol"})
        else:
            weights_prev = weights_after

        portfolio_rets.append(gross - cost)
        cost_series.append(cost)
        turnover_series.append(turnover)

    daily_net = pd.Series(portfolio_rets, index=prices.index, name="portfolio_return")
    trading_cost = pd.Series(cost_series, index=prices.index, name="trading_cost")
    turnover = pd.Series(turnover_series, index=prices.index, name="turnover")
    nav = (1 + daily_net).cumprod().rename("nav")
    drawdown = (nav / nav.cummax() - 1).rename("drawdown")
    monthly_net = daily_net.resample("ME").apply(lambda x: (1 + x).prod() - 1).rename("monthly_return")

    metrics = compute_metrics(daily_net, turnover[turnover > 0])
    daily_df = pd.concat([daily_net, trading_cost, turnover, nav, drawdown], axis=1)
    daily_df.to_csv(output_dir / "daily_portfolio_series.csv", index_label="date")
    monthly_net.to_csv(output_dir / "monthly_portfolio_returns.csv", index_label="date")

    if selected_names:
        last_dt = max(selected_names.keys())
        last_holdings = selected_names[last_dt].sort_values(["weight", "score"], ascending=[False, False])
        last_holdings.to_csv(output_dir / "last_holdings.csv", index=False)
        final_holdings_count = len(last_holdings)
    else:
        last_dt = None
        last_holdings = pd.DataFrame(columns=["sedol", "weight", "score", "ticker", "company_name"])
        last_holdings.to_csv(output_dir / "last_holdings.csv", index=False)
        final_holdings_count = 0

    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    progress_note = f"""# Progress Note - {variant_name}

- Universe: {UNIVERSE} monthly constituents
- Signal family: {variant['combo']}
- Inputs used: trailing price (`close_tr`), forward 12m EPS, estimate count, dollar volume, market cap, GICS sector
- Rebalance: monthly using last available trading day
- Selection: top {int(variant['top_pct'] * 100)}% names after liquidity/estimate filters
- Market regime: {'half exposure below SP50 200DMA' if variant['market_half'] else 'always on'}
- Total trading cost: {TOTAL_COST_BPS}bp including slippage
- Backtest window: {metrics['start']} ~ {metrics['end']}
- Final holdings count: {final_holdings_count}
- Last rebalance: {str(last_dt.date()) if last_dt is not None else 'N/A'}

## Economic rationale
- Upward forward EPS revisions proxy improving fundamentals and under-reacted analyst information.
- Earnings yield rewards cheaper forward expectations for a given price.
- Optional 6m momentum helps avoid value traps and keep names with confirming price action.
"""
    (output_dir / "progress_note.md").write_text(progress_note, encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), constrained_layout=True)
    axes[0].plot(nav.index, nav.values, label="Portfolio NAV", color="#1f77b4", linewidth=2)
    axes[0].set_title(f"{variant_name} - cumulative return")
    axes[0].set_ylabel("NAV")
    axes[0].legend(loc="upper left")
    axes[1].fill_between(drawdown.index, drawdown.values, 0, color="#d62728", alpha=0.25)
    axes[1].plot(drawdown.index, drawdown.values, color="#d62728", linewidth=1.8)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown")
    fig.savefig(output_dir / "cumulative_return_and_drawdown.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)
    axes[0].hist(daily_net.dropna(), bins=60, color="#1f77b4", alpha=0.75, edgecolor="white")
    axes[0].set_title("Daily Portfolio Return Distribution")
    axes[0].set_xlabel("Daily return")
    axes[1].hist(monthly_net.dropna(), bins=40, color="#ff7f0e", alpha=0.75, edgecolor="white")
    axes[1].set_title("Monthly Portfolio Return Distribution")
    axes[1].set_xlabel("Monthly return")
    fig.savefig(output_dir / "return_distributions.png", dpi=160)
    plt.close(fig)

    summary = {
        "metrics": metrics,
        "variant": variant_name,
        "output_dir": str(output_dir),
        "cumulative_chart": str(output_dir / "cumulative_return_and_drawdown.png"),
        "distribution_chart": str(output_dir / "return_distributions.png"),
        "last_holdings_path": str(output_dir / "last_holdings.csv"),
        "progress_note_path": str(output_dir / "progress_note.md"),
        "filters": {
            "min_dollar_volume": MIN_DOLLAR_VOLUME,
            "min_marketcap_units": MIN_MARKETCAP_UNITS,
            "min_estimates": MIN_ESTIMATES,
            "total_cost_bps": TOTAL_COST_BPS,
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=sorted(VARIANTS), required=True)
    args = parser.parse_args()
    run_variant(args.variant)
