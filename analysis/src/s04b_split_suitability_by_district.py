"""
s04b_split_suitability_by_district.py

Splits the monolithic `suitability_long.parquet` into per-district parquet
and JSON files so that each district detail page on the site only loads its
own slice (the monolith is ~5 MB and was being fetched on every district
detail page even though each page only needs that district's rows).

Inputs:
    analysis/curated/variety_match/suitability_long.parquet

Outputs:
    analysis/curated/variety_match/by_district/<slug>.parquet
    analysis/curated/variety_match/by_district/<slug>.json

The slug rule mirrors site/src/lib/district-meta.ts `slugify()`:
    NFD normalize -> strip combining marks -> ő/Ő->o, ű/Ű->u -> lowercase
    -> replace non-[a-z0-9]+ runs with '-' -> trim '-' from ends.

Idempotent: re-running overwrites the outputs deterministically.

Run:
    python analysis/src/s04b_split_suitability_by_district.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import pyarrow.parquet as pq

# Make stdout UTF-8-safe on Windows consoles.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "analysis" / "curated" / "variety_match" / "suitability_long.parquet"
OUT_DIR = REPO_ROOT / "analysis" / "curated" / "variety_match" / "by_district"


def slugify(s: str) -> str:
    """Mirror of the site's slugify() in src/lib/district-meta.ts."""
    # NFD normalize and strip combining marks.
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # The JS slugify also explicitly maps ő/ű because NFD doesn't decompose
    # the Hungarian double-acute into mark+base on all platforms. We do the
    # same to guarantee identical slugs between Python and TypeScript.
    s = s.replace("ő", "o").replace("Ő", "o").replace("ű", "u").replace("Ű", "u")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def _clean(v):
    if v is None:
        return None
    if isinstance(v, float) and v != v:  # NaN
        return None
    return v


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(f"Missing source parquet: {SRC}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tbl = pq.read_table(SRC)
    total_rows = tbl.num_rows
    borvidek_col = tbl.column("borvidek").to_pylist()
    unique_borvidek = sorted(set(borvidek_col))

    monolith_json_sibling = SRC.with_suffix(".json")
    monolith_json_size = (
        monolith_json_sibling.stat().st_size if monolith_json_sibling.exists() else 0
    )
    monolith_parquet_size = SRC.stat().st_size

    # Build a boolean mask per district and write both parquet + json.
    per_district_stats: list[tuple[str, str, int, int, int]] = []
    # (borvidek, slug, row_count, parquet_bytes, json_bytes)
    total_rows_written = 0

    import pyarrow.compute as pc

    for bv in unique_borvidek:
        slug = slugify(bv)
        mask = pc.equal(tbl.column("borvidek"), bv)
        sub = tbl.filter(mask)
        # Sort deterministically for idempotent output.
        sub = sub.sort_by(
            [
                ("variety", "ascending"),
                ("period", "ascending"),
                ("scenario", "ascending"),
            ]
        )
        parquet_path = OUT_DIR / f"{slug}.parquet"
        json_path = OUT_DIR / f"{slug}.json"

        pq.write_table(sub, parquet_path)

        records = sub.to_pylist()
        for r in records:
            for k, v in list(r.items()):
                r[k] = _clean(v)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, separators=(",", ":"))

        per_district_stats.append(
            (
                bv,
                slug,
                sub.num_rows,
                parquet_path.stat().st_size,
                json_path.stat().st_size,
            )
        )
        total_rows_written += sub.num_rows

    # Report.
    print(f"Source monolith: {SRC}")
    print(f"  rows: {total_rows}")
    print(f"  parquet bytes: {monolith_parquet_size:,}")
    print(f"  json bytes   : {monolith_json_size:,}")
    print()
    print(f"Wrote {len(unique_borvidek)} districts to {OUT_DIR}")
    print(f"  total rows written across splits: {total_rows_written}")
    print(f"  row-count match: {total_rows_written == total_rows}")
    print()
    json_sizes = [s[4] for s in per_district_stats]
    min_js, max_js = min(json_sizes), max(json_sizes)
    mean_js = sum(json_sizes) / len(json_sizes)
    print(
        f"Per-district JSON sizes: min={min_js:,} B  max={max_js:,} B  "
        f"mean={mean_js:,.0f} B"
    )
    total_json_saved = monolith_json_size - int(mean_js)
    print(
        f"Avg bytes saved per district page load: "
        f"{total_json_saved:,} ({total_json_saved / 1024:.0f} KB)"
    )
    print()
    print("Per-district detail (sorted by json bytes, desc):")
    for bv, slug, n, pb, jb in sorted(
        per_district_stats, key=lambda x: -x[4]
    ):
        print(f"  {slug:<22} {bv:<22} rows={n:>4}  parquet={pb:>7,} B  json={jb:>7,} B")


if __name__ == "__main__":
    main()
