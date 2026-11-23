"""Part B: download annual financials for the 12 TSX resource companies
(scorecard universe) via yfinance and compute plain credit risk metrics.
Mirrors the US AI credit risk project. All money in CAD millions.
Companies reporting in USD (Barrick, Agnico, Nutrien, Methanex, West Fraser)
are converted at the USD/CAD close on 31 Dec 2024, taken from CAD=X.
Ratios are currency free and are unchanged by the conversion.
Model year is 2024; earlier years are kept for trend context.
"""
import pathlib

import numpy as np
import pandas as pd
import yfinance as yf

base = pathlib.Path(__file__).resolve().parents[1]
TICKERS = {
    "CNQ": "Canadian Natural Resources", "SU": "Suncor", "CVE": "Cenovus",
    "TOU": "Tourmaline", "IMO": "Imperial Oil", "ABX": "Barrick",
    "AEM": "Agnico Eagle", "TECK-B": "Teck Resources", "CCO": "Cameco",
    "NTR": "Nutrien", "MX": "Methanex", "WFG": "West Fraser Timber",
}
USD_REPORTERS = {"ABX", "AEM", "NTR", "MX", "WFG"}

fx_hist = yf.Ticker("CAD=X").history(start="2024-12-30", end="2025-01-02",
                                     auto_adjust=True)
usdcad = float(fx_hist["Close"].iloc[-1])
print("USD/CAD close 31 Dec 2024:", round(usdcad, 4))


def v(df, row, y):
    if df is None or row not in df.index or y not in df.columns:
        return np.nan
    return df.loc[row, y]


rows = []
for tick, name in TICKERS.items():
    sym = tick + ".TO"
    t = yf.Ticker(sym)
    bs, inc, cf = t.balance_sheet, t.financials, t.cashflow
    try:
        fin_ccy = t.info.get("financialCurrency", "CAD")
    except Exception:
        fin_ccy = "USD" if tick in USD_REPORTERS else "CAD"
    years = sorted(set(bs.columns) | set(inc.columns), reverse=True)
    for y in years:
        ystr = str(y)[:10]
        rev = v(inc, "Total Revenue", y)
        ebit = v(inc, "EBIT", y)
        if pd.isna(ebit):
            ebit = v(inc, "Operating Income", y)
        ebitda = v(inc, "EBITDA", y)
        if pd.isna(ebitda) and pd.notna(ebit):
            dep = v(cf, "Depreciation And Amortization", y)
            if pd.isna(dep):
                dep = v(inc, "Depreciation", y)
            if pd.notna(dep):
                ebitda = ebit + abs(dep)
        intexp = v(inc, "Interest Expense", y)
        if pd.isna(intexp):
            nii = v(inc, "Net Interest Income", y)
            intexp = -nii if pd.notna(nii) else np.nan
        if pd.notna(intexp) and intexp < 0:
            intexp = abs(intexp)
        debt = v(bs, "Total Debt", y)
        cash = v(bs, "Cash Cash Equivalents And Short Term Investments", y)
        ca = v(bs, "Current Assets", y)
        cl = v(bs, "Current Liabilities", y)
        ta = v(bs, "Total Assets", y)
        eq = v(bs, "Stockholders Equity", y)
        wc = v(bs, "Working Capital", y)
        if pd.isna(wc) and pd.notna(ca) and pd.notna(cl):
            wc = ca - cl
        re_ = v(bs, "Retained Earnings", y)
        tl = ta - eq if pd.notna(ta) and pd.notna(eq) else np.nan
        ocf = v(cf, "Operating Cash Flow", y)
        fcf = v(cf, "Free Cash Flow", y)
        ni = v(inc, "Net Income", y)
        if pd.isna(ni):
            ni = v(inc, "Net Income Common Stockholders", y)
        rows.append(dict(ticker=tick, company=name, fiscal_year_end=ystr,
                         reporting_currency=fin_ccy, revenue=rev, ebit=ebit,
                         ebitda=ebitda, interest_expense=intexp,
                         net_income=ni, total_debt=debt,
                         cash=cash, current_assets=ca, current_liabilities=cl,
                         total_assets=ta, equity=eq, working_capital=wc,
                         retained_earnings=re_, total_liabilities=tl,
                         operating_cash_flow=ocf, free_cash_flow=fcf))
