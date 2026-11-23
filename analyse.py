"""Analyse StatCan data for the Canada energy transition note (Part A).

Window: 2015 to 2024, the latest complete year in all three tables.
- Electricity generation by source (25-10-0015-01), Canada, all classes.
  Fuel split charted 2016-2024: the published combustible-fuels aggregate
  starts in 2016 and the non-renewable split in 2020, so 2015 is used only
  for levels and growth rates of hydro, nuclear, wind and solar.
- Primary energy production by fuel (25-10-0029-01), Canada, terajoules.
  Shown in exajoules (1 EJ = 1,000 PJ = 1,000,000 TJ).
- Capital expenditures by industry (34-10-0035-01), Canada, $ millions.
  The table splits utilities only to Utilities [22], so the power-specific
  $32bn figure for 2024 is quoted from NRCan's Energy Fact Book, not from
  this table. 2025 and 2026 are intentions, shown only as a forward look.

Run: ./venv/bin/python analyse.py
"""

import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False})
GREEN = "#1D5C30"
GREY = "#6B7280"
DARK = "#111111"

os.makedirs("charts", exist_ok=True)
YEARS = list(range(2015, 2025))

# ---------------------------------------------------------------- electricity
elec = pd.read_csv("data/electricity_generation.csv", low_memory=False)
e = elec[(elec["GEO"] == "Canada")
         & (elec["Class of electricity producer"] == "Total all classes of electricity producer")].copy()
e["year"] = e["REF_DATE"].str[:4].astype(int)
e = e[e["year"].isin(YEARS)]
annual = e.groupby(["year", "Type of electricity generation"])["VALUE"].sum().unstack() / 1e6  # MWh -> TWh

# 2015 levels (turbine-type breakdown) for growth rates
base_2015 = annual.loc[2015]
for name, col in [("Wind", "Wind power turbine"), ("Solar", "Solar"),
                  ("Hydro", "Hydraulic turbine"), ("Nuclear", "Nuclear steam turbine")]:
    print(f"{name} 2015: {base_2015[col]:.2f} TWh -> 2024: {annual.loc[2024, col]:.2f} TWh "
          f"({100 * (annual.loc[2024, col] / base_2015[col] - 1):+.1f}%)")

# Fuel split 2016-2024 from published aggregates
split = pd.DataFrame({
    "Total": annual["Total all types of electricity generation"],
    "Hydro": annual["Hydraulic turbine"],
    "Nuclear": annual["Nuclear steam turbine"],
    "Wind": annual["Wind power turbine"],
    "Solar": annual["Solar"],
    "Combustible fuels": annual["Total electricity production from combustible fuels"],
})
split = split.loc[2016:2024]
split["Wind, solar and other renewables"] = (split["Total"] - split["Hydro"] - split["Nuclear"]
                                             - split["Combustible fuels"])
split["Hydro share %"] = 100 * split["Hydro"] / split["Total"]
split["Combustible share %"] = 100 * split["Combustible fuels"] / split["Total"]
split["Wind+solar share %"] = 100 * (split["Wind"] + split["Solar"]) / split["Total"]
split.to_csv("analysis_electricity.csv")
print(split.round(2).to_string())
print()
print("Fossil (non-renewable combustible) 2024: %.2f TWh, %.1f%% of total"
      % (annual.loc[2024, "Total electricity production from non-renewable combustible fuels"],
         100 * annual.loc[2024, "Total electricity production from non-renewable combustible fuels"]
         / annual.loc[2024, "Total all types of electricity generation"]))
print("Renewables (hydro+wind+solar+tidal+biomass) 2024: %.2f TWh, %.1f%% of total"
      % (annual.loc[2024, "Hydraulic turbine"] + annual.loc[2024, "Wind power turbine"]
         + annual.loc[2024, "Solar"] + annual.loc[2024, "Tidal power turbine"]
         + annual.loc[2024, "Total electricity production from biomass"],
         100 * (annual.loc[2024, "Hydraulic turbine"] + annual.loc[2024, "Wind power turbine"]
         + annual.loc[2024, "Solar"] + annual.loc[2024, "Tidal power turbine"]
         + annual.loc[2024, "Total electricity production from biomass"])
         / annual.loc[2024, "Total all types of electricity generation"]))

# Chart 1: stacked generation by source, 2016-2024
fig, ax = plt.subplots(figsize=(8.5, 4.2))
x = split.index.values
ax.bar(x, split["Hydro"], label="Hydro", color="#1D5C30")
ax.bar(x, split["Nuclear"], bottom=split["Hydro"], label="Nuclear", color="#9CA3AF")
ax.bar(x, split["Combustible fuels"], bottom=split["Hydro"] + split["Nuclear"],
       label="Combustible fuels", color="#111111")
ax.bar(x, split["Wind, solar and other renewables"],
       bottom=split["Hydro"] + split["Nuclear"] + split["Combustible fuels"],
       label="Wind, solar and other renewables", color="#8FBC8F")
