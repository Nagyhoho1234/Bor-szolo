"""Step 15, Discussion spotlight uncertainty table.

For the four spotlight districts, pick the model's top-4 replacement
candidates at 2081-2100 RCP8.5 (varieties not currently among the district's
principal cultivars, ranked by ensemble mean suitability) and report
ensemble mean, p10, p50, p90, and std across the 14 EURO-CORDEX members.

Outputs:
- ``analysis/curated/ensemble/discussion_spotlight_uncertainty.md``
- ``analysis/curated/ensemble/discussion_spotlight_uncertainty.csv``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
ENS_DIR = ANALYSIS / "curated" / "ensemble"

SPOTLIGHT = {"Soproni": "Sopron", "Tokaji": "Tokaj",
             "Villányi": "Villány", "Csongrádi": "Csongrád"}


def load_principals() -> dict[str, set[str]]:
    """Read principal-variety sets per district from the canonical YAML."""
    import yaml
    y = yaml.safe_load(
        (ANALYSIS / "config" / "districts.yml").read_text(encoding="utf-8")
    )
    # The YAML is keyed by the Hungarian borvidek name; we use that key directly.
    return {k: set(v.get("principal_varieties") or []) for k, v in y.items()}


PRINCIPAL = load_principals()


def load_members() -> list[str]:
    manifest = json.loads((ENS_DIR / "ensemble_manifest.json").read_text(encoding="utf-8"))
    return [m["member"] for m in manifest["members_processed"]]


def per_member_long(period: str, scen: str, members: list[str]) -> pd.DataFrame:
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
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def to_md(df: pd.DataFrame, float_cols: dict[str, str]) -> str:
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    lines = [header, sep]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            fmt = float_cols.get(c)
            if fmt and pd.notna(v) and not isinstance(v, str):
                cells.append(format(float(v), fmt))
            else:
                cells.append("" if pd.isna(v) else str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    members = load_members()
    period, scen = "2081-2100", "rcp85"
    long = per_member_long(period, scen, members)
    if long.empty:
        print("[s15] no per-member data for 2081-2100 rcp85")
        return

    rows = []
    for bv_hu, bv_en in SPOTLIGHT.items():
        sub = long[long["borvidek"] == bv_hu]
        if sub.empty:
            print(f"[s15] WARN: no data for {bv_hu}")
            continue
        # exclude principals; rank remaining by ensemble mean
        principals = set(PRINCIPAL.get(bv_hu, []))
        agg = (sub.groupby("variety")["suitability"]
                  .agg(["mean", lambda x: x.quantile(0.10),
                                 lambda x: x.quantile(0.50),
                                 lambda x: x.quantile(0.90),
                                 lambda x: x.std(ddof=1)])
                  .rename(columns={"<lambda_0>": "p10", "<lambda_1>": "p50",
                                   "<lambda_2>": "p90", "<lambda_3>": "std"})
                  .reset_index())
        agg = agg[~agg["variety"].isin(principals)]
        top4 = agg.sort_values("mean", ascending=False).head(4).reset_index(drop=True)
        for rank, r in top4.iterrows():
            rows.append({
                "District": bv_en,
                "Rank": int(rank) + 1,
                "Replacement candidate": r["variety"],
                "Ensemble mean": r["mean"],
                "p10": r["p10"],
                "p50": r["p50"],
                "p90": r["p90"],
                "Std": r["std"],
            })

    out_df = pd.DataFrame(rows)
    import os as _os
    variant = _os.environ.get("HUGLIN_VARIANT", "").upper()
    suffix = f"_{variant}" if variant else ""
    csv_path = ENS_DIR / f"discussion_spotlight_uncertainty{suffix}.csv"
    md_path = ENS_DIR / f"discussion_spotlight_uncertainty{suffix}.md"
    out_df.to_csv(csv_path, index=False)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("### Discussion spotlight uncertainty table, 2081-2100 RCP8.5\n\n")
        f.write("Top-4 replacement candidates per spotlight district "
                "(varieties not currently among the district's principal cultivars), "
                "with ensemble statistics across the 14 EURO-CORDEX members of the "
                "FORESEE-HUN archive.\n\n")
        f.write(to_md(out_df, float_cols={
            "Ensemble mean": ".3f", "p10": ".3f", "p50": ".3f",
            "p90": ".3f", "Std": ".3f",
        }))
        f.write("\n")
    print(f"[s15] wrote {csv_path.name} and {md_path.name} ({len(out_df)} rows)")


if __name__ == "__main__":
    main()
