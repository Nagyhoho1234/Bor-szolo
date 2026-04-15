# -*- coding: utf-8 -*-
"""
Step 0 — Build Hungarian wine district polygons.

Reads the manually-labelled settlement shapefile (admin8.shp) and dissolves
settlements by their `Borvidek` attribute into 22 wine-district polygons.
Adds parent borrégió, computes area (in EOV) and centroids (in WGS84), and
writes canonical geo files plus a simplified GeoJSON for the web map.

Read-only on the input shapefile. All outputs go under analysis/.
"""

from __future__ import annotations

import sys
import unicodedata
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(r"C:/Bor-szőlő")
SRC_SHP = ROOT / "admin8.shp"

ANALYSIS = ROOT / "analysis"
GEO_DIR = ANALYSIS / "geo"
CURATED_DIR = ANALYSIS / "curated"
REPORTS_FIG = ANALYSIS / "reports" / "figures"

for d in (GEO_DIR, CURATED_DIR, REPORTS_FIG):
    d.mkdir(parents=True, exist_ok=True)

OUT_SHP = GEO_DIR / "wine_districts.shp"
OUT_GPKG = GEO_DIR / "wine_districts.gpkg"
OUT_CENTROIDS = GEO_DIR / "wine_districts_centroids.csv"
OUT_GEOJSON = CURATED_DIR / "wine_districts.geojson"
OUT_FIG = REPORTS_FIG / "wine_districts_dissolved.png"

# ---------------------------------------------------------------------------
# Borvidék -> Borrégió mapping (using actual spellings as found in admin8.dbf)
# ---------------------------------------------------------------------------
BORVIDEK_TO_BORREGIO = {
    # Balaton
    "Badacsonyi": "Balaton",
    "Balatonboglári": "Balaton",
    "Balatonfüred-Csopaki": "Balaton",
    "Balatonfelvidéki": "Balaton",
    "Nagy-Somlói": "Balaton",
    "Zalai": "Balaton",
    # Felső-Pannon
    "Etyek-Budai": "Felső-Pannon",
    "Móri": "Felső-Pannon",
    "Neszmélyi": "Felső-Pannon",
    "Pannonhalmi": "Felső-Pannon",
    "Soproni": "Felső-Pannon",
    # Duna
    "Csongrádi": "Duna",
    "Hajós-Bajai": "Duna",
    "Kunsági": "Duna",
    # Felső-Magyarországi
    "Bükki": "Felső-Magyarországi",
    "Egri": "Felső-Magyarországi",
    "Mátrai": "Felső-Magyarországi",
    # Pannon
    "Pécsi": "Pannon",
    "Szekszárdi": "Pannon",
    "Tolnai": "Pannon",
    "Villányi": "Pannon",
    # Tokaj
    "Tokaji": "Tokaj",
}


