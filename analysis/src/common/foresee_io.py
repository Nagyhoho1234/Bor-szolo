"""Reusable I/O for FORESEE NetCDF files.

Wraps the conventions used by CNRM-ALADIN53 FORESEE-HUN files:
- 365-day no-leap calendar (manual decoding)
- regular 0.1 deg lat/lon grid stored as 2-D arrays
- variable name differs between observed (tmax/tmin) and rcp (tasmax/tasmin)
"""
from __future__ import annotations

import os
import re
import glob
import numpy as np
import pandas as pd
import xarray as xr

FORESEE_DIR = r"e:/FORESEE_App/foresee"

# Map a logical variable to candidate names found in NetCDFs
VAR_ALIASES = {
    "pr":        ["pr", "precip", "precipitation"],
    "tmax":      ["tmax", "tasmax", "tx"],
    "tmin":      ["tmin", "tasmin", "tn"],
    "tdmean":    ["daylight_mean_temp", "tdmean", "tmean"],
    "vpd":       ["vpd"],
    "radiation": ["radiation", "rad", "global_radiation"],
    "dlen":      ["length_of_the_day", "dlen"],
}


def decode_time_manual(start_year: int, n_days: int) -> pd.DatetimeIndex:
    """Decode a 365-day no-leap time axis as a pandas DatetimeIndex.

    Each calendar year has exactly 365 days (Feb has 28). The output index
    therefore has gaps on Feb 29 in real leap years, which is fine for our
    daily time-series usage.
    """
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates = []
    year, month, day = start_year, 1, 1
    for _ in range(n_days):
        dates.append(f"{year:04d}-{month:02d}-{day:02d}")
        day += 1
        if day > days_in_month[month - 1]:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
    return pd.to_datetime(dates)


def detect_scenario(path: str) -> str:
    p = path.lower()
    if "rcp45" in p:
        return "rcp45"
    if "rcp85" in p:
        return "rcp85"
    if "observed" in p:
        return "observed"
    return "unknown"


def detect_logical_var(path: str) -> str:
    p = os.path.basename(path).lower()
    # Order matters: check 'pr' last to avoid matching "rcp"
    if "tasmax" in p or "_tmax" in p:
        return "tmax"
    if "tasmin" in p or "_tmin" in p:
        return "tmin"
    if "tdmean" in p:
        return "tdmean"
    if "vpd" in p:
        return "vpd"
    if "radiation" in p:
        return "radiation"
    if "dlen" in p:
        return "dlen"
    if p.endswith("_pr.nc") or "_pr_" in p:
        return "pr"
    return "unknown"


def detect_start_year(path: str) -> int:
    m = re.search(r"(\d{4})-\d{4}", os.path.basename(path))
    return int(m.group(1)) if m else 1971


def open_foresee(path: str) -> xr.Dataset:
    """Open a FORESEE NetCDF with raw (undecoded) time."""
    try:
        return xr.open_dataset(path, decode_times=False, engine="scipy")
    except Exception:
        return xr.open_dataset(path, decode_times=False)


def get_data_var(ds: xr.Dataset, logical: str) -> str:
    """Find the actual variable name in the dataset for a logical name."""
    candidates = VAR_ALIASES.get(logical, [logical])
    lower_map = {v.lower(): v for v in ds.data_vars}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    # Fallback: first var with a time-like dim
    for v in ds.data_vars:
        if any(d in ds[v].dims for d in ("time", "zdim")):
            return v
    raise ValueError(f"No variable for {logical} in {list(ds.data_vars)}")


def get_lat_lon(ds: xr.Dataset) -> tuple[np.ndarray, np.ndarray]:
    """Return 2-D lat and lon arrays (broadcast if originally 1-D)."""
    lat = ds["lat"].values
    lon = ds["lon"].values
    if lat.ndim == 1 and lon.ndim == 1:
        lon, lat = np.meshgrid(lon, lat)
    return lat, lon


def get_lat_lon_1d(ds: xr.Dataset) -> tuple[np.ndarray, np.ndarray]:
    """Return 1-D unique lat and lon vectors (assumes regular grid)."""
    lat2, lon2 = get_lat_lon(ds)
    lats_1d = lat2[:, 0] if lat2.ndim == 2 else lat2
    lons_1d = lon2[0, :] if lon2.ndim == 2 else lon2
    return lats_1d, lons_1d


def list_foresee_files() -> list[str]:
    return sorted(glob.glob(os.path.join(FORESEE_DIR, "*.nc")))


def read_daily_cube(path: str) -> tuple[np.ndarray, pd.DatetimeIndex, str]:
    """Open a FORESEE NetCDF and return (data[T,Y,X], dates, var_name)."""
    ds = open_foresee(path)
    logical = detect_logical_var(path)
    var = get_data_var(ds, logical)
    arr = ds[var].values  # (T, Y, X)
    if arr.ndim != 3:
        raise ValueError(f"Unexpected shape {arr.shape} for {path}")
    n = arr.shape[0]
    dates = decode_time_manual(detect_start_year(path), n)
    ds.close()
    return arr.astype(np.float32), dates, logical
