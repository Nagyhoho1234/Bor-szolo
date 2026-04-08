"""Step 2 — compute viticulture indices for all districts/scenarios/years."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
sys.path.insert(0, str(ANALYSIS / "src"))

from common.vit_indices import (  # noqa: E402
    winkler_gdd, winkler_class,
    huglin_index, huglin_class,
    late_spring_frost_days, last_spring_frost_doy,
    heat_days, growing_season_precip,
    hargreaves_pet_annual, p_minus_pet, cool_night_index,
)

GPKG = ANALYSIS / "geo" / "wine_districts.gpkg"
DAILY_DIR = ANALYSIS / "interim" / "daily"
ANNUAL_DIR = ANALYSIS / "interim" / "annual"
ANNUAL_DIR.mkdir(parents=True, exist_ok=True)

INDEX_DEFS = {
    "winkler_gdd":            ("degC_day", "Winkler growing degree days (Apr1-Oct31)"),
    "huglin_index":           ("degC_day", "Huglin heliothermal index (Apr1-Sep30)"),
    "spring_frost_days":      ("days",     "Days with tmin<0 in Mar-May"),
    "last_spring_frost_doy":  ("doy",      "Latest day-of-year with tmin<0 (Jan-Jun15)"),
    "heat_days_t35":          ("days",     "Days with tmax>35 in Jun-Aug"),
    "extreme_heat_days_t38":  ("days",     "Days with tmax>38 in Jun-Aug"),
    "growing_season_precip":  ("mm",       "Precipitation Apr1-Oct31"),
    "hargreaves_pet":         ("mm",       "Hargreaves PET Apr1-Oct31"),
    "p_minus_pet":            ("mm",       "P-PET Apr1-Oct31"),
    "cool_night_index":       ("degC",     "Mean tmin September"),
}


def long_format(df_annual: pd.DataFrame, idx_name: str, scen: str, units: str,
                index_class_fn=None) -> pd.DataFrame:
    rows = []
    for year, row in df_annual.iterrows():
        for dist, val in row.items():
            cls = index_class_fn(val) if index_class_fn else None
            rows.append((int(year), dist, np.float32(val) if pd.notna(val) else np.nan,
                         units, scen, cls, idx_name))
    return pd.DataFrame(rows, columns=["year", "borvidek", "value", "units",
                                        "scenario", "index_class", "index"])


def compute_for_scenario(scen: str, lats: pd.Series) -> dict[str, pd.DataFrame]:
    print(f"[s02] Loading {scen} dailies...")
    tmax = pd.read_parquet(DAILY_DIR / f"tmax_{scen}_stitched_1971-2100.parquet")
    tmin = pd.read_parquet(DAILY_DIR / f"tmin_{scen}_stitched_1971-2100.parquet")
    pr   = pd.read_parquet(DAILY_DIR / f"pr_{scen}_stitched_1971-2100.parquet")

    print(f"[s02] {scen}: {len(tmax)} daily rows, {len(tmax.columns)} districts")
    out: dict[str, pd.DataFrame] = {}

    out["winkler_gdd"] = winkler_gdd(tmax, tmin)
    out["huglin_index"] = huglin_index(tmax, tmin, lats)
    out["spring_frost_days"] = late_spring_frost_days(tmin)
    out["last_spring_frost_doy"] = last_spring_frost_doy(tmin)
    out["heat_days_t35"] = heat_days(tmax, 35.0)
    out["extreme_heat_days_t38"] = heat_days(tmax, 38.0)
    out["growing_season_precip"] = growing_season_precip(pr)
    pet_annual = hargreaves_pet_annual(tmax, tmin, lats)
    out["hargreaves_pet"] = pet_annual
    out["p_minus_pet"] = p_minus_pet(out["growing_season_precip"], pet_annual)
    out["cool_night_index"] = cool_night_index(tmin)

    return out


def main():
    t0 = time.time()
    districts = gpd.read_file(GPKG)
    lats = pd.Series(districts.centroid_lat.values, index=districts.borvidek.values)

    for scen in ("rcp45", "rcp85"):
        annuals = compute_for_scenario(scen, lats)
        wide_cols = {}
        for idx_name, df in annuals.items():
            units, _ = INDEX_DEFS[idx_name]
            class_fn = (winkler_class if idx_name == "winkler_gdd"
                        else huglin_class if idx_name == "huglin_index"
                        else None)
            longdf = long_format(df, idx_name, scen, units, class_fn)
            longdf.to_parquet(ANNUAL_DIR / f"{idx_name}_{scen}_annual.parquet")
            wide_cols[idx_name] = df

        # Wide convenience: one row per (year, borvidek)
        first = next(iter(wide_cols.values()))
        years = first.index
        recs = []
        for y in years:
            for d in first.columns:
                rec = {"year": int(y), "borvidek": d}
                for k, df in wide_cols.items():
                    rec[k] = float(df.loc[y, d]) if y in df.index and d in df.columns else np.nan
                recs.append(rec)
        wide = pd.DataFrame(recs)
        wide_path = ANNUAL_DIR / f"indices_wide_{scen}.parquet"
        wide.to_parquet(wide_path)
        print(f"[s02] {scen}: wrote {len(annuals)} long parquets + wide ({len(wide)} rows)")

    n_files = len(list(ANNUAL_DIR.glob("*.parquet")))
    total = sum(p.stat().st_size for p in ANNUAL_DIR.glob("*.parquet")) / 1e6
    print(f"[s02] DONE in {time.time()-t0:.1f}s; {n_files} parquet files, {total:.2f} MB")


if __name__ == "__main__":
    main()
