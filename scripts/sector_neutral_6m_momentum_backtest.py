from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from topquant_ksk.db.tunnel import manage_db_tunnel, kill_tunnel

from src.common.quant_db import load_quant_db_credentials

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / 'outputs' / 'spy_sector_neutral_6m_momentum'
OUTDIR.mkdir(parents=True, exist_ok=True)

COST_BPS = 15
LOOKBACK_DAYS = 126  # 6-0 momentum
TOP_PCT = 0.20
UNIVERSE = 'SPY-US'


def connect_engine():
    creds = load_quant_db_credentials(ROOT)
    tunnel = manage_db_tunnel()
    uri = f"postgresql://{creds.user}:{quote_plus(creds.password)}@127.0.0.1:15432/quant_data"
    engine = create_engine(uri)
    return tunnel, engine


def fetch_data(engine):
    q_const = text("""
        SELECT time, sedol, ticker, company_name
        FROM public.monthly_etf_constituents
        WHERE universe_name = :universe
        ORDER BY time, sedol
    """)
    with engine.connect() as conn:
        const = pd.read_sql(q_const, conn, params={'universe': UNIVERSE}, parse_dates=['time'])

        sedols = sorted(const['sedol'].dropna().unique().tolist())
        min_time = const['time'].min()
        if not sedols:
            raise RuntimeError('No constituents found for universe')

        q_sector = text("""
            SELECT time, sedol, gics_level1_sector
            FROM public.monthly_time_series_data_stock
            WHERE sedol = ANY(:sedols)
              AND time >= :min_time
            ORDER BY time, sedol
        """)
        q_price = text("""
            SELECT time, sedol, close_tr
            FROM public.daily_adjusted_time_series_data_stock
            WHERE sedol = ANY(:sedols)
              AND time >= :min_time
            ORDER BY time, sedol
        """)
        sector = pd.read_sql(q_sector, conn, params={'sedols': sedols, 'min_time': min_time}, parse_dates=['time'])
        price = pd.read_sql(q_price, conn, params={'sedols': sedols, 'min_time': min_time}, parse_dates=['time'])
    return const, sector, price


def build_membership(const):
    const = const.copy()
    const['time'] = pd.to_datetime(const['time'], utc=True)
    return {
        dt: grp[['sedol', 'ticker', 'company_name']].drop_duplicates('sedol').set_index('sedol')
        for dt, grp in const.groupby('time')
    }


def build_sector_map(sector):
    sector = sector.copy()
    sector['time'] = pd.to_datetime(sector['time'], utc=True)
    sector = sector.sort_values(['time', 'sedol'])
    return {
        dt: grp[['sedol', 'gics_level1_sector']].drop_duplicates('sedol').set_index('sedol')['gics_level1_sector']
        for dt, grp in sector.groupby('time')
    }


def make_price_wide(price):
    price = price.copy()
    price['time'] = pd.to_datetime(price['time'], utc=True)
    price = price.dropna(subset=['close_tr'])
    wide = price.pivot_table(index='time', columns='sedol', values='close_tr', aggfunc='last').sort_index()
    tickers = price.drop_duplicates('sedol').set_index('sedol')['ticker']
    names = price.drop_duplicates('sedol').set_index('sedol')['company_name']
    return wide, tickers, names


def last_on_or_before(sorted_dates, dt):
    dt = pd.Timestamp(dt)
    pos = sorted_dates.searchsorted(dt, side='right') - 1
    if pos < 0:
        return None
    return sorted_dates[pos]


