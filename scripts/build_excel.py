"""Combined workbook: scorecard, credit models, 2024 financials, transition
summary, method. Decision-level tables only; full data stays in the CSVs."""
import pathlib

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

base = pathlib.Path(__file__).resolve().parents[1]
wb = Workbook()
title_font = Font(bold=True, size=14)
hdr_font = Font(bold=True, color="FFFFFF")
hdr_fill = __import__("openpyxl.styles", fromlist=["PatternFill"]).PatternFill("solid", fgColor="222222")


def sheet(name, title, rows, widths):
    ws = wb.create_sheet(name) if name != "Contents" else wb.active
    ws.title = name
    ws["A1"] = title
    ws["A1"].font = title_font
    for j, h in enumerate(rows[0], 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = hdr_font
        c.fill = hdr_fill
    for i, r in enumerate(rows[1:], 4):
        for j, v in enumerate(r, 1):
            ws.cell(row=i, column=j, value=v)
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    return ws


# Contents
ws = wb.active
ws.title = "Contents"
ws["A1"] = "Who Can Pay for the Transition: Combined Model"
ws["A1"].font = title_font
contents = [
    ["Sheet", "What it holds"],
    ["Scorecard", "Project 1 sustainability ranking, 12 companies, 4 measures, total out of 20"],
    ["Credit models", "Part B model results for 2024: Altman Z-prime, Springate, Zmijewski, Merton, synthetic rating"],
    ["Financials 2024", "2024 annual financials behind the models, CAD millions"],
    ["Transition", "Part A summary: electricity, primary energy production, capital spending, 2015 to 2024"],
    ["Method", "How each number was produced, and the limits"],
]
for j, h in enumerate(contents[0], 1):
    c = ws.cell(row=3, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, r in enumerate(contents[1:], 4):
    for j, v in enumerate(r, 1):
        ws.cell(row=i, column=j, value=v)
ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 100

sc = pd.read_csv(base / "data" / "scorecard.csv")
rows = [["Company", "Subsector", "Safety", "Climate targets", "Engagement", "Disclosure", "Total / 20"]]
for _, r in sc.sort_values("total", ascending=False).iterrows():
    rows.append([r.company, r.subsector, int(r.safety), int(r.climate), int(r.engagement), int(r.disclosure), int(r.total)])
sheet("Scorecard", "Sustainability scorecard, 2024 reports", rows, [32, 12, 10, 16, 12, 12, 12])

mod = pd.read_csv(base / "credit" / "data" / "models.csv")
met = pd.read_csv(base / "credit" / "data" / "metrics.csv")
m24 = met[met.fiscal_year_end.str.startswith("2024")].set_index("ticker")
rows = [["Company", "Debt / EBITDA", "Net debt / EBITDA", "Interest coverage",
         "Altman Z-prime", "Springate", "Zmijewski prob %", "Merton distance to default",
         "Merton EDF %", "Synthetic rating"]]
for _, r in mod.iterrows():
    t = r.ticker
    nd = (m24.loc[t, "net_debt"] / m24.loc[t, "ebitda"]) if pd.notna(m24.loc[t, "ebitda"]) else None
    rows.append([r.company, round(float(r.debt_ebitda), 2), round(float(nd), 2) if nd is not None else None,
                 round(float(r.interest_coverage), 2), round(float(r.altman_zprime), 2),
                 round(float(r.springate), 2), round(float(r.zmijewski_prob_pct), 1),
                 round(float(r.merton_dd), 2), round(float(r.merton_edf_pct), 6), r.synthetic_rating])
sheet("Credit models", "Credit models, 2024 annuals", rows, [32, 16, 18, 18, 16, 12, 18, 26, 14, 18])

fin = pd.read_csv(base / "credit" / "data" / "financials.csv")
f24 = fin[fin.fiscal_year_end.str.startswith("2024")]
cols = ["ticker", "company", "revenue", "ebit", "ebitda", "interest_expense", "net_income",
        "total_debt", "cash", "total_assets", "equity", "working_capital",
        "retained_earnings", "total_liabilities", "operating_cash_flow", "free_cash_flow"]
rows = [["Ticker", "Company", "Revenue", "EBIT", "EBITDA", "Interest expense", "Net income",
         "Total debt", "Cash", "Total assets", "Equity", "Working capital",
         "Retained earnings", "Total liabilities", "Operating cash flow", "Free cash flow"]]
for _, r in f24.iterrows():
    rows.append([r[c] if c in ("ticker", "company") else (round(float(r[c]), 1) if pd.notna(r[c]) else None) for c in cols])
sheet("Financials 2024", "2024 annual financials, CAD millions", rows,
      [10, 30] + [16] * 14)

el = pd.read_csv(base / "analysis_electricity.csv")
en = pd.read_csv(base / "analysis_energy_production.csv")
cx = pd.read_csv(base / "analysis_capex.csv")
ws = wb.create_sheet("Transition")
ws["A1"] = "Transition summary, 2015 to 2024 (StatCan)"
ws["A1"].font = title_font
r = 3
ws.cell(row=r, column=1, value="Electricity generation, terawatt hours").font = Font(bold=True, size=11)
r += 1
rows = [["Year", "Total", "Hydro", "Nuclear", "Wind", "Solar", "Combustible fuels", "Wind+solar share %"]]
for _, x in el[el.year.isin([2016, 2020, 2024])].iterrows():
    rows.append([int(x.year), round(x.Total, 2), round(x.Hydro, 2), round(x.Nuclear, 2),
                 round(x.Wind, 2), round(x.Solar, 2), round(x["Combustible fuels"], 2),
                 round(x["Wind+solar share %"], 1)])
for j, h in enumerate(rows[0], 1):
    c = ws.cell(row=r, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, row in enumerate(rows[1:], r + 1):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
r = r + len(rows) + 2
ws.cell(row=r, column=1, value="Primary energy production, exajoules").font = Font(bold=True, size=11)
r += 1
rows = [["Year", "Crude oil", "Natural gas", "Coal", "Primary electricity", "Total primary energy",
         "Fossil share %"]]
for _, x in en[en.year.isin([2015, 2020, 2024])].iterrows():
    rows.append([int(x.year), round(x["Crude oil"], 2), round(x["Natural gas"], 2),
                 round(x["Total coal"], 2), round(x["Primary electricity, hydro, nuclear, and other renewables"], 2),
                 round(x["Primary energy"], 2), round(x["Fossil share of primary %"], 1)])
for j, h in enumerate(rows[0], 1):
    c = ws.cell(row=r, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, row in enumerate(rows[1:], r + 1):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
r = r + len(rows) + 2
ws.cell(row=r, column=1, value="Capital spending, $ millions").font = Font(bold=True, size=11)
r += 1
rows = [["Year", "Oil and gas extraction", "Utilities"]]
for _, x in cx[cx.year.isin([2015, 2020, 2024])].iterrows():
    rows.append([int(x.year), round(x["Oil and gas extraction [211]"], 1), round(x["Utilities [22]"], 1)])
for j, h in enumerate(rows[0], 1):
    c = ws.cell(row=r, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, row in enumerate(rows[1:], r + 1):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
for j, w in enumerate([10, 22, 16, 12, 12, 20, 20, 20], 1):
    ws.column_dimensions[get_column_letter(j)].width = w

ws = wb.create_sheet("Method")
ws["A1"] = "Method and limits"
ws["A1"].font = title_font
lines = [
    "Scorecard: 4 measures scored 0 to 5 from each company's 2024 sustainability report, except Imperial Oil (2022, latest available). Emissions and freshwater intensity are shown in the scorecard file, not scored.",
    "Bill C-59: CNQ, Suncor and Cenovus stripped environmental content from their 2024 reports, so their climate and disclosure scores are disclosure gaps, not performance verdicts.",
    "Credit models: 2024 annual financials from Yahoo Finance. USD reporters (Barrick, Agnico, Nutrien, Methanex, West Fraser) converted at USD/CAD 1.435, the close on 31 Dec 2024.",
    "Tourmaline cash of $319m at 31 Dec 2024 is a manual fill from Zacks' balance sheet; Yahoo Finance has no cash row for Tourmaline.",
    "Teck net income of $406m uses the Net Income Common Stockholders row; the Net Income row is missing for Teck in 2024.",
    "Merton is point-in-time at 31 Dec 2024: 1-year daily volatility over 2024, market value at the 31 Dec 2024 close times current shares outstanding, risk free rate 3.0%.",
    "Transition data: Statistics Canada tables 25-10-0015-01, 25-10-0029-01 and 34-10-0035-01, downloaded 16 Nov 2026. 2025 and 2026 capital spending figures are intentions, not actuals.",
    "Past performance does not predict future performance. This project is an investigation, not a credit rating and not personal investment advice.",
]
for i, line in enumerate(lines, 3):
    ws.cell(row=i, column=1, value=line)
ws.column_dimensions["A"].width = 160

wb.save(base / "Who_Can_Pay_for_the_Transition_Model.xlsx")
print("excel done")
