from __future__ import annotations

import json
import math
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from topquant_ksk.db import DBConnection


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "spy_momentum_top10"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def make_connection() -> DBConnection:
    load_env(ROOT / ".env")
    user = os.getenv("QUANT_DB_USER")
    password = os.getenv("QUANT_DB_PASSWORD")
    if not user or not password:
        raise RuntimeError("QUANT_DB_USER / QUANT_DB_PASSWORD not found")
    return DBConnection(db_user=user, db_password=password, local_host=False)


def compute_metrics(daily_net: pd.Series, turnover: pd.Series) -> dict[str, float | str]:
    daily_net = daily_net.dropna()
    if daily_net.empty:
        raise RuntimeError("No returns computed")

    nav = (1 + daily_net).cumprod()
    dd = nav / nav.cummax() - 1
    months = daily_net.resample("ME").apply(lambda x: (1 + x).prod() - 1)

    ann_factor = 252
    total_return = nav.iloc[-1] - 1
    ann_return = nav.iloc[-1] ** (ann_factor / len(daily_net)) - 1
    ann_vol = daily_net.std(ddof=0) * math.sqrt(ann_factor)
    sharpe = daily_net.mean() / daily_net.std(ddof=0) * math.sqrt(ann_factor) if daily_net.std(ddof=0) > 0 else np.nan
    max_dd = dd.min()
    calmar = ann_return / abs(max_dd) if max_dd < 0 else np.nan
    hit_ratio_daily = (daily_net > 0).mean()
    hit_ratio_monthly = (months > 0).mean()

    return {
        "start": str(daily_net.index.min().date()),
        "end": str(daily_net.index.max().date()),
        "n_days": int(len(daily_net)),
        "n_months": int(len(months)),
        "total_return": float(total_return),
        "annual_return": float(ann_return),
        "annual_vol": float(ann_vol),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_dd),
        "calmar": float(calmar),
        "daily_hit_ratio": float(hit_ratio_daily),
        "monthly_hit_ratio": float(hit_ratio_monthly),
        "avg_monthly_turnover": float(turnover.mean()),
        "median_monthly_turnover": float(turnover.median()),
        "best_day": str(daily_net.idxmax().date()),
        "best_day_return": float(daily_net.max()),
        "worst_day": str(daily_net.idxmin().date()),
        "worst_day_return": float(daily_net.min()),
        "best_month": str(months.idxmax().date()),
        "best_month_return": float(months.max()),
        "worst_month": str(months.idxmin().date()),
        "worst_month_return": float(months.min()),
    }


