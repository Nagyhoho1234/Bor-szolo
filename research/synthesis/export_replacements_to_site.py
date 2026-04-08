"""
Export per-district variety replacement recommendations to the curated bundle.

Reads:
  research/synthesis/variety_replacements.csv

Writes:
  analysis/curated/variety_replacements/all.json    (single index)
  analysis/curated/variety_replacements/{slug}.json (one per district, 22 files)

These files are published to site/public/data/variety_replacements/ by
site/scripts/sync_curated.mjs (which wipes and recopies the curated bundle).

Each per-district file is keyed by horizon × scenario and contains the top
replacement candidates plus the at-risk principal varieties.
"""
from __future__ import annotations

import json
import sys
import io
import unicodedata
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"C:\Bor-szőlő")
CSV = ROOT / "research" / "synthesis" / "variety_replacements.csv"
PARQUET = ROOT / "analysis" / "curated" / "variety_match" / "suitability_long.parquet"
SITE_DIR = ROOT / "analysis" / "curated" / "variety_replacements"
SITE_DIR.mkdir(parents=True, exist_ok=True)


def slugify(s: str) -> str:
    """ASCII slug, lower-case, dashes for spaces, strip diacritics."""
    nfkd = unicodedata.normalize("NFKD", s)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    out = ""
    for c in ascii_str.lower():
        if c.isalnum():
            out += c
        elif out and out[-1] != "-":
            out += "-"
    return out.strip("-")


def main() -> int:
    df = pd.read_csv(CSV)
    suit = pd.read_parquet(PARQUET)

    print(f"Loaded {len(df)} replacement recommendations and "
          f"{len(suit)} suitability rows.")

    index_payload: dict = {
        "districts": [],
        "horizons": [
            {"label": "Near term", "period": "2021-2040"},
            {"label": "≈ +20y", "period": "2041-2060"},
            {"label": "≈ +40y", "period": "2061-2080"},
            {"label": "≈ +60y", "period": "2081-2100"},
        ],
        "scenarios": ["rcp45", "rcp85"],
    }

    for borvidek, group in df.groupby("borvidek"):
        slug = slugify(borvidek)
        region = group["borvidek"].iloc[0]
        # Resolve borregio from suitability table
        bor_rows = suit[suit.borvidek == borvidek]
        borregio = bor_rows["borregio"].iloc[0] if len(bor_rows) else ""

        # Current principal varieties (1991-2020 observed)
        current = suit[
            (suit.borvidek == borvidek)
            & (suit.period == "1991-2020")
            & (suit.scenario == "observed")
            & (suit.in_principal_varieties)
        ][["variety", "variety_en", "colour", "suitability"]].sort_values(
            "suitability", ascending=False
        )
        current_list = [
            {
                "variety": r.variety,
                "variety_en": r.variety_en,
                "colour": r.colour,
                "suitability": round(float(r.suitability), 3),
            }
            for r in current.itertuples(index=False)
        ]

        district_payload: dict = {
            "borvidek": borvidek,
            "borregio": borregio,
            "slug": slug,
            "current_principal_varieties": current_list,
            "horizons": {},
        }

        for (period, scenario), sub in group.groupby(["period", "scenario"]):
            key = f"{period}_{scenario}"

            # At-risk principal varieties at this horizon
            at_risk_df = suit[
                (suit.borvidek == borvidek)
                & (suit.period == period)
                & (suit.scenario == scenario)
                & (suit.in_principal_varieties)
                & (suit.delta_vs_1991_2020 <= -0.20)
            ].sort_values("delta_vs_1991_2020")

            at_risk = [
                {
                    "variety": r.variety,
                    "variety_en": r.variety_en,
                    "colour": r.colour,
                    "future_suitability": round(float(r.suitability), 3),
                    "delta": round(float(r.delta_vs_1991_2020), 3),
                    "limiting_factor": r.limiting_factor,
                }
                for r in at_risk_df.itertuples(index=False)
            ]

            replacements = [
                {
                    "rank": int(r.rank),
                    "variety": r.variety,
                    "variety_en": r.variety_en,
                    "colour": r.colour,
                    "future_suitability": round(float(r.future_suitability), 3),
                    "delta": round(float(r.delta_vs_1991_2020), 3),
                    "confidence": r.confidence,
                    "limiting_factor": r.limiting_factor,
                    "status": r.status,
                    "huglin_mean": int(round(float(r.huglin_mean))),
                    "winkler_mean": int(round(float(r.winkler_mean))),
                }
                for r in sub.sort_values("rank").itertuples(index=False)
            ]

            district_payload["horizons"][key] = {
                "period": period,
                "scenario": scenario,
                "at_risk_principal_varieties": at_risk,
                "replacement_candidates": replacements,
            }

        out_path = SITE_DIR / f"{slug}.json"
        out_path.write_text(
            json.dumps(district_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  wrote {out_path.name}")

        index_payload["districts"].append({
            "borvidek": borvidek,
            "borregio": borregio,
            "slug": slug,
            "file": f"{slug}.json",
        })

    # Index file
    index_payload["districts"].sort(key=lambda d: d["borvidek"])
    index_path = SITE_DIR / "all.json"
    index_path.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote index: {index_path}")
    print(f"Total per-district files: {len(index_payload['districts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