ax.set_ylabel("TWh")
ax.set_title("Electricity generation in Canada by source, 2016-2024", color=DARK, loc="left")
ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.12))
fig.tight_layout()
fig.savefig("charts/electricity_by_source.png", dpi=150)
plt.close(fig)

# ------------------------------------------------------- energy supply/demand
esd = pd.read_csv("data/energy_supply_demand.csv", low_memory=False)
s = esd[(esd["GEO"] == "Canada") & (esd["REF_DATE"].astype(int).isin(YEARS))].copy()
s = s.rename(columns={"REF_DATE": "year"})
prod = s[s["Supply and demand characteristics"] == "Production"]
fuels = ["Total coal", "Crude oil", "Natural gas",
         "Primary electricity, hydro, nuclear, and other renewables",
         "Primary energy", "Total primary and secondary energy"]
piv = prod[prod["Fuel type"].isin(fuels)].pivot(index="year", columns="Fuel type", values="VALUE")
piv = piv / 1e6  # TJ -> EJ
piv["Oil and gas"] = piv["Crude oil"] + piv["Natural gas"]
piv["Fossil share of primary %"] = 100 * (piv["Total coal"] + piv["Oil and gas"]) / piv["Primary energy"]
piv["Primary electricity share of primary %"] = (
    100 * piv["Primary electricity, hydro, nuclear, and other renewables"] / piv["Primary energy"])
piv.to_csv("analysis_energy_production.csv")
print(piv.round(2).to_string())
print()
for f in ["Crude oil", "Natural gas", "Total coal",
          "Primary electricity, hydro, nuclear, and other renewables", "Primary energy"]:
    print(f, "2015->2024: %+.1f%%" % (100 * (piv.loc[2024, f] / piv.loc[2015, f] - 1)))

# Chart 2: primary energy production by fuel
fig, ax = plt.subplots(figsize=(8.5, 4.2))
x = piv.index.values
ax.bar(x, piv["Crude oil"], label="Crude oil", color="#111111")
ax.bar(x, piv["Natural gas"], bottom=piv["Crude oil"], label="Natural gas", color="#6B7280")
ax.bar(x, piv["Total coal"], bottom=piv["Crude oil"] + piv["Natural gas"], label="Coal", color="#9CA3AF")
ax.bar(x, piv["Primary electricity, hydro, nuclear, and other renewables"],
       bottom=piv["Crude oil"] + piv["Natural gas"] + piv["Total coal"],
       label="Primary electricity (hydro, nuclear, renewables)", color="#1D5C30")
ax.set_ylabel("Exajoules")
ax.set_title("Primary energy production in Canada by fuel, 2015-2024", color=DARK, loc="left")
ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.12))
fig.tight_layout()
fig.savefig("charts/primary_energy_production.png", dpi=150)
plt.close(fig)

# ------------------------------------------------------------------- capex
cap = pd.read_csv("data/capital_expenditures.csv", low_memory=False)
c = cap[(cap["GEO"] == "Canada")
        & (cap["Capital and repair expenditures"] == "Capital expenditures")
        & (cap["North American Industry Classification System (NAICS)"].isin(
            ["Oil and gas extraction [211]", "Utilities [22]"]))].copy()
c = c.rename(columns={"REF_DATE": "year",
                      "North American Industry Classification System (NAICS)": "industry"})
cpiv = c.pivot(index="year", columns="industry", values="VALUE")
cpiv = cpiv.loc[2015:2024]
cpiv.to_csv("analysis_capex.csv")
print(cpiv.round(1).to_string())
print()
for ind in ["Oil and gas extraction [211]", "Utilities [22]"]:
    print(ind, "2015->2024: %+.1f%%" % (100 * (cpiv.loc[2024, ind] / cpiv.loc[2015, ind] - 1)))
print("Oil and gas 2014 peak: %.1f; 2020 low: %.1f"
      % (c[c["industry"] == "Oil and gas extraction [211]"].set_index("year").loc[2014, "VALUE"],
         c[c["industry"] == "Oil and gas extraction [211]"].set_index("year").loc[2020, "VALUE"]))
print("2025 intentions: oil and gas %.1f, utilities %.1f"
      % (c[c["industry"] == "Oil and gas extraction [211]"].set_index("year").loc[2025, "VALUE"],
         c[c["industry"] == "Utilities [22]"].set_index("year").loc[2025, "VALUE"]))

# Chart 3: capex, oil and gas vs utilities
fig, ax = plt.subplots(figsize=(8.5, 4.2))
years = cpiv.index.values
ax.plot(years, cpiv["Oil and gas extraction [211]"], marker="o", color="#111111",
        label="Oil and gas extraction")
ax.plot(years, cpiv["Utilities [22]"], marker="o", color="#1D5C30",
        label="Utilities (mostly electric power)")
ax.set_ylabel("$ millions")
ax.set_title("Capital expenditures, oil and gas against utilities, 2015-2024", color=DARK, loc="left")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
fig.tight_layout()
fig.savefig("charts/capex_oil_gas_vs_utilities.png", dpi=150)
plt.close(fig)
print("charts written")