def compute_weights(rebal_date, reb_idx, prices, membership_map, membership_dates, sector_map, sector_dates):
    if reb_idx - LOOKBACK_DAYS < 0:
        return pd.Series(dtype=float)

    const_dt = last_on_or_before(membership_dates, rebal_date)
    sect_dt = last_on_or_before(sector_dates, rebal_date)
    if const_dt is None or sect_dt is None:
        return pd.Series(dtype=float)

    members = membership_map[const_dt].index
    sectors = sector_map[sect_dt]
    px_now = prices.iloc[reb_idx]
    px_past = prices.iloc[reb_idx - LOOKBACK_DAYS]
    mom = px_now / px_past - 1.0
    eligible = mom.reindex(members).dropna()
    if eligible.empty:
        return pd.Series(dtype=float)

    sector_series = sectors.reindex(eligible.index).dropna()
    eligible = eligible.reindex(sector_series.index)
    if eligible.empty:
        return pd.Series(dtype=float)

    selected = []
    for sec, sec_mom in eligible.groupby(sector_series):
        n = len(sec_mom)
        k = max(1, int(np.ceil(n * TOP_PCT)))
        picked = sec_mom.sort_values(ascending=False).head(k)
        selected.append(picked)

    if not selected:
        return pd.Series(dtype=float)

    selected = pd.concat(selected)
    selected_sector = sector_series.reindex(selected.index)
    sector_names = selected_sector.dropna().unique().tolist()
    if not sector_names:
        return pd.Series(dtype=float)

    weights = pd.Series(0.0, index=selected.index)
    sector_weight = 1.0 / len(sector_names)
    for sec in sector_names:
        names = selected.index[selected_sector == sec]
        weights.loc[names] = sector_weight / len(names)
    return weights[weights > 0]


def run_backtest(prices, membership_map, membership_dates, sector_map, sector_dates):
    returns = prices.pct_change().fillna(0.0)
    month_ends = prices.index.to_series().groupby(prices.index.to_period('M')).max()
    rebal_dates = month_ends.tolist()

    weights_by_date = {}
    turnover_by_date = {}
    holdings_by_date = {}
    notes = []

    current_w = pd.Series(0.0, index=prices.columns)
    daily_ret = pd.Series(index=prices.index, dtype=float)
    cost_series = pd.Series(0.0, index=prices.index, dtype=float)

    rebal_set = set(rebal_dates)
    for i, dt in enumerate(prices.index):
        gross = float((current_w * returns.loc[dt].reindex(current_w.index).fillna(0.0)).sum())
        daily_ret.loc[dt] = gross
        post_w = current_w * (1.0 + returns.loc[dt].reindex(current_w.index).fillna(0.0))
        denom = 1.0 + gross
        if abs(denom) > 1e-12:
            post_w = post_w / denom
        else:
            post_w = post_w * 0.0

        if dt in rebal_set:
            target_sparse = compute_weights(dt, i, prices, membership_map, membership_dates, sector_map, sector_dates)
            target_w = pd.Series(0.0, index=prices.columns)
            if not target_sparse.empty:
                target_w.loc[target_sparse.index] = target_sparse.values
            turnover = float((target_w - post_w).abs().sum())
            cost = turnover * (COST_BPS / 10000.0)
            daily_ret.loc[dt] = daily_ret.loc[dt] - cost
            cost_series.loc[dt] = cost
            current_w = target_w
            weights_by_date[dt] = target_sparse.sort_values(ascending=False)
            turnover_by_date[dt] = turnover
            holdings_by_date[dt] = len(target_sparse)
            notes.append((dt, len(target_sparse), turnover))
        else:
            current_w = post_w

    nav = (1.0 + daily_ret).cumprod()
    dd = nav / nav.cummax() - 1.0
    monthly_ret = nav.resample('ME').last().pct_change().dropna()

    return {
        'daily_ret': daily_ret,
        'monthly_ret': monthly_ret,
        'nav': nav,
        'dd': dd,
        'weights_by_date': weights_by_date,
        'turnover_by_date': turnover_by_date,
        'holdings_by_date': holdings_by_date,
        'notes': notes,
    }


