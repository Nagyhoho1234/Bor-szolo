"""Viticulture climate indices on daily DataFrames.

Each function takes one or more wide DataFrames (index=date, columns=districts)
and returns an annual wide DataFrame (index=year, columns=districts) with the
specified units. Latitudes for Huglin / Hargreaves are passed as a Series
indexed by district name.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# ---------- helpers ----------

def _annual_window_sum(df: pd.DataFrame, start_md: tuple[int, int], end_md: tuple[int, int]) -> pd.DataFrame:
    """Sum daily values for each year over [start_md, end_md] inclusive."""
    md = list(zip(df.index.month, df.index.day))
    sm, sd = start_md
    em, ed = end_md
    in_window = np.array([(m, d) >= (sm, sd) and (m, d) <= (em, ed) for m, d in md])
    sub = df.loc[in_window]
    return sub.groupby(sub.index.year).sum(min_count=1)


def _annual_window_count(df: pd.DataFrame, mask_fn, start_md, end_md) -> pd.DataFrame:
    md = list(zip(df.index.month, df.index.day))
    sm, sd = start_md
    em, ed = end_md
    in_window = np.array([(m, d) >= (sm, sd) and (m, d) <= (em, ed) for m, d in md])
    sub = df.loc[in_window]
    return mask_fn(sub).astype(np.int16).groupby(sub.index.year).sum(min_count=1)


# ---------- 1. Winkler GDD ----------

def winkler_gdd(tmax: pd.DataFrame, tmin: pd.DataFrame) -> pd.DataFrame:
    tmean = (tmax + tmin) / 2.0
    gdd = (tmean - 10.0).clip(lower=0.0)
    return _annual_window_sum(gdd, (4, 1), (10, 31))


WINKLER_BREAKS = [(0, 1389, "Ia"), (1389, 1667, "Ib"),
                  (1667, 1944, "II"), (1944, 2222, "III"),
                  (2222, 2500, "IV"), (2500, 1e9, "V")]


def winkler_class(value: float) -> str:
    if pd.isna(value):
        return None
    for lo, hi, lbl in WINKLER_BREAKS:
        if lo <= value < hi:
            return lbl
    return None


# ---------- 2. Huglin index ----------

def huglin_K(lat: float) -> float:
    """Latitude correction (linear interp between paper anchors)."""
    anchors = np.array([
        (40.0, 1.02),
        (42.0, 1.02),
        (44.0, 1.03),
        (46.0, 1.04),
        (48.0, 1.05),
        (50.0, 1.06),
    ])
    if lat <= 40.0:
        return 1.02
    if lat >= 50.0:
        return 1.06
    return float(np.interp(lat, anchors[:, 0], anchors[:, 1]))


def huglin_index(tmax: pd.DataFrame, tmin: pd.DataFrame, lats: pd.Series) -> pd.DataFrame:
    tmean = (tmax + tmin) / 2.0
    daily = ((tmean - 10.0) + (tmax - 10.0)) / 2.0
    daily = daily.clip(lower=0.0)
    annual = _annual_window_sum(daily, (4, 1), (9, 30))
    K = pd.Series({c: huglin_K(lats[c]) for c in annual.columns})
    return annual.mul(K, axis=1)


HUGLIN_BREAKS = [
    (-1e9, 1500, "Very cool"),
    (1500, 1800, "Cool"),
    (1800, 2100, "Temperate"),
    (2100, 2400, "Temperate-warm"),
    (2400, 2700, "Warm"),
    (2700, 3000, "Warm-temperate"),
    (3000, 1e9, "Very warm"),
]


def huglin_class(value: float) -> str:
    if pd.isna(value):
        return None
    for lo, hi, lbl in HUGLIN_BREAKS:
        if lo <= value < hi:
            return lbl
    return None


# ---------- 3-6. Frost & heat ----------

def late_spring_frost_days(tmin: pd.DataFrame) -> pd.DataFrame:
    return _annual_window_count(tmin, lambda d: d < 0, (3, 1), (5, 31))


def last_spring_frost_doy(tmin: pd.DataFrame) -> pd.DataFrame:
    md = list(zip(tmin.index.month, tmin.index.day))
    in_window = np.array([(m, d) <= (6, 15) for m, d in md])
    sub = tmin.loc[in_window]
    doy = sub.index.dayofyear
    out = {}
    for year, idx in sub.groupby(sub.index.year).groups.items():
        block = sub.loc[idx]
        block_doy = block.index.dayofyear
        cols = {}
        for c in block.columns:
            mask = block[c].values < 0
            cols[c] = float(block_doy[mask].max()) if mask.any() else np.nan
        out[year] = cols
    df = pd.DataFrame.from_dict(out, orient="index")
    df.index.name = None
    return df.sort_index()


def heat_days(tmax: pd.DataFrame, threshold: float = 35.0) -> pd.DataFrame:
    return _annual_window_count(tmax, lambda d: d > threshold, (6, 1), (8, 31))


# ---------- 7. Growing-season precip ----------

def growing_season_precip(pr: pd.DataFrame) -> pd.DataFrame:
    return _annual_window_sum(pr, (4, 1), (10, 31))


# ---------- 8. Hargreaves PET ----------

def _Ra_mm_per_day(lat_deg: float, doy: np.ndarray) -> np.ndarray:
    """FAO-56 eq. 21: extraterrestrial radiation (mm/day water equivalent)."""
    Gsc = 0.0820  # MJ m-2 min-1
    phi = np.deg2rad(lat_deg)
    dr = 1.0 + 0.033 * np.cos(2.0 * np.pi * doy / 365.0)
    delta = 0.409 * np.sin(2.0 * np.pi * doy / 365.0 - 1.39)
    arg = -np.tan(phi) * np.tan(delta)
    arg = np.clip(arg, -1.0, 1.0)
    omega_s = np.arccos(arg)
    Ra_MJ = (24.0 * 60.0 / np.pi) * Gsc * dr * (
        omega_s * np.sin(phi) * np.sin(delta)
        + np.cos(phi) * np.cos(delta) * np.sin(omega_s)
    )
    # Convert MJ/m2/day -> mm/day water equivalent (divide by 2.45)
    return Ra_MJ / 2.45


def hargreaves_pet_annual(tmax: pd.DataFrame, tmin: pd.DataFrame, lats: pd.Series) -> pd.DataFrame:
    tmean = (tmax + tmin) / 2.0
    diff = (tmax - tmin).clip(lower=0.0)
    sqrt_diff = np.sqrt(diff)
    doy = np.array(tmax.index.dayofyear)
    pet = pd.DataFrame(index=tmax.index, columns=tmax.columns, dtype=np.float32)
    for c in tmax.columns:
        Ra = _Ra_mm_per_day(float(lats[c]), doy)
        pet[c] = 0.0023 * (tmean[c].values + 17.8) * sqrt_diff[c].values * Ra
    return _annual_window_sum(pet, (4, 1), (10, 31))


# ---------- 9. P - PET ----------

def p_minus_pet(pr_annual: pd.DataFrame, pet_annual: pd.DataFrame) -> pd.DataFrame:
    return pr_annual - pet_annual


# ---------- 10. Cool Night Index ----------

def cool_night_index(tmin: pd.DataFrame) -> pd.DataFrame:
    sub = tmin.loc[tmin.index.month == 9]
    return sub.groupby(sub.index.year).mean()