def main() -> None:
    conn = make_connection()

    universe = conn.download.fetch_universe_mask("SPY-US")
    universe = universe.sort_index()
    sedols = universe.columns.get_level_values("sedol").tolist()
    latest_meta = pd.DataFrame(
        {
            "ticker": universe.columns.get_level_values("ticker"),
            "company_name": universe.columns.get_level_values("company_name"),
            "sedol": universe.columns.get_level_values("sedol"),
        }
    ).drop_duplicates("sedol").set_index("sedol")

    prices_raw = conn.download.fetch_timeseries_table(
        table_name="public.daily_adjusted_time_series_data_stock",
        columns=["sedol"],
        item_names=["close_tr"],
        sedols=sedols,
        start_date=str(universe.index.min().date()),
        end_date=None,
    ).sort_index()

    prices = prices_raw.xs("close_tr", axis=1, level="item_name")
    prices = prices.sort_index().sort_index(axis=1)
    prices.index = pd.to_datetime(prices.index).tz_localize(None)

    universe.index = pd.to_datetime(universe.index).tz_localize(None)
    universe.columns = universe.columns.get_level_values("sedol")
    universe = universe.sort_index().sort_index(axis=1)

    common_sedols = prices.columns.intersection(universe.columns)
    prices = prices[common_sedols]
    universe = universe[common_sedols]
    latest_meta = latest_meta.loc[common_sedols]

    daily_rets = prices.pct_change()
    month_end_dates = prices.groupby(prices.index.to_period("M")).apply(lambda x: x.index[-1])
    month_end_dates = pd.DatetimeIndex(month_end_dates.tolist())

    lookback_trading_days = 252
    rebalance_dates: list[pd.Timestamp] = []
    target_weights: dict[pd.Timestamp, pd.Series] = {}
    selected_names: dict[pd.Timestamp, pd.DataFrame] = {}

    for dt in month_end_dates:
        loc = prices.index.get_indexer([dt])[0]
        if loc < lookback_trading_days:
            continue
        hist_dt = prices.index[loc - lookback_trading_days]
        mom = prices.loc[dt] / prices.loc[hist_dt] - 1

        month_mask = universe.loc[universe.index[universe.index <= dt].max()]
        eligible = month_mask[month_mask].index
        score = mom.loc[eligible].replace([np.inf, -np.inf], np.nan).dropna()
        if score.empty:
            continue
        n_select = max(1, int(math.ceil(len(score) * 0.10)))
        chosen = score.sort_values(ascending=False).head(n_select)
        w = pd.Series(0.0, index=prices.columns)
        w.loc[chosen.index] = 1.0 / len(chosen)

        rebalance_dates.append(dt)
        target_weights[dt] = w
        info = latest_meta.loc[chosen.index].copy()
        info.insert(0, "weight", 1.0 / len(chosen))
        info.insert(1, "signal_12m", chosen.values)
        selected_names[dt] = info.reset_index().rename(columns={"index": "sedol"})

    rebal_set = set(rebalance_dates)
    start_dt = rebalance_dates[0]
    daily_rets = daily_rets.loc[start_dt:]

    weights_prev = pd.Series(0.0, index=prices.columns)
    portfolio_rets = []
    cost_series = []
    turnover_series = []

    for dt in daily_rets.index:
        gross = float((weights_prev * daily_rets.loc[dt].fillna(0.0)).sum())
        weights_after = weights_prev * (1 + daily_rets.loc[dt].fillna(0.0))
        gross_nav = weights_after.sum()
        if gross_nav > 0:
            weights_after = weights_after / gross_nav
        else:
            weights_after = pd.Series(0.0, index=weights_prev.index)

        cost = 0.0
        turnover = 0.0
        if dt in rebal_set:
            w_target = target_weights[dt]
            turnover = float((w_target - weights_after).abs().sum())
            cost = turnover * 0.0015
            weights_prev = w_target.copy()
        else:
            weights_prev = weights_after.copy()

        portfolio_rets.append(gross - cost)
        cost_series.append(cost)
        turnover_series.append(turnover)

    daily_net = pd.Series(portfolio_rets, index=daily_rets.index, name="portfolio_return")
    trading_cost = pd.Series(cost_series, index=daily_rets.index, name="trading_cost")
    turnover = pd.Series(turnover_series, index=daily_rets.index, name="turnover")

    nav = (1 + daily_net).cumprod().rename("nav")
    drawdown = (nav / nav.cummax() - 1).rename("drawdown")
    monthly_net = daily_net.resample("ME").apply(lambda x: (1 + x).prod() - 1).rename("monthly_return")

    best_month_dt = monthly_net.idxmax()
    worst_month_dt = monthly_net.idxmin()
    best_month_nav_dt = nav.index[nav.index.get_indexer([best_month_dt], method="pad")][0]
    worst_month_nav_dt = nav.index[nav.index.get_indexer([worst_month_dt], method="pad")][0]

    peak_dt = nav.loc[: drawdown.idxmin()].idxmax()
    trough_dt = drawdown.idxmin()

    metrics = compute_metrics(daily_net, turnover[turnover > 0])

    daily_df = pd.concat([daily_net, trading_cost, turnover, nav, drawdown], axis=1)
    daily_df.to_csv(OUTPUT_DIR / "daily_portfolio_series.csv", index_label="date")
    monthly_net.to_csv(OUTPUT_DIR / "monthly_portfolio_returns.csv", index_label="date")

    last_holdings = selected_names[rebalance_dates[-1]].sort_values(["weight", "signal_12m"], ascending=[False, False])
    last_holdings.to_csv(OUTPUT_DIR / "last_holdings.csv", index=False)

    with open(OUTPUT_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    progress_note = f"""# Progress Note - SPY-US 12M Momentum Top 10%

- Universe: SPY-US monthly constituents
- Signal: trailing 12-month total return (`close_tr`)
- Rebalance: monthly, using last available trading day in daily price data
- Selection: top 10% of eligible names, equal-weight
- Trading cost: 15bp × one-way turnover at each rebalance
- Price field: `public.daily_adjusted_time_series_data_stock.close_tr`
- Backtest window: {metrics['start']} ~ {metrics['end']}
- Rebalance count: {len(rebalance_dates)}
- Final holdings count: {len(last_holdings)}

## Notes
- Universe membership is taken from the most recent SPY-US monthly constituent snapshot available on or before each rebalance date.
- Daily portfolio returns are computed from prior close weights, then rebalanced at month-end close with turnover cost deducted on the rebalance date.
- Initial entry also incurs trading cost through turnover from cash to target weights.
"""
    (OUTPUT_DIR / "progress_note.md").write_text(progress_note, encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False, constrained_layout=True)

    axes[0].plot(nav.index, nav.values, label="Portfolio NAV", color="#1f77b4", linewidth=2)
    axes[0].scatter(best_month_nav_dt, nav.loc[best_month_nav_dt], color="green", s=60, zorder=3)
    axes[0].scatter(worst_month_nav_dt, nav.loc[worst_month_nav_dt], color="red", s=60, zorder=3)
    axes[0].annotate(
        f"Best month\n{best_month_dt.strftime('%Y-%m')}\n{monthly_net.loc[best_month_dt]:.2%}",
        (best_month_nav_dt, nav.loc[best_month_nav_dt]),
        textcoords="offset points", xytext=(10, 10), fontsize=9,
    )
    axes[0].annotate(
        f"Worst month\n{worst_month_dt.strftime('%Y-%m')}\n{monthly_net.loc[worst_month_dt]:.2%}",
        (worst_month_nav_dt, nav.loc[worst_month_nav_dt]),
        textcoords="offset points", xytext=(10, -35), fontsize=9,
    )
    axes[0].set_title("SPY-US 12M Momentum Top 10% Equal Weight - Cumulative Return")
    axes[0].set_ylabel("NAV")
    axes[0].legend(loc="upper left")

    axes[1].fill_between(drawdown.index, drawdown.values, 0, color="#d62728", alpha=0.25)
    axes[1].plot(drawdown.index, drawdown.values, color="#d62728", linewidth=1.8)
    axes[1].scatter(peak_dt, drawdown.loc[peak_dt], color="orange", s=50, zorder=3)
    axes[1].scatter(trough_dt, drawdown.loc[trough_dt], color="red", s=60, zorder=3)
    axes[1].annotate(
        f"Peak before max DD\n{peak_dt.date()}",
        (peak_dt, drawdown.loc[peak_dt]),
        textcoords="offset points", xytext=(10, 10), fontsize=9,
    )
    axes[1].annotate(
        f"Max DD trough\n{trough_dt.date()}\n{drawdown.loc[trough_dt]:.2%}",
        (trough_dt, drawdown.loc[trough_dt]),
        textcoords="offset points", xytext=(10, -35), fontsize=9,
    )
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown")
    fig.savefig(OUTPUT_DIR / "cumulative_return_and_drawdown.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)
    axes[0].hist(daily_net.dropna(), bins=60, color="#1f77b4", alpha=0.75, edgecolor="white")
    axes[0].axvline(daily_net.mean(), color="black", linestyle="--", linewidth=1.2, label=f"Mean {daily_net.mean():.3%}")
    axes[0].set_title("Daily Portfolio Return Distribution")
    axes[0].set_xlabel("Daily return")
    axes[0].legend()

    axes[1].hist(monthly_net.dropna(), bins=40, color="#ff7f0e", alpha=0.75, edgecolor="white")
    axes[1].axvline(monthly_net.mean(), color="black", linestyle="--", linewidth=1.2, label=f"Mean {monthly_net.mean():.3%}")
    axes[1].set_title("Monthly Portfolio Return Distribution")
    axes[1].set_xlabel("Monthly return")
    axes[1].legend()
    fig.savefig(OUTPUT_DIR / "return_distributions.png", dpi=160)
    plt.close(fig)

    summary = {
        "metrics": metrics,
        "rebalance_dates": [str(x.date()) for x in rebalance_dates],
        "output_dir": str(OUTPUT_DIR),
        "cumulative_chart": str(OUTPUT_DIR / "cumulative_return_and_drawdown.png"),
        "distribution_chart": str(OUTPUT_DIR / "return_distributions.png"),
        "last_holdings_path": str(OUTPUT_DIR / "last_holdings.csv"),
        "progress_note_path": str(OUTPUT_DIR / "progress_note.md"),
    }
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