def strip_diacritics(s: str) -> str:
    """Recognisable ASCII version for borvidek_en."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def main() -> int:
    print(f"[s00] Reading {SRC_SHP}")
    gdf = gpd.read_file(SRC_SHP, encoding="utf-8")
    print(f"[s00] Loaded {len(gdf)} settlements, CRS={gdf.crs}, cols={list(gdf.columns)}")

    # Verify encoding round-trip
    sample = gdf["NAME"].dropna().astype(str).iloc[0]
    print(f"[s00] Encoding sanity: first NAME = {sample!r}")

    # Normalise Borvidek
    gdf["Borvidek"] = gdf["Borvidek"].fillna("").astype(str).str.strip()
    mask = gdf["Borvidek"] != ""
    sub = gdf.loc[mask].copy()
    print(f"[s00] Settlements with Borvidek label: {len(sub)}")

    # Unique values + counts
    counts = (
        sub["Borvidek"].value_counts().sort_index().rename_axis("borvidek").to_frame("n")
    )
    print("[s00] Unique Borvidek values and settlement counts:")
    for name, row in counts.iterrows():
        print(f"    {name:<25s} {int(row['n']):>4d}")
    print(f"[s00] Total unique borvidek: {len(counts)}")

    # Dissolve
    print("[s00] Dissolving by Borvidek ...")
    diss = sub.dissolve(by="Borvidek", aggfunc={"NAME": "count"}).reset_index()
    diss = diss.rename(columns={"NAME": "n_settlements", "Borvidek": "borvidek"})
    print(f"[s00] Dissolved to {len(diss)} polygons")

    # Borrégió mapping
    diss["borregio"] = diss["borvidek"].map(BORVIDEK_TO_BORREGIO)
    missing = diss[diss["borregio"].isna()]["borvidek"].tolist()
    if missing:
        warnings.warn(
            f"!!! UNMAPPED borvidek values (no borrégió): {missing}",
            stacklevel=1,
        )
        print(f"[s00] WARNING — unmapped: {missing}")
    else:
        print("[s00] All borvidek values mapped to a borrégió.")

    # English / ASCII display name
    diss["borvidek_en"] = diss["borvidek"].map(strip_diacritics)

    # ---- compute area in EOV (EPSG:23700) ----
    print("[s00] Reprojecting to EOV (EPSG:23700) for area ...")
    diss_eov = diss.to_crs(23700)
    diss["area_km2"] = (diss_eov.geometry.area / 1e6).round(3)

    # ---- centroids in WGS84 ----
    print("[s00] Computing centroids in WGS84 ...")
    cent_wgs = diss_eov.geometry.centroid.to_crs(4326)
    diss["centroid_lon"] = cent_wgs.x.round(6)
    diss["centroid_lat"] = cent_wgs.y.round(6)

    # ---- final geometry to WGS84 ----
    print("[s00] Reprojecting polygons to EPSG:4326 (canonical) ...")
    diss_wgs = diss.to_crs(4326)

    # Column order
    cols = [
        "borvidek",
        "borvidek_en",
        "borregio",
        "n_settlements",
        "area_km2",
        "centroid_lat",
        "centroid_lon",
        "geometry",
    ]
    diss_wgs = diss_wgs[cols]

    # ---- write outputs ----
    print(f"[s00] Writing {OUT_SHP}")
    diss_wgs.to_file(OUT_SHP, encoding="utf-8")

    print(f"[s00] Writing {OUT_GPKG}")
    diss_wgs.to_file(OUT_GPKG, driver="GPKG", layer="wine_districts")

    print(f"[s00] Writing {OUT_CENTROIDS}")
    cent_df = diss_wgs[
        ["borvidek", "borregio", "centroid_lat", "centroid_lon"]
    ].rename(columns={"centroid_lat": "lat", "centroid_lon": "lon"})
    cent_df.to_csv(OUT_CENTROIDS, index=False, encoding="utf-8")

    # Simplified GeoJSON for web map (target ≤ 500 KB)
    simp_props = ["borvidek", "borregio", "n_settlements", "area_km2", "geometry"]
    simp = diss_wgs[simp_props].copy()
    tol = 0.001
    simp["geometry"] = simp.geometry.simplify(tol, preserve_topology=True)
    print(f"[s00] Writing {OUT_GEOJSON} (simplify tol={tol} deg)")
    if OUT_GEOJSON.exists():
        OUT_GEOJSON.unlink()
    simp.to_file(OUT_GEOJSON, driver="GeoJSON")

    # If too big, increase tolerance
    size_kb = OUT_GEOJSON.stat().st_size / 1024
    while size_kb > 500 and tol < 0.05:
        tol *= 2
        simp["geometry"] = diss_wgs.geometry.simplify(tol, preserve_topology=True)
        OUT_GEOJSON.unlink()
        simp.to_file(OUT_GEOJSON, driver="GeoJSON")
        size_kb = OUT_GEOJSON.stat().st_size / 1024
        print(f"[s00]   re-simplified at tol={tol:.4f} -> {size_kb:.1f} KB")
    print(f"[s00] GeoJSON final size: {size_kb:.1f} KB")

    # ---- summary table ----
    print("\n[s00] === Summary: 22 wine districts ===")
    summary = diss_wgs[
        ["borvidek", "borregio", "n_settlements", "area_km2"]
    ].sort_values("borvidek").reset_index(drop=True)
    with pd.option_context("display.max_rows", None, "display.width", 120):
        print(summary.to_string(index=False))
    print(
        f"\n[s00] Total districts: {len(summary)}   "
        f"Total settlements covered: {int(summary['n_settlements'].sum())}   "
        f"Total area: {summary['area_km2'].sum():.1f} km^2"
    )

    # ---- file sizes ----
    print("\n[s00] Output file sizes:")
    for p in (OUT_SHP, OUT_GPKG, OUT_CENTROIDS, OUT_GEOJSON):
        kb = p.stat().st_size / 1024
        print(f"    {p.name:<35s} {kb:>10.1f} KB")

    # ---- sanity figure ----
    print(f"\n[s00] Rendering sanity figure -> {OUT_FIG}")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Country outline from admin8 dissolved
        country = gdf.to_crs(4326).dissolve()

        fig, ax = plt.subplots(figsize=(11, 8))
        country.boundary.plot(ax=ax, color="black", linewidth=0.6)
        diss_wgs.plot(
            ax=ax,
            column="borvidek",
            categorical=True,
            legend=True,
            cmap="tab20",
            edgecolor="white",
            linewidth=0.4,
            legend_kwds={
                "bbox_to_anchor": (1.02, 1),
                "loc": "upper left",
                "fontsize": 7,
                "title": "Borvidék",
            },
        )
        ax.set_title("Hungarian wine districts (dissolved from admin8)")
        ax.set_xlabel("lon")
        ax.set_ylabel("lat")
        ax.set_aspect("equal")
        plt.tight_layout()
        plt.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"[s00] Figure saved ({OUT_FIG.stat().st_size/1024:.1f} KB)")
    except Exception as e:
        print(f"[s00] WARNING: figure rendering failed: {e}")

    print("\n[s00] Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
