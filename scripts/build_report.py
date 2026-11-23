"""Combined report, draft 2: revised to her spec.
Executive summary in three parts: what the project is, what it tried to
achieve, summary of achievements. Heat map tables for the scorecard,
the credit models and the joint table. A methodology section on how
Python was used, with two short code listings. Formal register, numbered
sections, figures labelled as figures and tables as tables. Black text
only. Name once at the top. No first person. No em dashes."""
import math
import pathlib

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, Paragraph, Preformatted,
                                SimpleDocTemplate, Table, TableStyle)

base = pathlib.Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.black, spaceBefore=12, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.black, spaceBefore=10, spaceAfter=6)
small = ParagraphStyle("small", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black, spaceAfter=4)
caption = ParagraphStyle("caption", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=colors.black, spaceAfter=10)
cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black)
cellhead = ParagraphStyle("cellhead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.black)
code_style = ParagraphStyle("code", parent=styles["Normal"], fontName="Courier", fontSize=8.5, leading=11, textColor=colors.black, leftIndent=6)
RED = (0.969, 0.412, 0.420)
YELLOW = (1.0, 0.922, 0.518)
GREEN = (0.388, 0.745, 0.482)


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def heat(t):
    """t from 0 (weak) to 1 (strong): red through yellow to green."""
    t = max(0.0, min(1.0, t))
    rgb = lerp(RED, YELLOW, t * 2) if t < 0.5 else lerp(YELLOW, GREEN, (t - 0.5) * 2)
    return colors.HexColor("#%02x%02x%02x" % tuple(int(c * 255) for c in rgb))


def heat_linear(v, vmin, vmax, invert=False):
    t = (v - vmin) / (vmax - vmin)
    return heat(1 - t if invert else t)


def heat_cutoff(v, cut, span):
    """Below the cut-off: red to yellow. Above it: yellow to green."""
    if v <= cut:
        return heat(0.5 * max(0.0, v) / cut)
    return heat(0.5 + 0.5 * min(1.0, (v - cut) / span))


def heat_log(v, vmin, vmax):
    t = (math.log10(v) - math.log10(vmin)) / (math.log10(vmax) - math.log10(vmin))
    return heat(t)


VERDICT_COLORS = {
    "Can pay comfortably": "#63BE7B",
    "Can pay": "#A9D18E",
    "Can pay, moderately": "#FFEB84",
    "Constrained": "#F8696B",
    "Can pay, conditionally": "#FFC000",
    "Can pay, earnings not debt is the constraint": "#FFEB84",
    "Can pay, score is a disclosure gap": "#A9D18E",
}


def P(t, s=body):
    return Paragraph(t, s)


def tbl(data, widths, backgrounds=None):
    wrapped = [[Paragraph(str(c), cellhead if r == 0 else cell) for c in row] for r, row in enumerate(data)]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if backgrounds:
        for (col, row), color in backgrounds.items():
            style.append(("BACKGROUND", (col, row), (col, row), color))
    t.setStyle(TableStyle(style))
    return t


def img(path, w=170 * mm):
    return Image(str(path), width=w, height=w * 0.55)


story = []
story.append(P("Who Can Pay for the Transition: Canada's Energy Transition and the Balance Sheets Behind It", h1))
story.append(P("Munzeleen Sarwar", body))
story.append(P("November 2026. Sustainability scores from 2024 company reports. Financials from 2024 annual statements. Transition data from Statistics Canada, 2015 to 2024. This report is an investigation, not a credit rating and not personal investment advice.", small))
story.append(P("Executive summary", h1))
story.append(P("<b>What this project is.</b> A combined investigation of the 12 largest TSX-listed resource companies, five in energy, four in mining and three in materials, built for the Mackenzie Investments Resources team. It has three parts. Part 1 is a sustainability scorecard that ranks the 12 companies on safety, climate targets, community and Indigenous engagement, and disclosure. Part A is a research note on where Canada's energy sector is going, built from Statistics Canada data. Part B runs four credit risk models, Altman Z-prime, Springate, Zmijewski and Merton, on each company's 2024 annual statements. The conclusion joins the three parts into one answer: which companies can pay for the transition."))
story.append(P("<b>What it tried to achieve.</b> Four things. First, to set a measurement standard for sustainable development in the natural resources investment universe, which is the first responsibility in the Resources posting. Second, to measure the transition itself, in power generation, in what Canada produces, and in where capital spending goes. Third, to test each company's balance sheet with the same credit framework used for US AI companies, so the results can be compared across projects. Fourth, to join the sustainability score and the credit strength into one verdict per company, because neither measure alone answers the question."))
story.append(P("<b>Summary of achievements.</b> The scorecard was built and ranked: Barrick and Teck tie at the top with 17 out of 20, and Canadian Natural Resources is last at 9, with the gap flagged as a disclosure gap from Bill C-59 rather than a performance verdict. A returns test was run on the scores and found no link between scores and returns or volatility, which stops any false claim that a high score means a better stock. The transition note was written from three full Statistics Canada tables and verified against published 2023 figures: wind rose five times and solar twenty times between 2015 and 2024, yet the fossil share of primary energy production rose from 87.0% to 88.5%. The credit models were run on all 12 companies and produced a clear ranking, with Methanex and Nutrien as the stretched names and Agnico, Imperial, Tourmaline, Suncor, Barrick and CNQ as the strong balance sheets. The joint conclusion sorts the 12 into four groups: five can pay comfortably, three can pay, two are constrained despite good scores, and two are special cases. The work is fully reproducible: every number in this report traces to a saved data file and a named Python script, listed in Appendix A, with an Excel model and a notebook alongside the report."))
story.append(P("1. The sustainability scorecard", h1))
story.append(P("What this section is trying to achieve", h2))
story.append(P("The scorecard sets a measurement standard for sustainable development in the natural resources investment universe, which is the first responsibility in the Mackenzie Resources posting. It takes 12 TSX-listed resource companies and scores each on four measures that can be read from public reports: safety, climate target quality, community and Indigenous engagement, and disclosure completeness. Each measure is scored 0 to 5, for a total out of 20. Emissions intensity and freshwater intensity are shown separately and not scored, because almost every company reports them in its own unit and freshwater intensity was disclosed by almost nobody."))
story.append(P("How it works", h2))
story.append(P("Safety uses injury frequency per 200,000 hours worked, with bands at 0.20 or less for 5 points, 0.21 to 0.50 for 4, 0.51 to 1.00 for 3, 1.01 to 1.50 for 2, and above 1.50 for 1. Figures reported per 1,000,000 hours were divided by 5. Climate target quality rewards a dated net zero commitment with interim targets and TCFD alignment. Engagement rewards named Indigenous agreements, dollar amounts spent with Indigenous businesses, and grievance processes. Disclosure rewards the number of reporting frameworks used and third party assurance. The scoring was done by reading each company's 2024 sustainability report. Nothing was estimated. Where a figure was not disclosed, the score is 0 on that measure and the gap is flagged."))
story.append(P("Results", h2))
sc_rows = [
    ["Rank", "Company", "Safety", "Climate", "Engagement", "Disclosure", "Total / 20"],
    ["1", "Barrick Gold", 5, 5, 3, 4, 17],
    ["1", "Teck Resources", 3, 5, 4, 5, 17],
    ["3", "Imperial Oil", 4, 5, 4, 3, 16],
    ["4", "Agnico Eagle Mines", 2, 5, 4, 4, 15],
    ["4", "Nutrien", 3, 3, 4, 5, 15],
    ["4", "Methanex", 5, 3, 4, 3, 15],
    ["7", "Suncor Energy", 4, 2, 4, 4, 14],
    ["7", "Tourmaline Oil", 4, 3, 2, 5, 14],
    ["9", "West Fraser Timber", 1, 3, 4, 5, 13],
    ["10", "Cenovus Energy", 4, 0, 4, 4, 12],
    ["10", "Cameco", 1, 3, 3, 5, 12],
    ["12", "Canadian Natural Resources", 5, 0, 4, 0, 9],
]
sc_bg = {}
for i, row in enumerate(sc_rows[1:], 1):
    for j in range(2, 6):
        sc_bg[(j, i)] = heat(row[j] / 5)
    sc_bg[(6, i)] = heat(row[6] / 20)
story.append(tbl(sc_rows, [14 * mm, 52 * mm, 18 * mm, 18 * mm, 24 * mm, 22 * mm, 22 * mm], sc_bg))
story.append(P("Table 1: Sustainability ranking, 2024 reports, as a heat map. Green is strong, red is weak. Imperial Oil uses 2022 figures, its latest available report.", caption))
story.append(P("What the results mean", h2))
story.append(P("The top of the ranking is mining. Barrick leads on safety at 0.18 injuries per 200,000 hours, the lowest in mining, with a net zero target for 2050 and TCFD alignment. Teck ties it with the strongest engagement in the set: 85 active agreements with Indigenous Peoples, $292 million of Indigenous procurement, and the most complete disclosure at 5 points. Imperial is the best energy name at 16, with a net zero target and $4.6 billion spent with Indigenous businesses since 2008, but all its figures are from 2022 because it published no 2024 report."))
story.append(P("The bottom of the ranking is a disclosure story, not a performance story. Canadian Natural Resources has the best safety figure in energy at 0.12 injuries per 200,000 hours, down 37% since 2020, and $855 million in contracts with 212 Indigenous businesses in 2024, yet it scores 9 because Bill C-59 led it to strip environmental content from its 2024 report. It scored 0 on climate targets and 0 on disclosure. Cenovus is the same pattern at 12: safety of 0.33, $851 million spent with Indigenous businesses, the highest annual spend in its history, and 0 on climate targets. Suncor scored 2 on climate targets for TCFD only, with the same explanation. The 0s in this table are disclosure gaps, and the report flags them wherever they apply."))
story.append(P("Two other findings matter. First, freshwater intensity is the weakest disclosure in the whole set: only 3 of 12 companies disclose a company-wide figure. Second, Tourmaline is the only energy company that published full 2024 environmental figures, with the lowest emissions intensity in energy at 0.0177 tonnes of CO2e per barrel of oil equivalent, against about 0.045 for Suncor, 0.050 for CNQ and 0.051 for Cenovus."))
story.append(P("2. The energy transition in Canada", h1))
story.append(P("What this section is trying to achieve", h2))
story.append(P("This section measures where Canada's energy sector is going, from Statistics Canada data, in the style of an Economic Intelligence Bangladesh research note. It answers three questions: how power generation is changing, how what Canada produces is changing, and where the money is going. The window is 2015 to 2024, the latest complete year in all three tables."))
story.append(P("How it works", h2))
story.append(P("Three full tables were downloaded from Statistics Canada: table 25-10-0015-01 for electricity supply and disposition, table 25-10-0029-01 for supply and demand of primary and secondary energy, and table 34-10-0035-01 for capital and repair expenditures by industry. Two fixes were needed. First, the electricity table changed structure in 2015, so the fuel split chart runs from 2016 and 2015 is used only for levels and growth rates of hydro, nuclear, wind and solar. Second, the capital spending table has no NAICS code for electric power alone, so Utilities is used as the power-side series, labelled as mostly electric power, with the power-specific figure quoted separately from Natural Resources Canada's Energy Fact Book."))
story.append(P("Power: renewables grow, hydro falls, fossil holds its share", h2))
story.append(P("Wind and solar are the fastest growing sources in Canadian electricity, but they remain small. Wind rose from 8.85 terawatt hours in 2015 to 45.84 in 2024, and solar from 0.26 to 5.23. Together they were 8.4% of generation in 2024, up from 1.5% in 2015. Hydro still dominates at 56.1%, but it fell from 375.62 terawatt hours in 2015 to 341.82 in 2024, with the sharpest drops in 2023 and 2024, when dry conditions cut river flows. Nuclear fell 17% over the same period as reactors went down for refurbishment. Total generation was nearly flat, 592.76 terawatt hours in 2015 against 609.49 in 2024, so the growth in wind and solar mostly filled the gap left by hydro and nuclear rather than replacing fossil fuels. Combustible fuels supplied 22.1% of power in 2024, against 21.2% in 2016, and non-renewable combustible fuels alone were 20.5%. Renewables were 66.0% of generation in 2024, but that figure is mostly hydro built decades ago, not new capacity."))
story.append(img(base / "charts" / "electricity_by_source.png"))
story.append(P("Figure 1: Electricity generation in Canada by source, 2016 to 2024, terawatt hours. Source: Statistics Canada table 25-10-0015-01.", caption))
story.append(tbl([
["Terawatt hours", "2015", "2020", "2024", "Change 2015-2024"],
["Total generation", "592.76", "635.57", "609.49", "+2.8%"],
["Hydro", "375.62", "382.62", "341.82", "-9.0%"],
["Nuclear", "98.37", "92.65", "81.74", "-16.9%"],
["Wind", "8.85", "36.26", "45.84", "+417.8%"],
["Solar", "0.26", "2.57", "5.23", "+1,922.3%"],
["Combustible fuels", "n/a", "121.35", "134.57", "n/a"],
["Renewables", "n/a", "430.61", "402.25", "n/a"],
], [52 * mm, 28 * mm, 28 * mm, 28 * mm, 34 * mm]))
story.append(P("Table 2: Electricity generation. The combustible fuels split is published from 2016, so no 2015 figure is shown. Renewables in 2020 were 67.8% of generation and 66.0% in 2024.", caption))
story.append(P("Production: oil and gas grew by a third", h2))
story.append(P("What Canada produces moved the other way. Crude oil production rose from 8.84 exajoules in 2015 to 11.76 in 2024, up 33.0%, and natural gas from 6.47 to 8.91, up 37.7%. Coal fell 15.2% and primary electricity, hydro, nuclear and other renewables combined, fell 4.8% on the same hydro drought. Total primary energy production rose 28.8% to 24.66 exajoules, and oil and gas supplied 20.67 of it. The fossil share of production rose from 87.0% to 88.5%, while primary electricity fell from 9.5% to 7.0% of production. Canada produced more energy in 2024 than in 2015, and a larger share of it came from oil and gas."))
story.append(img(base / "charts" / "primary_energy_production.png"))
story.append(P("Figure 2: Primary energy production in Canada by fuel, 2015 to 2024, exajoules. Source: Statistics Canada table 25-10-0029-01.", caption))
story.append(tbl([
["Exajoules", "2015", "2020", "2024", "Change 2015-2024"],
["Crude oil", "8.84", "10.22", "11.76", "+33.0%"],
["Natural gas", "6.47", "7.60", "8.91", "+37.7%"],
["Coal", "1.35", "1.15", "1.15", "-15.2%"],
["Primary electricity", "1.81", "1.85", "1.72", "-4.8%"],
["Total primary energy", "19.15", "21.75", "24.66", "+28.8%"],
["Fossil share of primary energy", "87.0%", "87.2%", "88.5%", "+1.5 points"],
], [52 * mm, 28 * mm, 28 * mm, 28 * mm, 34 * mm]))
story.append(P("Table 3: Primary energy production. The four fuels shown sum to 23.54 exajoules in 2024; the rest is natural gas liquids, steam and other fuels.", caption))
story.append(P("Money: the capital is moving, slowly", h2))
story.append(P("Capital spending shows the turn more clearly than production does. Oil and gas extraction spent $51.1 billion in 2015, crashed to $21.8 billion in 2020, and recovered to $43.7 billion in 2024, still 43% below its 2014 peak of $76.1 billion. Utilities, mostly electric power, spent $31.5 billion in 2015 and $42.4 billion in 2024, up 35%, rising almost every year. The two lines met in 2024 and, on intentions, utilities pass oil and gas in 2025, $47.0 billion against $42.0 billion. The power-specific split, from Natural Resources Canada's Energy Fact Book, puts electric power generation and distribution at $32 billion in 2024 against $43 billion for oil and gas extraction, out of $89 billion of energy capital spending in total. Money is moving toward power. Production has not followed yet."))
story.append(img(base / "charts" / "capex_oil_gas_vs_utilities.png"))
story.append(P("Figure 3: Capital expenditures, oil and gas extraction against utilities, 2015 to 2024, $ millions. Source: Statistics Canada table 34-10-0035-01.", caption))
story.append(tbl([
["$ millions", "2015", "2020", "2024", "Change 2015-2024"],
["Oil and gas extraction", "51,065", "21,805", "43,652", "-14.5%"],
["Utilities", "31,524", "30,309", "42,429", "+34.6%"],
], [52 * mm, 28 * mm, 28 * mm, 28 * mm, 34 * mm]))
story.append(P("Table 4: Capital spending. 2025 figures are intentions: oil and gas $42,038 million, utilities $47,026 million.", caption))
story.append(P("What this section means for resource investors", h2))
story.append(P("The transition in Canada is uneven, and that unevenness is the investment question. Power is changing: wind and solar are growing fast, utilities are spending more than ever, and fossil fuels still supply a fifth of electricity. Production is not changing: oil and gas output is a third higher than a decade ago, and the fossil share of what Canada produces has risen. The companies that must fund the transition earn their cash from the fuels the transition is meant to replace. Whether they can pay for it depends on their balance sheets, not on the direction of the sector. The next section tests exactly that."))
story.append(P("3. Credit risk on the 12 companies", h1))
story.append(P("What this section is trying to achieve", h2))
story.append(P("This section extends the US AI credit risk framework to Canadian resource companies. It runs four models on each company's 2024 annual statements: Altman Z-prime, Springate, Zmijewski, and Merton distance to default, plus a synthetic rating from interest coverage and plain leverage and cash flow ratios. The model year is 2024, to match the scorecard year. The question is which balance sheets can carry transition investment, and which are already stretched."))
story.append(P("How it works", h2))
story.append(P("Annual financials come from Yahoo Finance, five years per company. Companies reporting in US dollars, Barrick, Agnico, Nutrien, Methanex and West Fraser, are converted to Canadian dollars at 1.435, the USD/CAD close on 31 December 2024. Altman Z-prime combines working capital, retained earnings, EBIT and equity, each divided by assets or liabilities, with weights 6.56, 3.26, 6.72 and 1.05. Above 2.6 is safe, 1.1 to 2.6 is grey, below 1.1 is distress. Springate combines working capital, EBIT and revenue with weights 1.03, 3.07, 0.66 and 0.4; above 0.862 is safe. Zmijewski combines return on assets, liabilities to assets and the current ratio into a probability of failure; the ranking matters more than the level. Merton treats equity as a call option on the firm's assets and measures distance to default in standard deviations, using one year of daily price volatility to 31 December 2024, market value at the 31 December 2024 close, and a risk free rate of 3.0%. The synthetic rating maps interest coverage to rating bands, with AAA at 8.5 times and above, BBB at 2.5 times and BB+ at 2.0 times."))
story.append(P("Results", h2))
cr_rows = [
    ["Company", "Debt / EBITDA", "Net debt / EBITDA", "Coverage", "Z-prime", "Springate", "Zmijewski %", "Merton DD", "Rating"],
    ["Agnico Eagle", 0.29, 0.08, 33.6, 3.54, 1.72, 5.3, 9.67, "AAA"],
    ["West Fraser", 0.37, -0.67, 2.5, 6.53, 0.46, 4.1, 8.93, "BB+"],
    ["Tourmaline", 0.40, 0.30, 21.4, 3.65, 1.09, 5.4, 9.67, "AAA"],
    ["Imperial Oil", 0.50, 0.38, 153.2, 4.33, 1.55, 9.5, 8.79, "AAA"],
    ["Barrick", 0.76, 0.17, 11.9, 2.13, 1.80, 14.9, 8.10, "AAA"],
    ["Suncor", 0.93, 0.71, 12.8, 2.74, 1.13, 14.6, 9.77, "AAA"],
    ["Cenovus", 1.11, 0.79, 7.3, 2.69, 1.14, 13.1, 8.37, "AA"],
    ["CNQ", 1.22, 1.21, 13.0, 2.49, 1.08, 16.8, 9.60, "AAA"],
    ["Cameco", 1.93, 1.02, 3.0, 3.66, 0.54, 8.5, 6.91, "A-"],
    ["Nutrien", 3.04, 2.84, 2.5, 2.10, 0.45, 20.0, 8.62, "BBB"],
    ["Methanex", 4.05, 2.93, 3.1, 2.89, 0.98, 36.3, 7.72, "A-"],
    ["Teck", 5.59, 1.33, 0.1, 3.64, 0.27, 13.8, 7.14, "CCC or lower"],
]
cr_bg = {}
for i, row in enumerate(cr_rows[1:], 1):
    cr_bg[(1, i)] = heat_linear(row[1], 0, 6, invert=True)
    cr_bg[(2, i)] = heat_linear(row[2], -1, 3, invert=True)
    cr_bg[(3, i)] = heat_log(row[3], 0.07, 35)
    cr_bg[(4, i)] = heat_cutoff(row[4], 2.6, 1.0)
    cr_bg[(5, i)] = heat_cutoff(row[5], 0.862, 0.6)
    cr_bg[(6, i)] = heat_linear(row[6], 0, 40, invert=True)
story.append(tbl(cr_rows, [28 * mm, 20 * mm, 22 * mm, 16 * mm, 14 * mm, 16 * mm, 18 * mm, 16 * mm, 20 * mm], cr_bg))
story.append(P("Table 5: Credit model results, 2024 annuals, as a heat map. Green is strong, red is weak. Teck coverage is 0.07x on reported EBIT; on adjusted EBIT it is 1.43x. Imperial coverage of 153.2x reflects an interest bill of only $41 million.", caption))
story.append(img(base / "credit" / "charts" / "debt_ebitda.png"))
story.append(P("Figure 4: Debt to EBITDA, 2024 annuals. The dashed line at 3 times is a common caution line.", caption))
story.append(img(base / "credit" / "charts" / "coverage_vs_leverage.png"))
story.append(P("Figure 5: Leverage against interest coverage, 2024 annuals, log scale for coverage. Teck sits alone at the bottom right. West Fraser sits at the bottom left: low leverage, low coverage.", caption))
story.append(img(base / "credit" / "charts" / "zmijewski_prob.png"))
story.append(P("Figure 6: Zmijewski probability of failure, 2024 annuals. Use the ranking, not the level: the model was calibrated on a different population and the absolute probabilities run high for capital-heavy firms.", caption))
story.append(P("What the models agree on", h2))
story.append(P("Methanex and Nutrien are the genuinely stretched names. Every model points the same way: highest leverage at 4.05 and 3.04 times EBITDA, highest net leverage at 2.93 and 2.84 times, thinnest cash flow cover with operating cash flow at 0.23 and 0.28 times their debt and free cash flow at 0.17 and 0.11 times, highest Zmijewski probabilities at 36.3% and 20.0%, and the lowest synthetic ratings at A- and BBB. Methanex leverage is persistent, not one bad year: 3.79 times in 2023 and 4.04 times in 2025. Agnico, Imperial, Tourmaline, Suncor, Barrick and CNQ are the strong balance sheets: leverage under 1.3 times, coverage above 11 times, operating cash flow above 0.7 times their debt. Agnico is the strongest on leverage at 0.29 times and on cash flow, with operating cash flow at 3.09 times its debt and free cash flow at 1.66 times."))
story.append(P("Where the models disagree, and why", h2))
story.append(P("Teck looks worst on gross leverage at 5.59 times and coverage at 0.07 times, but its net leverage is only 1.33 times because it held $7,587 million of cash at the end of 2024 from the steelmaking coal sale. Its 2024 EBIT of $57 million includes a $1,053 million write-off; on adjusted EBIT of $1,110 million, coverage is 1.43 times, Z-prime 3.79 and Springate 0.50, still below the 0.862 Springate cut-off. Even adjusted, Teck is weak on earnings cover: interest expense of $775 million is large next to post-coal earnings, and 2024 free cash flow was only $155 million. Merton gives a distance to default of 7.14, far from default, because the market value is large next to the default point. The honest reading is that Teck is not in distress, but it is the most leveraged name on earnings and the thinnest on interest cover."))
story.append(P("West Fraser is the opposite disagreement. Z-prime calls it the safest name in the set at 6.53, because it is net cash: $920 million of cash against $329 million of debt, net debt to EBITDA of -0.67 times. Springate calls it distressed at 0.46, because 2024 EBIT was only $92 million after the lumber downturn. A net-cash company is not in distress; its earnings collapsed for a year. Springate is an earnings model and it punishes a cyclical trough. The balance sheet is the truth here."))
story.append(P("Cameco fails Springate at 0.54 for a structural reason, not a credit reason: revenue to assets is only 0.32, because uranium mining is capital heavy, and EBIT to assets is only 0.039. Springate rewards asset turnover, so capital-heavy miners score low. Cameco leverage is 1.93 times and coverage is 3.0 times, which is middle of the set, not distress."))
story.append(P("Imperial coverage of 153.2 times is arithmetically right but should not be quoted on its own: interest expense was only $41 million in 2024, confirmed by interest paid of $42 million. The rating is AAA either way, but the number reflects a tiny interest bill, not infinite strength. CNQ sits in the Z-prime grey zone at 2.49 despite 13.0 times coverage and 1.22 times leverage, because working capital is negative at -$2,226 million and the equity to liabilities ratio is only 0.86. Negative working capital is normal for oil producers and Z-prime penalises it."))
story.append(P("4. Joint conclusion: who can pay for the transition", h1))
story.append(P("The combined table joins the scorecard total with the credit results for the same 12 companies in the same year."))
jt_rows = [
    ["Company", "Score / 20", "Debt / EBITDA", "Net debt / EBITDA", "Coverage", "OCF / debt", "Verdict"],
    ["Barrick", 17, 0.76, 0.17, 11.9, 0.85, "Can pay comfortably"],
    ["Teck", 17, 5.59, 1.33, 0.1, 0.28, "Can pay, conditionally"],
    ["Imperial", 16, 0.50, 0.38, 153.2, 1.44, "Can pay comfortably"],
    ["Agnico", 15, 0.29, 0.08, 33.6, 3.09, "Can pay comfortably"],
    ["Nutrien", 15, 3.04, 2.84, 2.5, 0.28, "Constrained"],
    ["Methanex", 15, 4.05, 2.93, 3.1, 0.23, "Constrained"],
    ["Suncor", 14, 0.93, 0.71, 12.8, 1.09, "Can pay comfortably"],
    ["Tourmaline", 14, 0.40, 0.30, 21.4, 2.09, "Can pay comfortably"],
    ["West Fraser", 13, 0.37, -0.67, 2.5, 2.89, "Can pay, earnings not debt is the constraint"],
    ["Cenovus", 12, 1.11, 0.79, 7.3, 0.87, "Can pay"],
    ["Cameco", 12, 1.93, 1.02, 3.0, 0.71, "Can pay, moderately"],
    ["CNQ", 9, 1.22, 1.21, 13.0, 0.71, "Can pay, score is a disclosure gap"],
]
jt_bg = {}
for i, row in enumerate(jt_rows[1:], 1):
    jt_bg[(1, i)] = heat(row[1] / 20)
    jt_bg[(2, i)] = heat_linear(row[2], 0, 6, invert=True)
    jt_bg[(3, i)] = heat_linear(row[3], -1, 3, invert=True)
    jt_bg[(4, i)] = heat_log(row[4], 0.07, 35)
    jt_bg[(5, i)] = heat_linear(row[5], 0, 3.2)
    jt_bg[(6, i)] = colors.HexColor(VERDICT_COLORS[row[6]])
story.append(tbl(jt_rows, [26 * mm, 16 * mm, 20 * mm, 24 * mm, 16 * mm, 18 * mm, 50 * mm], jt_bg))
story.append(P("Table 6: Score against credit strength, 2024, as a heat map. OCF to debt is operating cash flow divided by total debt.", caption))
story.append(P("Can pay comfortably: Barrick, Imperial, Agnico, Suncor, Tourmaline", h2))
story.append(P("These five pair a score of 14 or better with leverage under one times EBITDA and coverage above 11 times. Agnico is the strongest balance sheet in the set. Tourmaline is close behind. Imperial has the lowest leverage of the energy names. Barrick is joint top of the scorecard and carries only 0.17 times net leverage. Suncor is the quietest name in the group: 14 on the scorecard, 0.93 times leverage, 12.8 times coverage, operating cash flow above its debt."))
story.append(P("Can pay: CNQ, Cenovus, Cameco", h2))
story.append(P("CNQ and Cenovus sit at the bottom of the scorecard, 9 and 12, and both can pay. Their scores are disclosure gaps. Bill C-59 stripped the environmental content from their 2024 reports, so CNQ scored 0 on climate targets and 0 on disclosure, and Cenovus scored 0 on climate targets. Their balance sheets are strong: CNQ at 1.22 times leverage and 13.0 times coverage, Cenovus at 1.11 times and 7.3 times. A reader who only saw the scorecard would call CNQ the worst company in the set. A reader who only saw the credit models would call it one of the strongest. Both readings are in the numbers; the disclosure note is what reconciles them. Cameco is the moderate case. It scores 12, held back by the worst safety figure in the set at 2.26 injuries per 200,000 hours, 25% above its own target. Its credit is middle of the set: 1.93 times leverage, 3.0 times coverage, operating cash flow at 0.71 times its debt. It can pay, but its cash flow depends on the uranium price, and its equity volatility in 2024 was the highest in the set at 42.9% a year."))
story.append(P("Constrained: Nutrien and Methanex", h2))
story.append(P("Both scored 15 out of 20, joint fourth on the scorecard, and both are the most leveraged names in the set. Their transition spending, low-carbon methanol for Methanex and low-carbon ammonia and potash efficiency for Nutrien, has to be funded from operations that are already levered, and it competes directly with deleveraging. A high sustainability score does not create room to spend."))
story.append(P("Special cases: Teck and West Fraser", h2))
story.append(P("Teck is joint top of the scorecard at 17 and the most complicated credit in the set. Its ability to fund transition investment depends on copper earnings and the Quebrada Blanca ramp, not on the cash pile alone, and the cash will not last if it is spent without earnings behind it. West Fraser is net cash, so its low Springate score is a cyclical earnings trough, not distress. The constraint on West Fraser is earnings cyclicality, not debt."))
story.append(P("What each part alone would miss", h2))
story.append(P("The scorecard alone would rank CNQ last and Nutrien and Methanex joint fourth. The credit models reverse both calls. The credit models alone would call Teck the weakest name and West Fraser distressed. The scorecard and the cash positions reverse both calls. Part A alone would say the transition is stalled in production, because the fossil share of what Canada produces rose to 88.5%. The company-level answer is that the cash to fund the transition exists in the producers' balance sheets. The five energy names that can pay, CNQ, Suncor, Imperial, Cenovus and Tourmaline, earned their cash from the fuels the transition is meant to replace, and their combined operating cash flow in 2024 was about $47 billion. Whether they spend it on transition projects is a choice, not a constraint."))
story.append(P("5. Methodology: how Python was used", h1))
story.append(P("This project was built in Python, in VS Code, with each step saved as a script so every number in the report can be recomputed from the saved files. The work ran in seven steps."))
story.append(P("Step 1: the scorecard universe and framework. The 12 companies were chosen from TSX energy, mining and materials names, five, four and three. The four measures and the safety bands were set in a notes file. The scoring itself was done by reading each company's 2024 sustainability report, because the figures sit in PDF text and tables that no data feed carries cleanly. The ranking was saved as data in data/scorecard.csv, so the Excel model and the notebook read the same numbers as the report."))
story.append(P("Step 2: the transition data. The three Statistics Canada tables were downloaded as full tables. The Web Data Service endpoint returned 404, so the download used the direct zip URLs instead, one per table, and unzipped the CSV inside. The tables are 14.4, 34.0 and 15.9 megabytes, saved in data/ with their metadata files."))
story.append(P("Step 3: the transition analysis. analyse.py reads the three tables with pandas, sums monthly electricity data to annual totals, converts terajoules to exajoules, and computes the growth rates and shares. It also builds the three charts with matplotlib and writes three analysis CSV files, one per table, so the headline figures can be checked without rerunning the full tables. Two fixes in this step matter: the electricity fuel split runs from 2016 because the table structure changed in 2015, and Utilities stands in for electric power because the capital spending table has no finer split."))
story.append(P("Step 4: the credit data. credit/scripts/download_and_analyse.py pulls five years of annual financials per company through yfinance, converts US dollar reporters to Canadian dollars at 1.435, computes the plain ratios, and writes credit/data/financials.csv, credit/data/metrics.csv and credit/data/latest.csv. Two data fixes are in that script: Tourmaline cash of $319 million at 31 December 2024 is a manual fill from Zacks' balance sheet, because Yahoo Finance has no cash row for Tourmaline, and Teck net income of $406 million uses the Net Income Common Stockholders row, because the Net Income row is missing for Teck in 2024."))
story.append(P("Step 5: the credit models. credit/scripts/analyse_models.py reads the 2024 rows and runs the four models. Listing 1 shows the Altman Z-prime calculation, the first line of the model code. Each term is a ratio from the 2024 statements: working capital, retained earnings and EBIT divided by total assets, and equity divided by total liabilities. The weights are Altman's. The same file computes Springate, Zmijewski and Merton, and an adjusted view for Teck that adds back the $1,053 million write-off."))
story.append(Preformatted("zprime = (6.56 * (wc / ta) + 3.26 * (re_ / ta)\n"
                          "          + 6.72 * (ebit / ta) + 1.05 * (eq / tl))",
                          code_style))
story.append(P("Listing 1: Altman Z-prime, from credit/scripts/analyse_models.py. wc is working capital, re_ is retained earnings, ta is total assets, eq is equity and tl is total liabilities, all from the 2024 statements.", caption))
story.append(P("Step 6: the charts and the workbook. credit/scripts/make_charts.py builds the three Part B charts with matplotlib, and scripts/build_excel.py builds the combined workbook with openpyxl: Contents, Scorecard, Credit models, Financials 2024, Transition and Method. The workbook holds decision-level tables only; the full data stays in the CSV files."))
story.append(P("Step 7: the notebook and the report. scripts/build_notebook.py writes the recomputation notebook as plain JSON, with cells that reload the saved CSV files and reproduce the headline numbers and two charts. scripts/build_report.py builds this report with ReportLab: the text, the tables, the heat map colours and the six figures. The heat map colours are computed in that script from the numbers themselves, so a changed number changes its colour automatically. Listing 2 shows the colour rule."))
story.append(Preformatted("def heat(t):\n"
                          "    # t from 0 (weak) to 1 (strong): red through yellow to green\n"
                          "    t = max(0.0, min(1.0, t))\n"
                          "    rgb = lerp(RED, YELLOW, t * 2) if t < 0.5 \\\n"
                          "        else lerp(YELLOW, GREEN, (t - 0.5) * 2)\n"
                          "    return colors.HexColor(\"#%02x%02x%02x\" % tuple(int(c * 255) for c in rgb))",
                          code_style))
story.append(P("Listing 2: Heat map colour rule, from scripts/build_report.py. Each table cell is coloured from its own value: red for weak, yellow in the middle, green for strong. Coverage uses a log scale, because it runs from 0.07 to 153 times. Z-prime and Springate are coloured against their published cut-offs, 2.6 and 0.862.", caption))
story.append(P("Verification. Every number in the report was checked against the file it came from before the report was built: the scorecard totals against Step-2-Scorecard.md, the transition figures against the analysis CSV files, and the credit results against credit/data/models.csv. The 2023 electricity figures were checked against the Fraser Institute's published 2023 numbers and matched exactly. Two figures were corrected during the project and the corrections are kept in the record: Imperial Oil's 2022 GHG figures were first taken from a secondary aggregator and replaced with the company's own report table, and the five energy names' combined 2024 operating cash flow was first written as about $50 billion and corrected to about $47 billion after recomputing it from the data."))
story.append(P("6. What was learned from this project", h1))
story.append(P("1. A sustainability score is a disclosure measure as much as a performance measure. Bill C-59 changed what three energy companies published, and their scores fell with it. A scorecard that does not flag disclosure gaps will misrank companies."))
story.append(P("2. No single credit model is the answer. Altman Z-prime rewards low leverage and penalises negative working capital. Springate rewards asset turnover and punishes a cyclical earnings trough. Zmijewski ranks leverage well but its absolute probabilities run high for capital-heavy firms. Merton says no one is near default, which is true and not very informative on its own. The four models together, plus plain leverage and cash flow ratios, give a defensible reading."))
story.append(P("3. Gross leverage and net leverage tell different stories. Teck at 5.59 times gross and 1.33 times net is the clearest case, and West Fraser at 0.37 times gross and -0.67 times net is the other. Cash on the balance sheet is part of credit strength, not a footnote."))
story.append(P("4. A one-off item can move a model more than the business did. Teck's $1,053 million write-off cut reported EBIT to $57 million and coverage to 0.07 times. The adjusted view, 1.43 times, is still weak, but it is a different conclusion from 0.07 times, and the report must show both."))
story.append(P("5. The transition is uneven by design. Power is changing and production is not, because the economics point different ways: wind and solar are cheap to build and oil and gas are profitable to produce. Capital spending is the leading indicator, and it is moving toward power."))
story.append(P("6. The data gaps are part of the finding. Freshwater intensity was disclosed by only 3 of 12 companies. Tourmaline's cash was missing from the standard data feed. Imperial published no 2024 sustainability report. A measurement standard for the resources universe has to be built around gaps like these, not in spite of them."))
story.append(P("7. Limits and method", h1))
story.append(P("One year, 2024, for both parts. The scores are disclosure-based: a company that reports more scores higher, and Bill C-59 made the energy scores partly a measure of what was published, not what was done. The credit models are backward-looking and use reported earnings, so one-off items like Teck's write-off move them. Merton says no company is near default, but that reflects market values at 31 December 2024. The transition data are Statistics Canada tables, and the 2025 and 2026 capital spending figures are intentions, not actuals. Ability to pay is not willingness to spend: this report does not test capital allocation plans, and a company with room on its balance sheet may still choose dividends and buybacks over transition investment. That choice is the next question, and it needs the companies' capital plans, not their 2024 financials."))
story.append(P("Sources", h1))
story.append(P("Sustainability reports for the 12 companies, 2024 editions, except Imperial Oil (2023 report covering 2022). Statistics Canada tables 25-10-0015-01, 25-10-0029-01 and 34-10-0035-01, downloaded 16 November 2026. Natural Resources Canada, Energy Fact Book 2025-2026, Section 2, for the power-specific capital spending split. Annual financials from Yahoo Finance, five years per company, with Tourmaline cash filled from Zacks' balance sheet and Teck net income from the Net Income Common Stockholders row, as stated in section 3. Scripts, data and the Excel model are in the project folder, so every number in the tables can be recomputed from the saved files."))
story.append(P("Appendix A: Files in this project", h1))
story.append(tbl([
["File", "What it does", "Outputs"],
["energy-projects/Step-1-Universe-and-Framework.md", "Scorecard universe and scoring rules", "Universe of 12, 4 measures, bands"],
["energy-projects/Step-2-Data-*.md", "Data read from each company's report", "Energy, mining, materials, last-disclosed-year files"],
["energy-projects/Step-2-Scorecard.md", "Ranking and the reason for each score", "Table 1"],
["energy-projects/Step-3-Returns-Test.md", "Returns test of scores against returns", "No link found"],
["energy-projects/returns-test/returns_test.py", "Downloads prices, runs the returns test", "prices_monthly.csv, returns_results.csv"],
["pull_statcan.py", "Downloads the three StatCan tables", "data/ full tables and metadata"],
["analyse.py", "Builds the Part A series and charts", "analysis_*.csv, charts/*.png"],
["Canada-Energy-Transition-Note.md", "Standalone Part A note", "Section 2 of this report"],
["credit/scripts/download_and_analyse.py", "Downloads financials, computes plain ratios", "credit/data/financials.csv, metrics.csv, latest.csv"],
["credit/scripts/analyse_models.py", "Runs the four credit models", "credit/data/models.csv"],
["credit/scripts/make_charts.py", "Builds the Part B charts", "credit/charts/*.png"],
["credit/Part-B-Results.md", "Standalone Part B results note", "Section 3 of this report"],
["Joint-Conclusion-Who-Can-Pay.md", "Joint conclusion note", "Section 4 of this report"],
["data/scorecard.csv", "Scorecard ranking as data", "Read by the model and notebook"],
["scripts/build_excel.py", "Builds the combined workbook", "Who_Can_Pay_for_the_Transition_Model.xlsx"],
["scripts/build_notebook.py", "Builds the recomputation notebook", "Who_Can_Pay_for_the_Transition_Notebook.ipynb"],
["scripts/build_report.py", "Builds this report", "Who_Can_Pay_for_the_Transition_Report.pdf"],
["README.md", "Project summary", "Question, answer, files, method and limits"],
], [52 * mm, 58 * mm, 60 * mm]))
doc = SimpleDocTemplate(str(base / "Who_Can_Pay_for_the_Transition_Report.pdf"), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm, title="Who Can Pay for the Transition", author="Munzeleen Sarwar")
doc.build(story)
print("report done")
