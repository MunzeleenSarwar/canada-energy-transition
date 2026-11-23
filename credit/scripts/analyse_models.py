"""Part B models: Altman Z-prime, Springate, Zmijewski, Merton distance to
default, synthetic rating from interest coverage. Model year is 2024, to
match the scorecard year. All money in CAD millions.
Merton is point-in-time at 31 Dec 2024: 1-year daily price volatility over
2024, market value at the 31 Dec 2024 close times current shares outstanding
(an approximation, stated in the report), default point from 2024
liabilities, risk free rate 3.0% (1-year Government of Canada yield area).
Teck's 2024 EBIT of $57m includes a $1,053m write-off, so an adjusted view
(EBIT plus the write-off) is computed alongside the reported view.
"""
import pathlib
from math import erf, log, sqrt

import numpy as np
import pandas as pd
import yfinance as yf

base = pathlib.Path(__file__).resolve().parents[1]
fin = pd.read_csv(base / "data" / "financials.csv")
met = pd.read_csv(base / "data" / "metrics.csv")
met24 = met[met.fiscal_year_end.str.startswith("2024")].set_index("ticker")
TECK_WRITEOFF = 1053.0  # CAD millions, 2024 write-off in Teck's income statement


def norm_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def synthetic_rating(cov):
    bands = [(8.5, "AAA"), (6.5, "AA"), (5.5, "A+"), (4.25, "A"), (3.0, "A-"),
             (2.5, "BBB"), (2.0, "BB+"), (1.75, "BB"), (1.5, "B+"),
             (1.25, "B"), (0.8, "B-")]
    for cut, r in bands:
        if cov >= cut:
            return r
    return "CCC or lower"


rows = []
for tick, g in fin.sort_values("fiscal_year_end").groupby("ticker"):
    r = g[g.fiscal_year_end.str.startswith("2024")].iloc[0]
    ta, wc, re_, ebit, rev = r.total_assets, r.working_capital, r.retained_earnings, r.ebit, r.revenue
    eq, tl, cl = r.equity, r.total_liabilities, r.current_liabilities
    ni = r.net_income
    ebit_adj = ebit + TECK_WRITEOFF if tick == "TECK-B" else np.nan
    zprime = 6.56 * (wc / ta) + 3.26 * (re_ / ta) + 6.72 * (ebit / ta) + 1.05 * (eq / tl) if ta and tl else np.nan
    zprime_adj = (6.56 * (wc / ta) + 3.26 * (re_ / ta) + 6.72 * (ebit_adj / ta) + 1.05 * (eq / tl)
                  if tick == "TECK-B" and ta and tl else np.nan)
    springate = 1.03 * (wc / ta) + 3.07 * (ebit / ta) + 0.66 * (ebit / cl) + 0.4 * (rev / ta) if ta and cl else np.nan
    springate_adj = (1.03 * (wc / ta) + 3.07 * (ebit_adj / ta) + 0.66 * (ebit_adj / cl) + 0.4 * (rev / ta)
                     if tick == "TECK-B" and ta and cl else np.nan)
    roa = ni / ta if ta else np.nan
    zm_score = -4.336 - 4.513 * roa + 5.679 * (tl / ta) + 0.004 * (r.current_assets / cl) if ta and cl else np.nan
    zm_prob = 1 / (1 + np.exp(-zm_score)) if not np.isnan(zm_score) else np.nan
    # Merton at 31 Dec 2024
    t = yf.Ticker(tick + ".TO")
    hist = t.history(start="2024-01-01", end="2025-01-01", auto_adjust=True)
    rets = np.log(hist["Close"] / hist["Close"].shift(1)).dropna()
    eq_vol = rets.std() * sqrt(252) if len(rets) > 50 else np.nan
    close_2024 = float(hist["Close"].iloc[-1]) if len(hist) else np.nan
    shares = t.info.get("sharesOutstanding", np.nan)
    mcap = close_2024 * shares / 1e6 if pd.notna(close_2024) and pd.notna(shares) else np.nan
    V = mcap + tl
    sigma_a = eq_vol * (mcap / V) if V else np.nan
    default_point = cl + 0.5 * (tl - cl)
    rf = 0.03
    dd = (log(V / default_point) + (rf - 0.5 * sigma_a ** 2)) / sigma_a if sigma_a and default_point else np.nan
    edf = norm_cdf(-dd) * 100 if not np.isnan(dd) else np.nan
    cov = met24.loc[tick].interest_coverage
    rows.append(dict(ticker=tick, company=r.company, fiscal_year_end=r.fiscal_year_end,
                     altman_zprime=zprime, altman_zprime_adj=zprime_adj,
                     springate=springate, springate_adj=springate_adj,
                     zmijewski_prob_pct=zm_prob * 100 if not np.isnan(zm_prob) else np.nan,
                     equity_vol_pct=eq_vol * 100 if not np.isnan(eq_vol) else np.nan,
                     asset_vol_pct=sigma_a * 100 if not np.isnan(sigma_a) else np.nan,
                     market_cap_2024_cad_m=mcap, default_point_cad_m=default_point,
                     merton_dd=dd, merton_edf_pct=edf,
                     interest_coverage=cov,
                     interest_coverage_adj=(ebit_adj / r.interest_expense
                                            if tick == "TECK-B" and r.interest_expense else np.nan),
                     synthetic_rating=synthetic_rating(cov),
                     debt_ebitda=met24.loc[tick].debt_ebitda,
                     ocf_to_debt=(r.operating_cash_flow / r.total_debt) if r.total_debt else np.nan,
                     debt_to_assets=(r.total_debt / ta) if ta else np.nan,
                     liabilities_to_assets=(tl / ta) if ta else np.nan))
df = pd.DataFrame(rows)
df.to_csv(base / "data" / "models.csv", index=False)
print(df[["ticker", "altman_zprime", "altman_zprime_adj", "springate", "springate_adj",
          "zmijewski_prob_pct", "merton_dd", "merton_edf_pct", "synthetic_rating",
          "debt_ebitda", "interest_coverage"]].to_string(index=False))