def summarize(bt, tickers, names):
    daily = bt['daily_ret'].dropna()
    monthly = bt['monthly_ret'].dropna()
    nav = bt['nav'].dropna()
    dd = bt['dd'].dropna()
    years = len(daily) / 252.0
    cagr = nav.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    vol = daily.std() * np.sqrt(252)
    sharpe = daily.mean() / daily.std() * np.sqrt(252) if daily.std() > 0 else np.nan
    mdd = dd.min()
    calmar = cagr / abs(mdd) if mdd < 0 else np.nan

    best_day = daily.idxmax(); worst_day = daily.idxmin()
    best_month = monthly.idxmax(); worst_month = monthly.idxmin()
    trough = dd.idxmin()
    peak = nav.loc[:trough].idxmax()

    last_rebal = max(bt['weights_by_date'].keys())
    last_hold = bt['weights_by_date'][last_rebal].rename('weight').to_frame()
    last_hold['ticker'] = last_hold.index.map(tickers)
    last_hold['company_name'] = last_hold.index.map(names)

    turnover = pd.Series(bt['turnover_by_date']).sort_index()

    summary = {
        'start': str(nav.index[0].date()),
        'end': str(nav.index[-1].date()),
        'final_nav': float(nav.iloc[-1]),
        'cumulative_return': float(nav.iloc[-1] - 1),
        'cagr': float(cagr),
        'volatility': float(vol),
        'sharpe': float(sharpe),
        'mdd': float(mdd),
        'calmar': float(calmar),
        'daily_win_rate': float((daily > 0).mean()),
        'monthly_win_rate': float((monthly > 0).mean()),
        'avg_monthly_turnover': float(turnover.mean()),
        'median_monthly_turnover': float(turnover.median()),
        'rebalance_count': int(len(turnover)),
        'final_holdings_count': int(len(last_hold)),
        'best_day': [str(best_day.date()), float(daily.loc[best_day])],
        'worst_day': [str(worst_day.date()), float(daily.loc[worst_day])],
        'best_month': [str(best_month.date()), float(monthly.loc[best_month])],
        'worst_month': [str(worst_month.date()), float(monthly.loc[worst_month])],
        'peak_before_mdd': str(peak.date()),
        'mdd_trough': str(trough.date()),
        'last_rebalance': str(last_rebal.date()),
    }
    return summary, last_hold, turnover


