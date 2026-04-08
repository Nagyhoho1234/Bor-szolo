"""
s09_inject_extremes_into_descriptions.py
Add an honest, sourced 'climate_extremes_outlook' block to each per-district
description JSON so that fields previously assumed to be 'no data' (esp. hail
and convective storms, but also drought, frost, extreme rainfall) reference
the freshly-fetched CCKP CMIP6 extremes from s06b_cckp_extras.py.

Honesty rules:
- We say 'extreme 1-day precipitation' (rx1day) and explicitly call it a
  PROXY for severe convective storms — we never claim CMIP6 models hail.
- We cite the World Bank CCKP CMIP6 ensemble.
- All numbers come from the parquet files in analysis/curated/cckp/.
"""
import os, sys, io, json, shutil
from pathlib import Path

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import pandas as pd

ROOT = Path(r"C:\Bor-szőlő\analysis")
CCKP = ROOT / "curated" / "cckp"
DESC = ROOT / "curated" / "descriptions"
SITE_DESC_DIR = Path(r"C:\Bor-szőlő\site\public\data\descriptions")
SITE_DESC_AGG = Path(r"C:\Bor-szőlő\site\public\data\descriptions.json")

def load(var, scen, period):
    p = CCKP / f"cckp_cmip6_{var}_{scen}_per_district.parquet"
    df = pd.read_parquet(p)
    return df.query(f'period=="{period}" and stat=="mean"').set_index("borvidek")["value"]

def main():
    # Load all needed series
    rx1_h = load("rx1day", "historical", "1995-2014")
    rx1_f = load("rx1day", "ssp585",     "2080-2099")
    rx5_h = load("rx5day", "historical", "1995-2014")
    rx5_f = load("rx5day", "ssp585",     "2080-2099")
    cdd_h = load("cdd",    "historical", "1995-2014")
    cdd_f = load("cdd",    "ssp585",     "2080-2099")
    fd_h  = load("fd",     "historical", "1995-2014")
    fd_f  = load("fd",     "ssp585",     "2080-2099")
    tnn_h = load("tnn",    "historical", "1995-2014")
    tnn_f = load("tnn",    "ssp585",     "2080-2099")
    cwd_h = load("cwd",    "historical", "1995-2014")
    cwd_f = load("cwd",    "ssp585",     "2080-2099")
    gsl_h = load("gsl",    "historical", "1995-2014")
    gsl_f = load("gsl",    "ssp585",     "2080-2099")

    files = sorted([p for p in DESC.glob("*.json") if p.name != "descriptions.json"])
    print(f"Found {len(files)} per-district description files")

    updated = 0
    aggregate = {}

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            doc = json.load(f)
        b = doc.get("borvidek")
        slug = doc.get("slug", fp.stem)
        if b not in rx1_h.index:
            print(f"  WARN no CCKP row for {b}; skipping injection")
            aggregate[slug] = doc
            continue

        rx1h, rx1f = float(rx1_h[b]), float(rx1_f[b])
        rx5h, rx5f = float(rx5_h[b]), float(rx5_f[b])
        cddh, cddf = float(cdd_h[b]), float(cdd_f[b])
        fdh,  fdf  = float(fd_h[b]),  float(fd_f[b])
        tnnh, tnnf = float(tnn_h[b]), float(tnn_f[b])
        cwdh, cwdf = float(cwd_h[b]), float(cwd_f[b])
        gslh, gslf = float(gsl_h[b]), float(gsl_f[b])

        d_rx1 = rx1f - rx1h
        d_cdd = cddf - cddh
        d_fd  = fdf  - fdh
        d_tnn = tnnf - tnnh

        # Build a sourced, honest outlook block
        outlook = {
            "summary": (
                f"World Bank CCKP CMIP6 ensemble (1995-2014 baseline vs. 2080-2099 SSP5-8.5) "
                f"projects, for the {b} district centroid: "
                f"annual maximum 1-day precipitation rising from {rx1h:.1f} mm to {rx1f:.1f} mm "
                f"(+{d_rx1:.1f} mm, a proxy for severe-storm intensity); "
                f"longest annual dry spell from {cddh:.1f} to {cddf:.1f} days "
                f"({'+' if d_cdd>=0 else ''}{d_cdd:.1f}); "
                f"frost days from {fdh:.0f} to {fdf:.0f} days/year "
                f"({'+' if d_fd>=0 else ''}{d_fd:.0f}); "
                f"annual coldest night from {tnnh:.1f} \u00b0C to {tnnf:.1f} \u00b0C."
            ),
            "hail_caveat": (
                "CMIP6 climate models do not directly simulate hail. The closest "
                "physical proxy in this dataset is rx1day (annual maximum 1-day "
                "precipitation), which captures convective storm intensity. "
                "True hail event records are not part of the World Bank CCKP "
                "collection or HungaroMet's open daily station data."
            ),
            "metrics": {
                "rx1day_mm_hist_1995_2014":  round(rx1h, 2),
                "rx1day_mm_ssp585_2080_2099": round(rx1f, 2),
                "rx5day_mm_hist_1995_2014":  round(rx5h, 2),
                "rx5day_mm_ssp585_2080_2099": round(rx5f, 2),
                "cdd_days_hist_1995_2014":   round(cddh, 2),
                "cdd_days_ssp585_2080_2099": round(cddf, 2),
                "cwd_days_hist_1995_2014":   round(cwdh, 2),
                "cwd_days_ssp585_2080_2099": round(cwdf, 2),
                "frost_days_hist_1995_2014": round(fdh, 1),
                "frost_days_ssp585_2080_2099": round(fdf, 1),
                "tnn_c_hist_1995_2014":      round(tnnh, 2),
                "tnn_c_ssp585_2080_2099":    round(tnnf, 2),
                "growing_season_length_days_hist_1995_2014": round(gslh, 1),
                "growing_season_length_days_ssp585_2080_2099": round(gslf, 1),
            },
            "source": "World Bank Climate Change Knowledge Portal — CMIP6 ensemble (cmip6-x0.25), district-centroid nearest grid sample.",
            "source_url": "https://climateknowledgeportal.worldbank.org/",
        }

        doc["climate_extremes_outlook"] = outlook

        # Also append a human-readable note to top_sources if not already there
        cckp_note = {
            "title": "World Bank Climate Change Knowledge Portal — CMIP6 ensemble extremes (cdd, rx1day, rx5day, fd, tnn, gsl)",
            "url": "https://climateknowledgeportal.worldbank.org/"
        }
        srcs = doc.get("top_sources", []) or []
        if not any(s.get("url","").startswith("https://climateknowledgeportal") for s in srcs):
            srcs.append(cckp_note)
            doc["top_sources"] = srcs

        with open(fp, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        aggregate[slug] = doc
        updated += 1
        print(f"  updated {fp.name}")

    # Re-aggregate
    agg_path = DESC / "descriptions.json"
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(aggregate, f, ensure_ascii=False, indent=2)
    print(f"Re-wrote {agg_path.name} ({len(aggregate)} entries)")

    # Sync to site
    SITE_DESC_DIR.mkdir(parents=True, exist_ok=True)
    for fp in DESC.glob("*.json"):
        shutil.copy2(fp, SITE_DESC_DIR / fp.name)
    shutil.copy2(agg_path, SITE_DESC_AGG)
    print(f"Synced {len(list(DESC.glob('*.json')))} files to {SITE_DESC_DIR}")
    print(f"Synced aggregate to {SITE_DESC_AGG}")
    print(f"Total updates: {updated}")

if __name__ == "__main__":
    main()
