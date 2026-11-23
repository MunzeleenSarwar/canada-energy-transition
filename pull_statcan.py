"""Pull StatCan tables for the Canada energy transition note (Part A).

Tables (Web Data Service, full-table CSV download):
- 25100015 (25-10-0015-01): electricity supply and disposition, by type
  of generation, monthly.
- 25100029 (25-10-0029-01): supply and demand of primary and secondary
  energy in terajoules, annual.
- 34100035 (34-10-0035-01): capital expenditures, by industry, annual.

Run from the energy-transition folder: ./venv/bin/python pull_statcan.py
"""

import io
import time
import zipfile

import requests

TABLES = {
    "electricity_generation": "25100015",
    "energy_supply_demand": "25100029",
    "capital_expenditures": "34100035",
}

BASE = "https://www150.statcan.gc.ca/n1/wds/rest"


def download_table(product_id, out_csv):
    url = f"{BASE}/getFullTableDownloadCSV/{product_id}/en"
    for attempt in range(3):
        resp = requests.post(url, timeout=120)
        resp.raise_for_status()
        payload = resp.json()
        obj = payload.get("object")
        if obj:
            z = requests.get(obj, timeout=300)
            z.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(z.content)) as zf:
                names = [n for n in zf.namelist() if n.endswith(".csv")]
                data = zf.read(names[0])
            with open(out_csv, "wb") as f:
                f.write(data)
            print(f"{product_id} -> {out_csv} ({len(data) / 1e6:.1f} MB)")
            return
        print(f"attempt {attempt + 1}: no object URL, retrying")
        time.sleep(10)
    raise RuntimeError(f"no object URL for {product_id}: {payload}")


if __name__ == "__main__":
    for name, product_id in TABLES.items():
        download_table(product_id, f"data/{name}.csv")
    print("done")