def make_plots(bt, summary):
    nav = bt['nav']; dd = bt['dd']; daily = bt['daily_ret'].dropna(); monthly = bt['monthly_ret'].dropna()
    best_day_dt = pd.Timestamp(summary['best_day'][0], tz='UTC')
    worst_day_dt = pd.Timestamp(summary['worst_day'][0], tz='UTC')
    peak_dt = pd.Timestamp(summary['peak_before_mdd'], tz='UTC')
    trough_dt = pd.Timestamp(summary['mdd_trough'], tz='UTC')

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios':[2,1]})
    axes[0].plot(nav.index, nav.values, color='navy', lw=2, label='NAV')
    axes[0].scatter([best_day_dt], [nav.loc[best_day_dt]], color='green', s=50, zorder=5)
    axes[0].scatter([worst_day_dt], [nav.loc[worst_day_dt]], color='red', s=50, zorder=5)
    axes[0].scatter([peak_dt, trough_dt], [nav.loc[peak_dt], nav.loc[trough_dt]], color=['orange','black'], s=45, zorder=5)
    axes[0].annotate(f"Best day\n{summary['best_day'][0]}\n{summary['best_day'][1]:.2%}", (best_day_dt, nav.loc[best_day_dt]), xytext=(10,10), textcoords='offset points', fontsize=9)
    axes[0].annotate(f"Worst day\n{summary['worst_day'][0]}\n{summary['worst_day'][1]:.2%}", (worst_day_dt, nav.loc[worst_day_dt]), xytext=(10,-35), textcoords='offset points', fontsize=9)
    axes[0].set_title('SPY-US Sector-Neutral 6M Momentum (Fast Experiment)')
    axes[0].set_ylabel('NAV')
    axes[0].legend(loc='upper left')

    axes[1].fill_between(dd.index, dd.values, 0, color='firebrick', alpha=0.35)
    axes[1].axvline(peak_dt, color='orange', ls='--', lw=1)
    axes[1].axvline(trough_dt, color='black', ls='--', lw=1)
    axes[1].set_title('Drawdown')
    axes[1].set_ylabel('DD')
    axes[1].set_xlabel('Date')
    fig.tight_layout()
    fig.savefig(OUTDIR / 'cumulative_return_and_drawdown.png', dpi=160, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(daily.values, bins=50, color='steelblue', edgecolor='white')
    axes[0].axvline(daily.mean(), color='red', ls='--', lw=1.5)
    axes[0].set_title('Daily Return Histogram')
    axes[0].set_xlabel('Daily return')
    axes[0].set_ylabel('Frequency')

    axes[1].hist(monthly.values, bins=35, color='darkseagreen', edgecolor='white')
    axes[1].axvline(monthly.mean(), color='red', ls='--', lw=1.5)
    axes[1].set_title('Monthly Return Histogram')
    axes[1].set_xlabel('Monthly return')
    axes[1].set_ylabel('Frequency')
    fig.tight_layout()
    fig.savefig(OUTDIR / 'return_histograms.png', dpi=160, bbox_inches='tight')
    plt.close(fig)


def save_outputs(bt, summary, last_hold, turnover):
    bt['daily_ret'].rename('daily_return').to_csv(OUTDIR / 'daily_returns.csv')
    bt['monthly_ret'].rename('monthly_return').to_csv(OUTDIR / 'monthly_returns.csv')
    pd.DataFrame({'nav': bt['nav'], 'drawdown': bt['dd'], 'cost': bt['daily_ret']*0 + 0}).to_csv(OUTDIR / 'nav_drawdown.csv')
    last_hold.to_csv(OUTDIR / 'last_holdings.csv', index_label='sedol')
    turnover.rename('turnover').to_csv(OUTDIR / 'turnover.csv')
    pd.Series(summary).to_json(OUTDIR / 'summary.json', force_ascii=False, indent=2)
    with open(OUTDIR / 'progress_note.md', 'w', encoding='utf-8') as f:
        f.write('# Progress Note - SPY-US Sector-Neutral 6M Momentum\n\n')
        f.write('- Universe: SPY-US monthly constituents\n')
        f.write('- Signal: trailing 6-month total return (6-0) using `close_tr`\n')
        f.write('- Sector neutralization: equal weight across GICS level1 sectors, equal weight within selected names\n')
        f.write('- Selection: top 20% within each sector\n')
        f.write('- Rebalance: monthly using last available trading day\n')
        f.write('- Cost: 15bp x one-way turnover\n')
        f.write(f"- Backtest window: {summary['start']} ~ {summary['end']}\n")
        f.write(f"- Rebalance count: {summary['rebalance_count']}\n")
        f.write(f"- Final holdings count: {summary['final_holdings_count']}\n")


def main():
    tunnel = None
    try:
        tunnel, engine = connect_engine()
        const, sector, price = fetch_data(engine)
        membership_map = build_membership(const)
        membership_dates = pd.DatetimeIndex(sorted(membership_map.keys()))
        sector_map = build_sector_map(sector)
        sector_dates = pd.DatetimeIndex(sorted(sector_map.keys()))
        prices, tickers, names = make_price_wide(price)
        bt = run_backtest(prices, membership_map, membership_dates, sector_map, sector_dates)
        summary, last_hold, turnover = summarize(bt, tickers, names)
        make_plots(bt, summary)
        save_outputs(bt, summary, last_hold, turnover)
        print(summary)
        print(f"saved_to={OUTDIR}")
    finally:
        if tunnel is not None:
            kill_tunnel(tunnel)

if __name__ == '__main__':
    main()
