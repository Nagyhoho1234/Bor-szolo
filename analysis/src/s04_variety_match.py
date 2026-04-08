"""Step 4 — variety x district climate suitability across periods and scenarios."""
from __future__ import annotations

import io
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")

CONFIG_DIR = ANALYSIS / "config"
NORMALS_DIR = ANALYSIS / "curated" / "normals"
OUT_DIR = ANALYSIS / "curated" / "variety_match"
FIG_DIR = ANALYSIS / "reports" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# (period_label, scenario_label_out, normals_filename)
PERIOD_SCENARIOS = [
    ("1971-2000", "observed", "normals_1971-2000_per_district.parquet"),
    ("1991-2020", "observed", "normals_1991-2020_per_district.parquet"),
    # 20-year future bins
    ("2021-2040", "rcp45", "normals_2021-2040_rcp45_per_district.parquet"),
    ("2041-2060", "rcp45", "normals_2041-2060_rcp45_per_district.parquet"),
    ("2061-2080", "rcp45", "normals_2061-2080_rcp45_per_district.parquet"),
    ("2081-2100", "rcp45", "normals_2081-2100_rcp45_per_district.parquet"),
    ("2021-2040", "rcp85", "normals_2021-2040_rcp85_per_district.parquet"),
    ("2041-2060", "rcp85", "normals_2041-2060_rcp85_per_district.parquet"),
    ("2061-2080", "rcp85", "normals_2061-2080_rcp85_per_district.parquet"),
    ("2081-2100", "rcp85", "normals_2081-2100_rcp85_per_district.parquet"),
]

BASELINE_PERIOD = "1991-2020"
BASELINE_SCENARIO = "observed"

INDEX_HUGLIN = "huglin_index"
INDEX_WINKLER = "winkler_gdd"
INDEX_FROST = "spring_frost_days"
INDEX_HEAT = "heat_days_t35"


# ------------------------------------------------------------
# name normalisation helpers
# ------------------------------------------------------------

