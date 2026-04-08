"""
Export per-district COMBINED suitability JSON: baseline + RCP4.5 + RCP8.5
side-by-side for every future period. The chart only needs to fetch ONE
file per district, the user picks a period from a dropdown, and the bars
re-render from in-memory data.

Reads:
  analysis/curated/variety_match/suitability_long.parquet

Writes:
  analysis/curated/variety_match_combined/{slug}.json   (22 files)
  analysis/curated/variety_match_combined/all.json      (index)

Each per-district file has the shape:

{
  "borvidek": "Tokaji",
  "borregio": "Tokaj",
  "slug": "tokaji",
  "baseline_period": "1991-2020",
  "future_periods": ["2021-2040", "2041-2060", "2061-2080", "2081-2100"],
  "varieties": [
    {
      "variety": "Furmint",
      "variety_en": "Furmint",
      "colour": "white",
      "in_principal": true,
      "baseline": 0.73,
      "scenarios": {
        "2021-2040": {"rcp45": 0.74, "rcp85": 0.78},
        "2041-2060": {"rcp45": 0.72, "rcp85": 0.75},
        "2061-2080": {"rcp45": 0.65, "rcp85": 0.45},
        "2081-2100": {"rcp45": 0.55, "rcp85": 0.17}
      }
    },
    ...
  ]
}
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
PARQUET = ROOT / "analysis" / "curated" / "variety_match" / "suitability_long.parquet"
OUT_DIR = ROOT / "analysis" / "curated" / "variety_match_combined"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASELINE_PERIOD = "1991-2020"
FUTURE_PERIODS = ["2021-2040", "2041-2060", "2061-2080", "2081-2100"]
SCENARIOS = ["rcp45", "rcp85"]


def slugify(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    out = ""
    for c in ascii_str.lower():
        if c.isalnum():
            out += c
        elif out and out[-1] != "-":
            out += "-"
    return out.strip("-")


def round_or_none(v):
    if v is None or (isinstance(v, float) and v != v):
        return None
    return round(float(v), 3)


def main() -> int:
    df = pd.read_parquet(PARQUET)
    print(f"Loaded {len(df)} rows, {df.borvidek.nunique()} districts, "
          f"{df.variety.nunique()} varieties.")

    # Stable variety order: principals first (by baseline suitability desc),
    # then non-principals (by max future suitability desc)
    index_payload: dict = {
        "districts": [],
        "baseline_period": BASELINE_PERIOD,
        "future_periods": FUTURE_PERIODS,
        "scenarios": SCENARIOS,
    }

    for borvidek in sorted(df.borvidek.unique()):
        slug = slugify(borvidek)
        sub = df[df.borvidek == borvidek]
        borregio = sub["borregio"].iloc[0]

        # Variety ordering: principals first
        baseline = sub[(sub.period == BASELINE_PERIOD) & (sub.scenario == "observed")]
        baseline_map = baseline.set_index("variety").to_dict("index")

        # Sort: principals by baseline desc, then non-principals by max future suitability desc
        future_max = (
            sub[sub.period.isin(FUTURE_PERIODS)]
            .groupby("variety")["suitability"]
            .max()
            .to_dict()
        )

        def variety_sort_key(v: str) -> tuple:
            row = baseline_map.get(v, {})
            principal = bool(row.get("in_principal_varieties", False))
            base_suit = float(row.get("suitability") or 0.0)
            fmax = float(future_max.get(v, 0.0))
            # principals first (False sorts before True so negate)
            return (not principal, -base_suit, -fmax)

        varieties_sorted = sorted(baseline_map.keys(), key=variety_sort_key)

        variety_records = []
        for variety in varieties_sorted:
            base_row = baseline_map[variety]
            scenarios_payload: dict = {}
            for period in FUTURE_PERIODS:
                period_payload: dict = {}
                for scenario in SCENARIOS:
                    cell = sub[
                        (sub.variety == variety)
                        & (sub.period == period)
                        & (sub.scenario == scenario)
                    ]
                    if not cell.empty:
                        r = cell.iloc[0]
                        period_payload[scenario] = {
                            "suitability": round_or_none(r["suitability"]),
                            "delta": round_or_none(r["delta_vs_1991_2020"]),
                            "limiting_factor": r["limiting_factor"],
                        }
                    else:
                        period_payload[scenario] = None
                scenarios_payload[period] = period_payload

            variety_records.append({
                "variety": variety,
                "variety_en": base_row.get("variety_en", variety),
                "colour": base_row.get("colour"),
                "confidence": base_row.get("confidence"),
                "in_principal": bool(base_row.get("in_principal_varieties", False)),
                "baseline": round_or_none(base_row.get("suitability")),
                "scenarios": scenarios_payload,
            })

        district_payload = {
            "borvidek": borvidek,
            "borregio": borregio,
            "slug": slug,
            "baseline_period": BASELINE_PERIOD,
            "future_periods": FUTURE_PERIODS,
            "scenarios": SCENARIOS,
            "varieties": variety_records,
        }

        out_path = OUT_DIR / f"{slug}.json"
        out_path.write_text(
            json.dumps(district_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  wrote {out_path.name}  varieties={len(variety_records)}")

        index_payload["districts"].append({
            "borvidek": borvidek,
            "borregio": borregio,
            "slug": slug,
            "file": f"{slug}.json",
        })

    index_path = OUT_DIR / "all.json"
    index_path.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote index: {index_path}")
    print(f"Total per-district files: {len(index_payload['districts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
