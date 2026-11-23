# Part B results: credit risk on the 12 scorecard companies, 2024 annuals

Model year 2024, to match the scorecard year. All money in CAD millions.
USD reporters (Barrick, Agnico, Nutrien, Methanex, West Fraser) converted
at USD/CAD 1.435, the close on 31 Dec 2024. Ratios are currency free.
Merton is point-in-time at 31 Dec 2024: 1-year daily volatility over 2024,
market value at the 31 Dec 2024 close times current shares outstanding
(an approximation), default point from 2024 liabilities, risk free rate
3.0%. Synthetic rating comes from interest coverage bands (AAA at 8.5x
and above, BBB at 2.5x, BB+ at 2.0x, B at 1.25x).

## Headline table, 2024

| Company | Debt / EBITDA | Net debt / EBITDA | Coverage | Z-prime | Springate | Zmijewski % | Merton DD | Synthetic |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Agnico Eagle | 0.29 | 0.08 | 33.6 | 3.54 | 1.72 | 5.3 | 9.67 | AAA |
| West Fraser | 0.37 | -0.67 | 2.5 | 6.53 | 0.46 | 4.1 | 8.93 | BB+ |
| Tourmaline | 0.40 | 0.30 | 21.4 | 3.65 | 1.09 | 5.4 | 9.67 | AAA |
| Imperial Oil | 0.50 | 0.38 | 153.2 | 4.33 | 1.55 | 9.5 | 8.79 | AAA |
| Barrick | 0.76 | 0.17 | 11.9 | 2.13 | 1.80 | 14.9 | 8.10 | AAA |
| Suncor | 0.93 | 0.71 | 12.8 | 2.74 | 1.13 | 14.6 | 9.77 | AAA |
| Cenovus | 1.11 | 0.79 | 7.3 | 2.69 | 1.14 | 13.1 | 8.37 | AA |
| CNQ | 1.22 | 1.21 | 13.0 | 2.49 | 1.08 | 16.8 | 9.60 | AAA |
| Cameco | 1.93 | 1.02 | 3.0 | 3.66 | 0.54 | 8.5 | 6.91 | A- |
| Nutrien | 3.04 | 2.84 | 2.5 | 2.10 | 0.45 | 20.0 | 8.62 | BBB |
| Methanex | 4.05 | 2.93 | 3.1 | 2.89 | 0.98 | 36.3 | 7.72 | A- |
| Teck | 5.59 | 1.33 | 0.1 | 3.64 | 0.27 | 13.8 | 7.14 | CCC or lower |

Cut-offs: Z-prime above 2.6 is safe, 1.1 to 2.6 grey, below 1.1 distress.
Springate above 0.862 is safe, below is distress. Zmijewski is a
probability of failure; use the ranking, not the level. Merton distance to
default above 3 is far from default; every company here is above 6.9.

## What the models agree on

Methanex and Nutrien are the genuinely stretched names. Every model
points the same way: highest leverage (4.05x and 3.04x), highest net
leverage (2.93x and 2.84x), thinnest cash flow cover (operating cash flow
to debt 0.23x and 0.28x, free cash flow to debt 0.17x and 0.11x), highest
Zmijewski probabilities (36.3% and 20.0%), lowest synthetic ratings
(A- and BBB). Methanex leverage is not new: it was 3.79x in 2023 and
4.04x in 2025, so this is a persistent position, not one bad year.

Agnico, Imperial, Tourmaline, Suncor, Barrick and CNQ are the strong
balance sheets: leverage under 1.3x, coverage above 11x, operating cash
flow to debt above 0.7x. Agnico is the strongest on leverage (0.29x) and
cash flow (operating cash flow 3.09x its debt, free cash flow 1.66x).

## Where the models disagree, and why

Teck looks worst on gross leverage (5.59x) and coverage (0.07x), but its
net leverage is only 1.33x because it held $7,587m of cash at the end of
2024 from the steelmaking coal sale. Its 2024 EBIT of $57m includes a
$1,053m write-off; on adjusted EBIT of $1,110m, coverage is 1.43x,
Z-prime 3.79 (from 3.64) and Springate 0.50 (from 0.27), still below the
0.862 Springate cut-off. Even adjusted, Teck is weak on earnings cover:
interest expense of $775m is large next to post-coal earnings. Merton
gives Teck a distance to default of 7.14, far from default, because the
market value is large next to the default point. The honest reading:
Teck is not in distress, but it is the most leveraged name on earnings
and the thinnest on interest cover.

West Fraser is the model disagreement. Z-prime says safest in the set
(6.53) because it has almost no debt: net cash of $591m, net debt to
EBITDA of -0.67x. Springate says distress (0.46) because 2024 EBIT was
only $92m after the lumber downturn. A net-cash company is not in
distress; its earnings collapsed for a year. Springate is an earnings
model and it punishes a cyclical trough. The balance sheet is the truth
here.

Cameco fails Springate (0.54) for a structural reason, not a credit
reason: revenue to assets is only 0.32, because uranium mining is
capital heavy, and EBIT to assets is only 0.039. Springate rewards
asset turnover, so capital-heavy miners score low. Cameco leverage is
1.93x and coverage is 3.0x, which is middle of the set, not distress.

Imperial coverage of 153.2x is arithmetically right but should not be
quoted on its own: interest expense was only $41m in 2024, confirmed by
interest paid of $42m. The rating is AAA either way, but the number
reflects a tiny interest bill, not infinite strength.

CNQ sits in the Z-prime grey zone (2.49) despite 13.0x coverage and
1.22x leverage, because working capital is negative (-$2,226m) and the
equity to liabilities ratio is only 0.86. Negative working capital is
normal for oil producers and Z-prime penalises it. Do not call CNQ grey
without that sentence.

## Data notes

Tourmaline cash is a manual fill: yfinance has no cash row at all for
Tourmaline, so cash and equivalents of $319m at 31 Dec 2024 come from
Zacks' balance sheet, which reproduces the company's filings (2023:
$353m, 2025: $130m). Net debt for Tourmaline depends on that figure.
Teck net income of $406m uses the "Net Income Common Stockholders" row,
because the "Net Income" row is missing for Teck in 2024; the $406m is
net income after a $1,206m gain from discontinued operations (the coal
sale) and a $923m loss from continuing operations.

## Files

- data/financials.csv (5 years per company), data/metrics.csv,
  data/latest.csv (2025, kept for trend context only), data/models.csv
  (2024 model results).
- charts/debt_ebitda.png, charts/zmijewski_prob.png,
  charts/coverage_vs_leverage.png.
- scripts/download_and_analyse.py, scripts/analyse_models.py,
  scripts/make_charts.py.