def _norm(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower().replace("-", "").replace(" ", "")


# ------------------------------------------------------------
# winkler class
# ------------------------------------------------------------

def winkler_class_of(gdd: float) -> int | float:
    if not np.isfinite(gdd):
        return np.nan
    if gdd < 1389:
        return 1
    if gdd < 1667:
        return 2
    if gdd < 1944:
        return 3
    if gdd < 2222:
        return 4
    return 5


# ------------------------------------------------------------
# sub-scores
# ------------------------------------------------------------

def huglin_trapezoid(hi: float, env: pd.Series) -> float:
    if not np.isfinite(hi):
        return np.nan
    hmin, olo, ohi, hmax = env["huglin_min"], env["huglin_opt_low"], env["huglin_opt_high"], env["huglin_max"]
    if hi < hmin or hi > hmax:
        return 0.0
    if hi < olo:
        return float((hi - hmin) / max(olo - hmin, 1e-9))
    if hi <= ohi:
        return 1.0
    return float((hmax - hi) / max(hmax - ohi, 1e-9))


def winkler_ok_fn(gdd: float, env: pd.Series) -> bool:
    wc = winkler_class_of(gdd)
    if not np.isfinite(wc):
        return False
    return bool(env["winkler_class_min"] <= wc <= env["winkler_class_max"])


def penalty_score(days: float, tolerance: float) -> float:
    if not np.isfinite(days):
        return np.nan
    tol = max(tolerance, 1.0)
    return float(1.0 - min(1.0, max(0.0, (days - tolerance) / tol)))


# ------------------------------------------------------------
# main
# ------------------------------------------------------------

def load_envelopes() -> pd.DataFrame:
    df = pd.read_csv(CONFIG_DIR / "grape_envelopes.csv", encoding="utf-8")
    df["_key"] = df["variety"].map(_norm)
    return df


def load_districts() -> dict:
    with open(CONFIG_DIR / "districts.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_district_lookup(normals_borvideks: list[str], districts_cfg: dict) -> dict:
    """Map districts.yml key -> canonical borvidek string (from normals)."""
    canonical = {_norm(b): b for b in normals_borvideks}
    out = {}
    for key, entry in districts_cfg.items():
        name_hu = entry.get("name_hu", key)
        cand = _norm(name_hu)
        if cand in canonical:
            out[key] = canonical[cand]
        else:
            # try stripping hyphens
            alt = _norm(name_hu.replace("-", ""))
            if alt in canonical:
                out[key] = canonical[alt]
            else:
                warnings.warn(f"District '{name_hu}' not found in normals; skipping")
                out[key] = None
    return out


def pivot_normals(df: pd.DataFrame) -> pd.DataFrame:
    """Return borvidek -> {huglin, winkler, frost, heat} means."""
    wanted = {INDEX_HUGLIN, INDEX_WINKLER, INDEX_FROST, INDEX_HEAT}
    sub = df[df["index"].isin(wanted)][["borvidek", "borregio", "index", "mean"]]
    wide = sub.pivot_table(index=["borvidek", "borregio"], columns="index", values="mean").reset_index()
    wide = wide.rename(columns={
        INDEX_HUGLIN: "huglin_mean",
        INDEX_WINKLER: "winkler_mean",
        INDEX_FROST: "frost_days_mean",
        INDEX_HEAT: "heat_days_mean",
    })
    for c in ["huglin_mean", "winkler_mean", "frost_days_mean", "heat_days_mean"]:
        if c not in wide.columns:
            wide[c] = np.nan
    return wide


def compute_period(norm_df: pd.DataFrame, envelopes: pd.DataFrame,
                   period: str, scenario: str,
                   principal_by_district_canonical: dict[str, set[str]]) -> pd.DataFrame:
    wide = pivot_normals(norm_df)
    rows = []
    env_keys = set(envelopes["_key"])
    for _, drow in wide.iterrows():
        bv = drow["borvidek"]
        bv_key = _norm(bv)
        principal_set = principal_by_district_canonical.get(bv_key, set())
        # union: score every variety in every district
        for _, env in envelopes.iterrows():
            variety = env["variety"]
            vkey = env["_key"]
            hi = drow["huglin_mean"]
            gdd = drow["winkler_mean"]
            frost = drow["frost_days_mean"]
            heat = drow["heat_days_mean"]
            h_score = huglin_trapezoid(hi, env)
            w_ok = winkler_ok_fn(gdd, env)
            f_score = penalty_score(frost, env["frost_tolerance_days"])
            ht_score = penalty_score(heat, env["heat_tolerance_days"])
            # Soft Winkler penalty: instead of 0/1, decay smoothly when GDD
            # falls outside the variety's class range. Softened from gap/3.0
            # to gap/4.0 so a single class beyond costs 25% (not 33%) and
            # 4 classes off reaches 0. This better reflects that varieties
            # *can* grow beyond their classical optimum class with quality
            # changes rather than failing outright.
            wc = winkler_class_of(gdd)
            if isinstance(wc, float) and not np.isfinite(wc):
                w_score = 0.5  # missing data
            elif env["winkler_class_min"] <= wc <= env["winkler_class_max"]:
                w_score = 1.0
            else:
                gap = max(env["winkler_class_min"] - wc, wc - env["winkler_class_max"])
                w_score = max(0.0, 1.0 - gap / 4.0)
            # suitability
            if any(not np.isfinite(x) for x in [h_score, f_score, ht_score]):
                suit = np.nan
            else:
                suit = h_score * w_score * f_score * ht_score
            # limiting factor
            sub_scores = {
                "huglin": h_score if np.isfinite(h_score) else 1.0,
                "winkler": 1.0 if w_ok else 0.0,
                "frost": f_score if np.isfinite(f_score) else 1.0,
                "heat": ht_score if np.isfinite(ht_score) else 1.0,
            }
            limiting = min(sub_scores, key=lambda k: sub_scores[k])
            rows.append({
                "borvidek": bv,
                "borregio": drow["borregio"],
                "variety": variety,
                "variety_en": env["variety_en"],
                "period": period,
                "scenario": scenario,
                "huglin_mean": np.float32(hi),
                "winkler_mean": np.float32(gdd),
                "frost_days_mean": np.float32(frost),
                "heat_days_mean": np.float32(heat),
                "huglin_score": np.float32(h_score),
                "winkler_ok": bool(w_ok),
                "frost_score": np.float32(f_score),
                "heat_score": np.float32(ht_score),
                "suitability": np.float32(suit),
                "limiting_factor": limiting,
                "colour": env["colour"],
                "confidence": env["confidence"],
                "in_principal_varieties": vkey in principal_set,
            })
    return pd.DataFrame(rows)


def main() -> None:
    envelopes = load_envelopes()
    districts_cfg = load_districts()

    # load one normals file to get canonical borvidek list
    probe = pd.read_parquet(NORMALS_DIR / PERIOD_SCENARIOS[0][2])
    canonical_borvideks = sorted(probe["borvidek"].unique().tolist())

    # map districts.yml entries to canonical borvidek strings
    dmap = build_district_lookup(canonical_borvideks, districts_cfg)

    # principal variety sets keyed by normalised canonical borvidek
    principal_by_district_canonical: dict[str, set[str]] = {}
    missing_env_report: list[tuple[str, str]] = []
    env_keys = set(envelopes["_key"])
    for key, entry in districts_cfg.items():
        canon = dmap.get(key)
        if canon is None:
            continue
        pv = entry.get("principal_varieties", [])
        keys = set()
        for v in pv:
            vk = _norm(v)
            if vk not in env_keys:
                missing_env_report.append((canon, v))
            keys.add(vk)
        principal_by_district_canonical[_norm(canon)] = keys

    if missing_env_report:
        print("WARNING: principal varieties with no envelope match:")
        seen = set()
        for district, var in missing_env_report:
            tag = (district, var)
            if tag in seen:
                continue
            seen.add(tag)
            print(f"  - {district}: {var}")
    else:
        print("All principal varieties have envelope matches.")

    # compute each period/scenario
    all_frames = []
    per_file_counts = {}
    for period, scenario, fname in PERIOD_SCENARIOS:
        norm_df = pd.read_parquet(NORMALS_DIR / fname)
        df = compute_period(norm_df, envelopes, period, scenario, principal_by_district_canonical)
        out_name = f"district_variety_suitability_{period}_{scenario}.parquet"
        # delta filled later after baseline is known
        all_frames.append(df)
        per_file_counts[(period, scenario)] = len(df)
        print(f"  computed {period} {scenario}: {len(df)} (district, variety) rows")

    long_df = pd.concat(all_frames, ignore_index=True)

    # baseline lookup: (borvidek, variety) -> suitability
    base = long_df[(long_df["period"] == BASELINE_PERIOD) & (long_df["scenario"] == BASELINE_SCENARIO)]
    base_map = base.set_index(["borvidek", "variety"])["suitability"].to_dict()

    def delta(row):
        if row["period"] == BASELINE_PERIOD and row["scenario"] == BASELINE_SCENARIO:
            return np.float32(np.nan)
        b = base_map.get((row["borvidek"], row["variety"]), np.nan)
        if not np.isfinite(b) or not np.isfinite(row["suitability"]):
            return np.float32(np.nan)
        return np.float32(row["suitability"] - b)

    long_df["delta_vs_1991_2020"] = long_df.apply(delta, axis=1).astype("float32")

    # write per-(period, scenario) files
    for (period, scenario), _count in per_file_counts.items():
        sub = long_df[(long_df["period"] == period) & (long_df["scenario"] == scenario)].copy()
        out_path = OUT_DIR / f"district_variety_suitability_{period}_{scenario}.parquet"
        sub.to_parquet(out_path, index=False)
        print(f"  wrote {out_path.name}  rows={len(sub)}")

    long_path = OUT_DIR / "suitability_long.parquet"
    long_df.to_parquet(long_path, index=False)
    print(f"  wrote {long_path.name}  rows={len(long_df)}")

    # verification: top/bottom under 2071-2100 rcp85
    fut = long_df[(long_df["period"] == "2081-2100") & (long_df["scenario"] == "rcp85")].copy()
    fut_valid = fut.dropna(subset=["delta_vs_1991_2020"])
    print("\nTop 3 winners (2071-2100 rcp85, all varieties):")
    for _, r in fut_valid.nlargest(3, "delta_vs_1991_2020").iterrows():
        print(f"  {r['borvidek']:20s} {r['variety']:22s} delta={r['delta_vs_1991_2020']:+.3f}")
    print("Bottom 3 losers (2071-2100 rcp85, all varieties):")
    for _, r in fut_valid.nsmallest(3, "delta_vs_1991_2020").iterrows():
        print(f"  {r['borvidek']:20s} {r['variety']:22s} delta={r['delta_vs_1991_2020']:+.3f}")

    # headline winners/losers restricted to principal varieties
    fut_principal = fut[fut["in_principal_varieties"]].dropna(subset=["delta_vs_1991_2020"])
    headline_rows = []
    for bv, g in fut_principal.groupby("borvidek"):
        if g.empty:
            continue
        w = g.loc[g["delta_vs_1991_2020"].idxmax()]
        l = g.loc[g["delta_vs_1991_2020"].idxmin()]
        base_loser = base_map.get((bv, l["variety"]), np.nan)
        headline_rows.append({
            "borvidek": bv,
            "biggest_winner_variety": w["variety"],
            "winner_delta": float(w["delta_vs_1991_2020"]),
            "biggest_loser_variety": l["variety"],
            "loser_delta": float(l["delta_vs_1991_2020"]),
            "current_suitability_loser": float(base_loser) if np.isfinite(base_loser) else np.nan,
            "future_suitability_loser": float(l["suitability"]) if np.isfinite(l["suitability"]) else np.nan,
        })
    headline = pd.DataFrame(headline_rows).sort_values("borvidek")
    headline_path = OUT_DIR / "headline_winners_losers.csv"
    headline.to_csv(headline_path, index=False, encoding="utf-8")
    print(f"\n  wrote {headline_path.name}  rows={len(headline)}")

    # report headline for Tokaji/Egri/Villányi
    print("\nHeadline winners/losers for Tokaji, Egri, Villányi:")
    for target in ["Tokaji", "Egri", "Villányi"]:
        row = headline[headline["borvidek"] == target]
        if row.empty:
            print(f"  {target}: NOT FOUND")
        else:
            r = row.iloc[0]
            print(f"  {target}: winner={r['biggest_winner_variety']} ({r['winner_delta']:+.3f})  "
                  f"loser={r['biggest_loser_variety']} ({r['loser_delta']:+.3f}) "
                  f"cur={r['current_suitability_loser']:.3f} fut={r['future_suitability_loser']:.3f}")

    # quick heatmap figure (principal varieties only)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fut_pv = fut[fut["in_principal_varieties"]]
        if not fut_pv.empty:
            pv = fut_pv.pivot_table(index="variety", columns="borvidek", values="suitability", aggfunc="mean")
            fig, ax = plt.subplots(figsize=(max(8, 0.45 * pv.shape[1] + 4),
                                             max(6, 0.35 * pv.shape[0] + 2)))
            im = ax.imshow(pv.values, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
            ax.set_xticks(range(pv.shape[1]))
            ax.set_xticklabels(pv.columns, rotation=70, ha="right", fontsize=8)
            ax.set_yticks(range(pv.shape[0]))
            ax.set_yticklabels(pv.index, fontsize=8)
            ax.set_title("Suitability — 2071-2100 RCP8.5 (principal varieties only)")
            fig.colorbar(im, ax=ax, label="suitability [0,1]")
            fig.tight_layout()
            fig_path = FIG_DIR / "suitability_heatmap_2071-2100_rcp85.png"
            fig.savefig(fig_path, dpi=150)
            plt.close(fig)
            print(f"  wrote figure {fig_path}")
    except Exception as e:
        print(f"  figure skipped: {e}")

    # anomaly checks
    nan_rows = long_df["suitability"].isna().sum()
    print(f"\nNaN suitability rows: {nan_rows} / {len(long_df)}")
    # per period
    for (p, s), g in long_df.groupby(["period", "scenario"]):
        nn = g["suitability"].isna().sum()
        print(f"  {p} {s}: nan={nn} rows={len(g)} mean={g['suitability'].mean():.3f}")


if __name__ == "__main__":
    main()
