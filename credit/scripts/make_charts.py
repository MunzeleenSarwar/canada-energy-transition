"""Part B charts, 2024 model year. Colours are for charts only, per her rule."""
import pathlib

import matplotlib.pyplot as plt
import pandas as pd

base = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
models = pd.read_csv(base / "data" / "models.csv")
met = pd.read_csv(base / "data" / "metrics.csv")
m24 = met[met.fiscal_year_end.str.startswith("2024")].set_index("ticker")
d = models.set_index("ticker").join(m24[["total_debt", "cash", "net_debt", "ebitda"]])
d["net_debt_ebitda"] = d["net_debt"] / d["ebitda"]

# 1. Debt to EBITDA, 2024, sorted
s = d.sort_values("debt_ebitda")
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(s["company"], s["debt_ebitda"], color="#1D5C30")
ax.axvline(3.0, color="#9CA3AF", linewidth=1, linestyle="--")
ax.text(3.05, len(s) - 0.5, "3x, a common caution line", fontsize=9, color="#555555")
ax.set_xlabel("Total debt divided by EBITDA, times")
ax.set_title("Debt to EBITDA, 2024 annuals")
fig.tight_layout()
fig.savefig(base / "charts" / "debt_ebitda.png", dpi=200)
plt.close(fig)

# 2. Zmijewski probability of failure, 2024, sorted
s = d.sort_values("zmijewski_prob_pct")
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(s["company"], s["zmijewski_prob_pct"], color="#1D5C30")
ax.set_xlabel("Zmijewski probability of failure, %")
ax.set_title("Zmijewski probability, 2024 annuals (ranking, not a literal chance)")
fig.tight_layout()
fig.savefig(base / "charts" / "zmijewski_prob.png", dpi=200)
plt.close(fig)

# 3. Leverage against coverage, 2024, log scale for coverage
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(d["debt_ebitda"], d["interest_coverage"], s=90, color="#1D5C30")
for tick, row in d.iterrows():
    ax.annotate(tick, (row["debt_ebitda"], row["interest_coverage"]),
                textcoords="offset points", xytext=(5, 5), fontsize=9)
ax.axvline(3.0, color="#9CA3AF", linewidth=1, linestyle="--")
ax.axhline(3.0, color="#9CA3AF", linewidth=1, linestyle="--")
ax.set_xlabel("Debt to EBITDA, times")
ax.set_ylabel("Interest coverage, times (log scale)")
ax.set_yscale("log")
ax.set_title("Leverage against interest coverage, 2024 annuals")
fig.tight_layout()
fig.savefig(base / "charts" / "coverage_vs_leverage.png", dpi=200)
plt.close(fig)
print("charts done")
