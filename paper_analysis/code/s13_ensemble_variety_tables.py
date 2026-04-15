"""Step 13, per-variety ensemble uncertainty tables.

For each (period, scenario) combination, aggregate the 14-member ensemble
suitability to one row per variety with mean, p10, p50, p90, and std across
members and across districts. Write:

- ``analysis/curated/ensemble/variety_uncertainty_<period>_<scenario>.md``
  (markdown table, one per combination)
- ``analysis/curated/ensemble/variety_uncertainty_<period>_<scenario>.csv``
  (same content, machine-readable)
- ``analysis/curated/ensemble/variety_uncertainty_all.csv``
  (concatenated long-form, ready for Zenodo archive)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
ENS_DIR = ANALYSIS / "curated" / "ensemble"
PER_MEMBER_ROOT = ENS_DIR  # <member>/variety_match/district_variety_suitability_<period>_<scen>.parquet

PERIOD_SCENARIOS = [
    ("1971-2000", "observed"),
    ("1991-2020", "observed"),
    ("2021-2040", "rcp45"), ("2041-2060", "rcp45"),
    ("2061-2080", "rcp45"), ("2081-2100", "rcp45"),
    ("2021-2040", "rcp85"), ("2041-2060", "rcp85"),
    ("2061-2080", "rcp85"), ("2081-2100", "rcp85"),
]


def load_members() -> list[str]:
    import json
    manifest = json.loads((ENS_DIR / "ensemble_manifest.json").read_text(encoding="utf-8"))
    return [m["member"] for m in manifest["members_processed"]]


def per_member_long(period: str, scen: str, members: list[str]) -> pd.DataFrame:
    """Stack per-member, per-district, per-variety suitability into a long df."""
    import os as _os
    variant = _os.environ.get("HUGLIN_VARIANT", "").upper()
    sub_path = f"variety_match/{variant}" if variant else "variety_match"
    rows = []
    for m in members:
        p = (ENS_DIR / m / sub_path
             / f"district_variety_suitability_{period}_{scen}.parquet")
        if not p.exists():
            continue
        df = pd.read_parquet(p)
        score = next(c for c in ("suitability", "score", "suitability_score")
                     if c in df.columns)
        member_df = df[["borvidek", "variety", score]].rename(columns={score: "suitability"})
        member_df["member"] = m
        rows.append(member_df)
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def table_to_md(df: pd.DataFrame, float_cols: dict[str, str]) -> str:
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    rows = []
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            fmt = float_cols.get(c)
            if fmt and pd.notna(v) and not isinstance(v, str):
                cells.append(format(float(v), fmt))
            else:
                cells.append("" if pd.isna(v) else str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def main():
    t0 = time.time()
    members = load_members()
    print(f"[s13] {len(members)} members in manifest")

    master: list[pd.DataFrame] = []

    for period, scen in PERIOD_SCENARIOS:
        big = per_member_long(period, scen, members)
        if big.empty:
            print(f"[s13] SKIP {period} {scen}: no per-member parquet")
            continue

        # Aggregate over (member, district) per variety to get the ensemble
        # distribution across the full Hungarian surface.
        g = big.groupby("variety")["suitability"]
        table = pd.DataFrame({
            "variety": list(g.groups.keys()),
            "mean": g.mean().values,
            "p10":  g.quantile(0.10).values,
            "p50":  g.quantile(0.50).values,
            "p90":  g.quantile(0.90).values,
            "std":  g.std(ddof=1).values,
        }).sort_values("mean", ascending=False).reset_index(drop=True)

        table["period"] = period
        table["scenario"] = scen
        master.append(table)

        csv_path = ENS_DIR / f"variety_uncertainty_{period}_{scen}.csv"
        md_path = ENS_DIR / f"variety_uncertainty_{period}_{scen}.md"
        table[["variety", "mean", "p10", "p50", "p90", "std"]].to_csv(csv_path, index=False)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"### Table T-{period}-{scen}. Per-variety ensemble suitability "
                    f"({period}, {scen.upper()})\n\n")
            f.write("57 varieties, each row is an ensemble aggregate over the 14 "
                    "EURO-CORDEX RCM members × 22 wine districts "
                    f"(n = {len(members)*22} samples per variety).\n\n")
            f.write(table_to_md(
                table[["variety", "mean", "p10", "p50", "p90", "std"]],
                float_cols={"mean": ".3f", "p10": ".3f", "p50": ".3f",
                            "p90": ".3f", "std": ".3f"},
            ))
            f.write("\n")
        print(f"[s13] {csv_path.name}: {len(table)} varieties")

    if master:
        all_df = pd.concat(master, ignore_index=True)
        all_csv = ENS_DIR / "variety_uncertainty_all.csv"
        all_df[["period", "scenario", "variety", "mean", "p10", "p50", "p90", "std"]] \
            .to_csv(all_csv, index=False)
        print(f"[s13] master CSV -> {all_csv} ({len(all_df)} rows)")

    print(f"[s13] DONE in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