df = pd.DataFrame(rows)
for c in df.columns[4:]:
    df[c] = df[c] / 1e6  # millions in reporting currency
# Manual fill: yfinance's balance sheet has no cash row at all for Tourmaline.
# Cash and equivalents from Zacks' balance sheet, which reproduces the
# company's filings (CAD millions): 2021: 9, 2022: 836, 2023: 353, 2024: 319,
# 2025: 130. Only the 2024 figure is used by the models.
tou_cash = {"2021-12-31": 9, "2022-12-31": 836, "2023-12-31": 353,
            "2024-12-31": 319, "2025-12-31": 130}
for ystr, val in tou_cash.items():
    df.loc[(df.ticker == "TOU") & (df.fiscal_year_end == ystr), "cash"] = val
usd = df["reporting_currency"] == "USD"
df.loc[usd, df.columns[4:]] = df.loc[usd, df.columns[4:]] * usdcad
df["reporting_currency"] = df["reporting_currency"].replace(
    {"USD": "USD converted to CAD", "CAD": "CAD"})
df.to_csv(base / "data" / "financials.csv", index=False)

m = df.copy()
m["debt_ebitda"] = m.total_debt / m.ebitda
m["net_debt_ebitda"] = (m.total_debt - m.cash) / m.ebitda
m["interest_coverage"] = m.ebit / m.interest_expense
m["current_ratio"] = m.current_assets / m.current_liabilities
m["cash_to_debt"] = m.cash / m.total_debt
m["debt_to_equity"] = m.total_debt / m.equity
m["fcf_to_debt"] = m.free_cash_flow / m.total_debt
m["net_debt"] = m.total_debt - m.cash
m.to_csv(base / "data" / "metrics.csv", index=False)

latest = []
for tick, g in m.sort_values("fiscal_year_end").groupby("ticker"):
    r = g.iloc[-1]
    info = yf.Ticker(tick + ".TO").info
    mcap = info.get("marketCap", np.nan) / 1e6 if info.get("marketCap") else np.nan
    z = np.nan
    if pd.notna(r.total_assets) and r.total_assets:
        z = (1.2 * (r.working_capital / r.total_assets)
             + 1.4 * (r.retained_earnings / r.total_assets)
             + 3.3 * (r.ebit / r.total_assets)
             + 0.6 * (mcap / r.total_liabilities if pd.notna(r.total_liabilities) and r.total_liabilities else np.nan)
             + 1.0 * (r.revenue / r.total_assets))
    latest.append(dict(ticker=tick, company=r.company, fiscal_year_end=r.fiscal_year_end,
                       market_cap_cad_m=mcap, altman_z=z,
                       **{k: r[k] for k in ["revenue", "ebit", "ebitda", "interest_expense",
                                            "total_debt", "net_debt", "cash", "debt_ebitda",
                                            "net_debt_ebitda", "interest_coverage", "current_ratio",
                                            "cash_to_debt", "debt_to_equity", "fcf_to_debt"]}))
lat = pd.DataFrame(latest)
lat.to_csv(base / "data" / "latest.csv", index=False)
print(lat[["ticker", "fiscal_year_end", "total_debt", "debt_ebitda",
           "interest_coverage", "current_ratio", "altman_z"]].to_string())
print("years per ticker:\n", df.groupby("ticker").size())
print("missing fields in 2024 rows:")
y24 = df[df.fiscal_year_end.str.startswith("2024")]
print(y24.isna().sum()[y24.isna().sum() > 0].to_string())
