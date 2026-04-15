"""Step 11, aggregate per-member outputs into ensemble statistics.

Reads each member's curated outputs produced by s01b and computes, across
members, the ensemble mean, 10th/50th/90th percentiles, and standard
deviation for:

- period normals of every viticulture index (``curated/normals/``);
- district-variety suitability for every period-scenario combination
  (``curated/variety_match/``);
- per-district crossover year (first year under RCP8.5 where the national
  mean suitability drops below the 1991-2020 baseline).

Outputs land in ``analysis/curated/ensemble/``:

    ensemble_normals_<period>_<scenario>_per_district.parquet
    ensemble_suitability_<period>_<scenario>.parquet
    ensemble_crossover_year.parquet

The manifest written by s01b determines which members are included. Members
listed under ``members_missing`` are skipped.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
MANIFEST_PATH = ANALYSIS / "curated" / "ensemble" / "ensemble_manifest.json"
import os as _os
_VARIANT = _os.environ.get("HUGLIN_VARIANT", "").upper()
OUT_DIR = (ANALYSIS / "curated" / "ensemble_variants" / _VARIANT) if _VARIANT else (ANALYSIS / "curated" / "ensemble")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PERIOD_SCENARIOS = [
    ("1971-2000", "observed"),
    ("1991-2020", "observed"),
    ("2021-2040", "rcp45"), ("2041-2060", "rcp45"),
    ("2061-2080", "rcp45"), ("2081-2100", "rcp45"),
    ("2021-2040", "rcp85"), ("2041-2060", "rcp85"),
    ("2061-2080", "rcp85"), ("2081-2100", "rcp85"),
]


# ---------------------------------------------------------------------------
# Manifest + path resolution
# ---------------------------------------------------------------------------

def load_members() -> list[str]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"no manifest at {MANIFEST_PATH}; run s01b_ensemble_orchestrator first"
        )
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    return [m["member"] for m in manifest["members_processed"]]


def normals_path(member: str, period: str, scenario: str) -> Path:
    return (ANALYSIS / "curated" / "ensemble" / member / "normals"
            / f"normals_{period}{'_' + scenario if scenario != 'observed' else ''}"
              f"_per_district.parquet")


def suitability_path(member: str, period: str, scenario: str) -> Path:
    import os as _os
    variant = _os.environ.get("HUGLIN_VARIANT", "").upper()
    sub = f"variety_match/{variant}" if variant else "variety_match"
    return (ANALYSIS / "curated" / "ensemble" / member / sub
            / f"district_variety_suitability_{period}_{scenario}.parquet")


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def _percentile_stats(df: pd.DataFrame, group_cols: list[str],
                      value_col: str) -> pd.DataFrame:
    """Group, then compute n, mean, p10, p50, p90, std across members."""
    g = df.groupby(group_cols)[value_col]
    return (
        pd.DataFrame({
            "n_members": g.count(),
            "mean":      g.mean(),
            "p10":       g.quantile(0.10),
            "p50":       g.quantile(0.50),
            "p90":       g.quantile(0.90),
            "std":       g.std(ddof=1),
        })
        .reset_index()
    )


def aggregate_normals(members: list[str]) -> None:
    for period, scenario in PERIOD_SCENARIOS:
        rows = []
        for m in members:
            p = normals_path(m, period, scenario)
            if not p.exists():
                continue
            df = pd.read_parquet(p)
            df = df.assign(member=m)
            rows.append(df)
        if not rows:
            print(f"[s11] normals {period} {scenario}: no member output")
            continue
        big = pd.concat(rows, ignore_index=True)
        agg = _percentile_stats(big, ["borvidek", "index"], "mean")
        out = OUT_DIR / f"ensemble_normals_{period}_{scenario}_per_district.parquet"
        agg.to_parquet(out)
        print(f"[s11] {out.name}: {len(agg)} rows (n_members={big['member'].nunique()})")


def aggregate_suitability(members: list[str]) -> None:
    for period, scenario in PERIOD_SCENARIOS:
        rows = []
        for m in members:
            p = suitability_path(m, period, scenario)
            if not p.exists():
                continue
            df = pd.read_parquet(p)
            df = df.assign(member=m)
            rows.append(df)
        if not rows:
            print(f"[s11] suitability {period} {scenario}: no member output")
            continue
        big = pd.concat(rows, ignore_index=True)
        # normalise the score column name
        score_col = next(
            (c for c in ("suitability", "score", "suitability_score") if c in big.columns),
            None,
        )
        if score_col is None:
            print(f"[s11] WARN suitability {period} {scenario}: no score column")
            continue
        agg = _percentile_stats(big, ["borvidek", "variety"], score_col)
        out = OUT_DIR / f"ensemble_suitability_{period}_{scenario}.parquet"
        agg.to_parquet(out)
        print(f"[s11] {out.name}: {len(agg)} rows (n_members={big['member'].nunique()})")


def aggregate_crossover(members: list[str]) -> None:
    """National-mean suitability crossover year per member (RCP8.5).

    Crossover year is the first year where the 5-year running mean of
    national-mean suitability drops below the 1991-2020 baseline value.
    """
    # Rebuild a national-mean annual series from each member's
    # district-level suitability timeseries (one value per year).
    # Members store per-period suitability rather than per-year, so we use
    # the six period midpoints and linearly interpolate between them for a
    # fair per-member crossover definition.
    per_member = []
    for m in members:
        try:
            baseline_df = pd.read_parquet(suitability_path(m, "1991-2020", "observed"))
            baseline = baseline_df.groupby("variety").get_group  # not used; fallback
        except Exception:
            continue

        # build (period, national_mean_score) series
        pts = []
        mids = {"1971-2000": 1986, "1991-2020": 2006,
                "2021-2040": 2031, "2041-2060": 2051,
                "2061-2080": 2071, "2081-2100": 2091}
        for period, scenario in PERIOD_SCENARIOS:
            if scenario not in ("observed", "rcp85"):
                continue
            p = suitability_path(m, period, scenario)
            if not p.exists():
                continue
            df = pd.read_parquet(p)
            score_col = next(
                (c for c in ("suitability", "score", "suitability_score") if c in df.columns),
                None,
            )
            if score_col is None:
                continue
            # national mean = mean across (borvidek, variety)
            pts.append((mids[period], float(df[score_col].mean())))
        if len(pts) < 3:
            continue
        pts.sort()
        years = np.array([p[0] for p in pts])
        vals = np.array([p[1] for p in pts])
        base_val = vals[years == 2006]
        if base_val.size == 0:
            continue
        base = float(base_val[0])
        # find first midpoint where vals < base
        below = np.where((years > 2006) & (vals < base))[0]
        if below.size == 0:
            crossover = np.nan
        else:
            # linear interp between the last >=base point and the first below
            j = int(below[0])
            y_prev, v_prev = years[j - 1], vals[j - 1]
            y_cur, v_cur = years[j], vals[j]
            if v_cur == v_prev:
                crossover = float(y_cur)
            else:
                crossover = float(y_prev + (base - v_prev) * (y_cur - y_prev) / (v_cur - v_prev))
        per_member.append({"member": m, "crossover_year_rcp85": crossover})

    df = pd.DataFrame(per_member)
    out = OUT_DIR / "ensemble_crossover_year.parquet"
    df.to_parquet(out)
    print(f"[s11] {out.name}: {len(df)} members (mean={df['crossover_year_rcp85'].mean():.1f}, "
          f"p10={df['crossover_year_rcp85'].quantile(0.1):.1f}, "
          f"p90={df['crossover_year_rcp85'].quantile(0.9):.1f})")


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    members = load_members()
    print(f"[s11] aggregating {len(members)} members: {members}")
    aggregate_normals(members)
    aggregate_suitability(members)
    aggregate_crossover(members)
    print(f"[s11] DONE in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
