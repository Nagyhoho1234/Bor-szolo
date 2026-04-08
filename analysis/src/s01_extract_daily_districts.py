"""Step 1 — extract area-weighted daily climate per wine district.

Reads all 13 FORESEE NetCDFs, builds a (22 x ngrid) weight matrix once
via regionmask, and computes a (T x 22) DataFrame for each variable/scenario
in a single matmul. Stitches observed + RCP into 1971-2100 daily series.

Outputs in analysis/interim/daily/:
    <var>_<scenario>_daily_per_district.parquet      (raw, per file)
    <var>_<scenario>_stitched_1971-2100.parquet      (var in {tmax,tmin,pr})
And a weight matrix at analysis/interim/district_weights.npz
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
import regionmask

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
sys.path.insert(0, str(ANALYSIS / "src"))

from common.foresee_io import (  # noqa: E402
    list_foresee_files,
    open_foresee,
    get_lat_lon,
    get_lat_lon_1d,
    read_daily_cube,
    detect_scenario,
    detect_logical_var,
)

GPKG = ANALYSIS / "geo" / "wine_districts.gpkg"
INTERIM = ANALYSIS / "interim"
DAILY_DIR = INTERIM / "daily"
WEIGHTS_NPZ = INTERIM / "district_weights.npz"

DAILY_DIR.mkdir(parents=True, exist_ok=True)


def build_weights(districts: gpd.GeoDataFrame) -> tuple[np.ndarray, list[str], np.ndarray, np.ndarray, list[str]]:
    """Build a (22, ngrid) area-weighted matrix using regionmask.

    Returns
    -------
    W : float32 array (22, ny*nx); rows sum to 1.0
    names : list of borvidek names in row order
    lats_1d, lons_1d : grid coordinates (1-D, in deg)
    fallback : list of district names where mask was empty -> nearest cell used
    """
    sample_nc = next(p for p in list_foresee_files() if "observed" in p.lower() and "tmax" in p.lower())
    ds = open_foresee(sample_nc)
    lats_1d, lons_1d = get_lat_lon_1d(ds)
    ds.close()

    ny, nx = len(lats_1d), len(lons_1d)
    names = list(districts["borvidek"].values)

    regs = regionmask.from_geopandas(districts, names="borvidek", name="borvidek")
    mask3d = regs.mask_3D(lons_1d, lats_1d)  # (region, lat, lon) bool

    W = np.zeros((len(names), ny * nx), dtype=np.float32)
    fallback: list[str] = []

    # Approximate cell area weight via cos(lat) — uniform 0.1 deg grid
    coslat = np.cos(np.deg2rad(lats_1d))[:, None] * np.ones((1, nx), dtype=np.float64)
    cell_area = coslat.ravel().astype(np.float32)

    region_ids = list(mask3d.region.values)
    for i, name in enumerate(names):
        if i in region_ids:
            mask2d = mask3d.sel(region=i).values.astype(bool)
        else:
            mask2d = np.zeros((ny, nx), dtype=bool)
        flat = mask2d.ravel()
        if flat.any():
            w = flat.astype(np.float32) * cell_area
        else:
            # Fallback: nearest grid cell to centroid
            clat = float(districts.iloc[i]["centroid_lat"])
            clon = float(districts.iloc[i]["centroid_lon"])
            jy = int(np.argmin(np.abs(lats_1d - clat)))
            jx = int(np.argmin(np.abs(lons_1d - clon)))
            w = np.zeros(ny * nx, dtype=np.float32)
            w[jy * nx + jx] = 1.0
            fallback.append(name)
        W[i] = w / w.sum()

    return W, names, lats_1d, lons_1d, fallback


def extract_one(path: str, W: np.ndarray, names: list[str]) -> pd.DataFrame:
    """Return a (T x 22) DataFrame for one NetCDF (var aggregated by W)."""
    arr, dates, var = read_daily_cube(path)
    T, Y, X = arr.shape
    flat = arr.reshape(T, Y * X)
    # Replace NaNs with 0 only where weight is 0; otherwise use nan-aware mean
    if np.isnan(flat).any():
        # weighted nan-mean per district
        mask = ~np.isnan(flat)
        # numerator: sum over cells of value * weight (treating NaN as 0)
        flat_z = np.where(mask, flat, 0.0)
        num = flat_z @ W.T            # (T, 22)
        denom = mask.astype(np.float32) @ W.T
        denom[denom == 0] = np.nan
        out = num / denom
    else:
        out = flat @ W.T              # already area-normalized rows
    df = pd.DataFrame(out, index=pd.DatetimeIndex(dates, name="date"), columns=names)
    return df


def main():
    t0 = time.time()
    print("[s01] Loading districts...")
    districts = gpd.read_file(GPKG).to_crs("EPSG:4326").reset_index(drop=True)
    print(f"[s01] {len(districts)} districts; columns: {list(districts.columns)}")

    print("[s01] Building weight matrix...")
    W, names, lats_1d, lons_1d, fallback = build_weights(districts)
    print(f"[s01] Weight matrix shape: {W.shape}, rows sum range: "
          f"{W.sum(axis=1).min():.4f}-{W.sum(axis=1).max():.4f}")
    if fallback:
        print(f"[s01] Nearest-cell fallback used for: {fallback}")
    else:
        print("[s01] No fallback needed.")

    np.savez(WEIGHTS_NPZ,
             W=W,
             names=np.array(names, dtype=object),
             lats=lats_1d,
             lons=lons_1d,
             fallback=np.array(fallback, dtype=object))
    print(f"[s01] Saved weights -> {WEIGHTS_NPZ}")

    files = list_foresee_files()
    print(f"[s01] Found {len(files)} NetCDF files")
    raw_outputs: dict[tuple[str, str], pd.DataFrame] = {}

    for f in files:
        scen = detect_scenario(f)
        var = detect_logical_var(f)
        print(f"[s01] -> {os.path.basename(f)}  var={var}  scen={scen}")
        df = extract_one(f, W, names)
        out_path = DAILY_DIR / f"{var}_{scen}_daily_per_district.parquet"
        df.to_parquet(out_path)
        # sanity
        print(f"      dates {df.index.min().date()}..{df.index.max().date()}, "
              f"n={len(df.index.unique())}, "
              f"min={np.nanmin(df.values):.2f} mean={np.nanmean(df.values):.2f} max={np.nanmax(df.values):.2f}")
        zeros = [c for c in df.columns if np.all(df[c].values == 0)]
        if zeros:
            print(f"      WARNING all-zero columns: {zeros}")
        raw_outputs[(var, scen)] = df

    # Stitch observed + rcp for tmax/tmin/pr
    print("[s01] Stitching observed + RCP series...")
    for var in ("tmax", "tmin", "pr"):
        obs = raw_outputs.get((var, "observed"))
        if obs is None:
            print(f"[s01] No observed file for {var}, skipping stitch")
            continue
        obs_part = obs.loc[:"2021-12-31"]
        for scen in ("rcp45", "rcp85"):
            rcp = raw_outputs.get((var, scen))
            if rcp is None:
                print(f"[s01] No {scen} file for {var}, skipping")
                continue
            rcp_part = rcp.loc["2022-01-01":]
            stitched = pd.concat([obs_part, rcp_part], axis=0)
            stitched = stitched[~stitched.index.duplicated(keep="first")].sort_index()
            out = DAILY_DIR / f"{var}_{scen}_stitched_1971-2100.parquet"
            stitched.to_parquet(out)
            print(f"[s01] {out.name}: {stitched.index.min().date()}..{stitched.index.max().date()}, "
                  f"n_rows={len(stitched)}")

    dt = time.time() - t0
    n_files = len(list(DAILY_DIR.glob("*.parquet")))
    total = sum(p.stat().st_size for p in DAILY_DIR.glob("*.parquet")) / 1e6
    print(f"[s01] DONE in {dt:.1f}s; {n_files} parquet files, {total:.1f} MB")


if __name__ == "__main__":
    main()
