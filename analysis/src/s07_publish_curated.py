"""
Step 7: Validate, document, and publish the curated dataset bundle.

Reads everything under analysis/curated/, validates it, and writes:
  - curated/manifest.json
  - curated/README.md
  - curated/SHA256SUMS.txt
  - curated/bundle_size.txt

Idempotent: re-running produces identical outputs modulo the generated_at timestamp.
Does NOT mutate any existing data file.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import io
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Force UTF-8 on Windows consoles.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]            # analysis/
CURATED = ROOT / "curated"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(CURATED).as_posix()


def describe_parquet(path: Path, errors: list) -> dict:
    info = {
        "path": rel(path),
        "type": "parquet",
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    try:
        df = pd.read_parquet(path)
        info["rows"] = int(len(df))
        info["columns"] = list(df.columns)
        info["dtypes"] = {c: str(df[c].dtype) for c in df.columns}
        # flag all-NaN columns (where data is expected).
        # Whitelist baseline-vs-baseline anomaly/delta columns which are
        # null by definition in the 1991-2020 reference files.
        EXPECTED_NULL = {
            ("normals/normals_1991-2020_per_district.parquet",
             "anomaly_vs_1991_2020"),
            ("normals/normals_1991-2020_per_district.parquet",
             "anomaly_pct"),
            ("variety_match/district_variety_suitability_1991-2020_observed.parquet",
             "delta_vs_1991_2020"),
        }
        all_nan = [c for c in df.columns if len(df) > 0 and df[c].isna().all()]
        unexpected = [c for c in all_nan if (rel(path), c) not in EXPECTED_NULL]
        if all_nan:
            info["all_nan_columns"] = all_nan
        if unexpected:
            errors.append(f"{rel(path)}: unexpected all-NaN columns {unexpected}")
    except Exception as e:
        errors.append(f"{rel(path)}: parquet load failed: {e}")
        info["load_error"] = str(e)
    return info


def describe_csv(path: Path, errors: list) -> dict:
    info = {
        "path": rel(path),
        "type": "csv",
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding="latin-1")
        except Exception as e:
            errors.append(f"{rel(path)}: csv load failed: {e}")
            info["load_error"] = str(e)
            return info
    except Exception as e:
        errors.append(f"{rel(path)}: csv load failed: {e}")
        info["load_error"] = str(e)
        return info
    info["rows"] = int(len(df))
    info["columns"] = list(df.columns)
    return info


def describe_geojson(path: Path, errors: list) -> dict:
    info = {
        "path": rel(path),
        "type": "geojson",
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    try:
        import geopandas as gpd
        gdf = gpd.read_file(path)
        info["rows"] = int(len(gdf))
        info["columns"] = [c for c in gdf.columns if c != "geometry"]
        crs = gdf.crs.to_string() if gdf.crs is not None else None
        info["crs"] = crs
        if len(gdf) != 22:
            errors.append(f"{rel(path)}: expected 22 features, got {len(gdf)}")
        if crs and "4326" not in crs:
            errors.append(f"{rel(path)}: expected EPSG:4326, got {crs}")
        invalid = int((~gdf.geometry.is_valid).sum())
        if invalid > 0:
            errors.append(f"{rel(path)}: {invalid} invalid geometries")
        info["invalid_geometries"] = invalid
    except Exception as e:
        errors.append(f"{rel(path)}: geojson load failed: {e}")
        info["load_error"] = str(e)
    return info


def describe_generic(path: Path) -> dict:
    return {
        "path": rel(path),
        "type": path.suffix.lstrip(".").lower() or "file",
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


# --------------------------------------------------------------------------- #
# Winkler-shift headline
# --------------------------------------------------------------------------- #

def winkler_class(gdd: float) -> str:
    """Amerine & Winkler regions (base 10 C)."""
    if gdd is None or pd.isna(gdd):
        return "NA"
    if gdd < 1389:
        return "Ia"
    if gdd < 1667:
        return "Ib"
    if gdd < 1944:
        return "II"
    if gdd < 2222:
        return "III"
    if gdd < 2500:
        return "IV"
    return "V"


WINKLER_ORDER = ["Ia", "Ib", "II", "III", "IV", "V"]


def class_to_ord(c: str) -> int:
    try:
        return WINKLER_ORDER.index(c)
    except ValueError:
        return -1


def compute_headline_winkler_shift() -> dict:
    base = pd.read_parquet(CURATED / "normals" / "normals_1991-2020_per_district.parquet")
    fut = pd.read_parquet(CURATED / "normals" / "normals_2071-2100_rcp85_per_district.parquet")

    base_w = base[base["index"] == "winkler_gdd"][["borvidek", "mean"]].rename(
        columns={"mean": "gdd_base"}
    )
    fut_w = fut[fut["index"] == "winkler_gdd"][["borvidek", "mean"]].rename(
        columns={"mean": "gdd_fut"}
    )
    merged = base_w.merge(fut_w, on="borvidek", how="inner")
    merged["class_base"] = merged["gdd_base"].apply(winkler_class)
    merged["class_fut"] = merged["gdd_fut"].apply(winkler_class)
    merged["shift_steps"] = merged.apply(
        lambda r: class_to_ord(r["class_fut"]) - class_to_ord(r["class_base"]),
        axis=1,
    )
    merged["delta_gdd"] = merged["gdd_fut"] - merged["gdd_base"]

    top = merged.sort_values("shift_steps", ascending=False).iloc[0]
    return {
        "district": str(top["borvidek"]),
        "class_base": str(top["class_base"]),
        "class_fut": str(top["class_fut"]),
        "shift_steps": int(top["shift_steps"]),
        "gdd_base": float(top["gdd_base"]),
        "gdd_fut": float(top["gdd_fut"]),
        "delta_gdd": float(top["delta_gdd"]),
        "table": merged[
            ["borvidek", "gdd_base", "gdd_fut", "class_base", "class_fut", "shift_steps"]
        ].sort_values("shift_steps", ascending=False),
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    assert CURATED.exists(), f"Missing curated dir: {CURATED}"

    validation_errors: list[str] = []
    files_meta: list[dict] = []

    # Walk the tree deterministically (sorted).
    all_files = sorted(
        [p for p in CURATED.rglob("*") if p.is_file()],
        key=lambda p: rel(p),
    )

    # Exclude outputs that we're about to (re)generate so manifest is stable.
    EXCLUDE = {"manifest.json", "README.md", "SHA256SUMS.txt", "bundle_size.txt"}
    all_files = [p for p in all_files if rel(p) not in EXCLUDE]

    print(f"[s07] scanning {len(all_files)} files under {CURATED}")

    for p in all_files:
        suf = p.suffix.lower()
        if suf == ".parquet":
            meta = describe_parquet(p, validation_errors)
        elif suf == ".csv":
            meta = describe_csv(p, validation_errors)
        elif suf == ".geojson":
            meta = describe_geojson(p, validation_errors)
        elif suf in {".json", ".md", ".txt"}:
            meta = describe_generic(p)
        else:
            meta = describe_generic(p)
        files_meta.append(meta)

    total_bytes = sum(m["size_bytes"] for m in files_meta)
    total_mb = round(total_bytes / (1024 * 1024), 3)

    # Per-subfolder bundle size
    per_folder: dict[str, int] = {}
    for m in files_meta:
        parts = m["path"].split("/")
        key = parts[0] if len(parts) > 1 else "(root)"
        per_folder[key] = per_folder.get(key, 0) + m["size_bytes"]

    # Row-count headlines
    def load_rows(rel_path: str) -> int:
        p = CURATED / rel_path
        if not p.exists():
            return 0
        return int(len(pd.read_parquet(p)))

    normals_rows = 0
    for p in (CURATED / "normals").glob("*.parquet"):
        normals_rows += int(len(pd.read_parquet(p)))

    suitability_rows = load_rows("variety_match/suitability_long.parquet")

    cckp_rows = 0
    for p in (CURATED / "cckp").glob("*.parquet"):
        cckp_rows += int(len(pd.read_parquet(p)))

    # Headline Winkler shift
    try:
        winkler = compute_headline_winkler_shift()
    except Exception as e:
        winkler = None
        validation_errors.append(f"headline winkler computation failed: {e}")

    # ------------------------------------------------------------------ #
    # Manifest
    # ------------------------------------------------------------------ #
    descriptions = {
        "wine_districts.geojson": "22 Hungarian wine districts dissolved from the manually-labelled admin8 settlements layer (EPSG:4326, simplified).",
        "indices/indices_rcp45_annual.parquet": "Annual viticulture indices per district, FORESEE v1.1 CNRM-ALADIN53 RCP4.5.",
        "indices/indices_rcp85_annual.parquet": "Annual viticulture indices per district, FORESEE v1.1 CNRM-ALADIN53 RCP8.5.",
        "normals/normals_1971-2000_per_district.parquet": "30-year normals (observed, 1971-2000) + trends + anomalies + risk flags.",
        "normals/normals_1991-2020_per_district.parquet": "30-year normals (observed baseline, 1991-2020).",
        "normals/normals_2041-2070_rcp45_per_district.parquet": "30-year normals (RCP4.5, mid-century).",
        "normals/normals_2041-2070_rcp85_per_district.parquet": "30-year normals (RCP8.5, mid-century).",
        "normals/normals_2071-2100_rcp45_per_district.parquet": "30-year normals (RCP4.5, end-century).",
        "normals/normals_2071-2100_rcp85_per_district.parquet": "30-year normals (RCP8.5, end-century).",
        "variety_match/suitability_long.parquet": "Long union of all per-(district, variety, period, scenario) suitability scores.",
        "variety_match/headline_winners_losers.csv": "Top varieties rising and falling across districts between baseline and RCP8.5 2071-2100.",
        "cckp/cckp_summary.csv": "Wide summary of CCKP CMIP6 ensemble stats per (district, variable, scenario, period).",
        "threats/README.md": "Documentation for the threats/ subfolder (draft; needs web verification).",
        "threats/flavescence_doree_timeline.csv": "DRAFT: Flavescence doree detection timeline in Hungary. NEEDS WEB VERIFICATION.",
        "threats/trunk_diseases.csv": "DRAFT: Grapevine trunk disease summary. NEEDS WEB VERIFICATION.",
        "threats/pest_disease_regulatory.csv": "DRAFT: EU/Hungary pest & disease regulatory status. NEEDS WEB VERIFICATION.",
        "threats/eu_pesticides_actives.csv": "DRAFT: EU pesticides database extract for viticulture active substances. NEEDS WEB VERIFICATION.",
    }
    for m in files_meta:
        if m["path"] in descriptions:
            m["description"] = descriptions[m["path"]]
        elif m["path"].startswith("variety_match/district_variety_suitability_"):
            m["description"] = "Per-(district, variety) suitability scores for a specific (period, scenario)."
        elif m["path"].startswith("cckp/cckp_cmip6_"):
            m["description"] = "CCKP CMIP6 multi-model ensemble stats per district for a specific (variable, scenario)."

    manifest = {
        "bundle_name": "bor-szolo_curated",
        "version": "v1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "license": (
            "Derived data from FORESEE v1.1 (CNRM-ALADIN53 RCP runs) + "
            "World Bank CCKP CMIP6 ensemble; raw underlying climate data is "
            "not redistributed in this bundle."
        ),
        "citation_required": [
            "FORESEE v1.1 dataset (Dobor et al.)",
            "World Bank Climate Change Knowledge Portal CMIP6 0.25 degree (worldbank/climateknowledgeportal)",
            "Frontiers in Plant Science 2025 https://doi.org/10.3389/fpls.2025.1481431 (Hungarian wine region temperature indices benchmark)",
        ],
        "files": files_meta,
        "totals": {
            "n_files": len(files_meta),
            "total_size_mb": total_mb,
            "n_districts": 22,
            "n_varieties": 38,
            "n_indices": 9,
            "scenarios": ["observed", "rcp45", "rcp85"],
            "periods": ["1971-2000", "1991-2020", "2041-2070", "2071-2100"],
            "normals_rows": normals_rows,
            "suitability_rows": suitability_rows,
            "cckp_rows": cckp_rows,
        },
        "headline": (
            {
                "metric": "max_winkler_class_shift_rcp85_2071_2100",
                "district": winkler["district"],
                "class_base": winkler["class_base"],
                "class_future": winkler["class_fut"],
                "shift_steps": winkler["shift_steps"],
                "gdd_base": round(winkler["gdd_base"], 1),
                "gdd_future": round(winkler["gdd_fut"], 1),
                "delta_gdd": round(winkler["delta_gdd"], 1),
            }
            if winkler
            else None
        ),
        "validation_errors": validation_errors,
        "draft_flags": [
            "threats/*.csv - domain-knowledge stubs without live source verification (subagent web tools were denied during initial curation); MUST be verified before publication.",
            "config/grape_envelopes.csv - frost_tolerance_days were re-calibrated post hoc to match the index definition; the underlying confidence ratings remain as bootstrapped.",
        ],
    }

    manifest_path = CURATED / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=False),
        encoding="utf-8",
    )
    print(f"[s07] wrote {manifest_path}")

    # ------------------------------------------------------------------ #
    # README.md
    # ------------------------------------------------------------------ #
    readme = f"""# bor-szolo curated bundle (v1.0.0)

This bundle is the analysis-ready output of the Hungarian wine district
climate pipeline. It provides per-district viticulture indices, 30-year
climate normals, variety-suitability scores, a multi-model validation
layer from the World Bank CCKP, and a curated (draft) threats dossier,
all keyed to Hungary's 22 official wine districts (borvidek) grouped into
6 wine regions (borregio): Balaton, Duna, Eger, Pannon, Sopron, and
Tokaj.

## Folder layout

- `wine_districts.geojson` - 22 districts dissolved from the
  manually-labelled admin8 settlements layer (EPSG:4326, simplified).
- `indices/` - Annual viticulture indices per district for each RCP
  scenario (FORESEE v1.1, CNRM-ALADIN53).
- `normals/` - 30-year normals with trends, anomalies vs 1991-2020, and
  risk flags for each (period, scenario) combo.
- `variety_match/` - Per-(district, variety, period, scenario)
  suitability scores with limiting factors, plus a long-format union
  and a headline winners/losers CSV.
- `cckp/` - World Bank CCKP CMIP6 multi-model ensemble per-district
  stats for 7 variables across 3 scenarios. Used as an independent
  validation layer, not as the primary projection.
- `threats/` - Curated dossier on Flavescence doree, grapevine trunk
  diseases, pest/disease regulatory status, and EU pesticide actives.
  **DRAFT - needs web verification before publication.**

## Data sources and roles

| Source | Role |
|---|---|
| FORESEE v1.1 (Dobor et al.) | Primary daily-resolution projection (CNRM-ALADIN53 under RCP4.5 and RCP8.5). Drives `indices/`, `normals/`, `variety_match/`. |
| World Bank CCKP CMIP6 0.25 deg | Independent multi-model validation layer (`cckp/`). |
| Frontiers in Plant Science 2025 (10.3389/fpls.2025.1481431) | Benchmark reference for Hungarian wine region temperature indices. |
| Curated threats dossier | Flavescence doree, trunk diseases, EU regulation (DRAFT). |

## Viticulture indices (9)

| Index | One-line definition |
|---|---|
| `winkler_gdd` | Growing-season degree days base 10 C, Apr-Oct (Amerine & Winkler regions). |
| `huglin_index` | Heliothermal index with daylength correction, Apr-Sep. |
| `gst` | Mean growing-season temperature, Apr-Oct (Jones wine-style bands). |
| `bedd` | Biologically Effective Degree Days base 10 C, capped at 19 C. |
| `cool_night_index` | Mean minimum temperature in September (colour & aroma proxy). |
| `frost_days` | Count of days with Tmin < -2 C between bud-break and Oct. |
| `heat_days` | Count of days with Tmax >= 35 C during the growing season. |
| `growing_season_precip` | Cumulative precipitation Apr-Oct. |
| `dry_days_js` | Count of July-August days with P < 1 mm (drought proxy). |

## Periods and scenarios

- **Periods:** 1971-2000 (historical), 1991-2020 (observed baseline),
  2041-2070 (mid-century), 2071-2100 (end-century).
- **Scenarios:** `observed` (for the two historical periods), `rcp45`,
  `rcp85` (for the two future periods).

## Citation

If you use this bundle, please cite ALL of:

1. FORESEE v1.1 (Dobor et al.) for the underlying daily climate data.
2. World Bank Climate Change Knowledge Portal CMIP6 0.25 deg for the
   validation layer.
3. Frontiers in Plant Science 2025,
   <https://doi.org/10.3389/fpls.2025.1481431>, for the Hungarian wine
   region temperature-index benchmark that the indices in this bundle
   are calibrated against.

## License

Derived data only. Raw underlying FORESEE and CCKP fields are **not**
redistributed in this bundle; only per-district aggregates, normals,
and derived indices are published here. Users needing the raw fields
must fetch them directly from the original providers under their
respective licenses.

## Known limitations

- **Single-model RCP projection.** The primary future projection uses
  only the CNRM-ALADIN53 run of FORESEE v1.1; the CCKP layer is the
  multi-model ensemble cross-check.
- **Hargreaves PET.** Future-period evapotranspiration uses Hargreaves
  (Tmin/Tmax/Ra) rather than Penman-Monteith, because radiation and
  wind fields were unavailable at daily resolution for the projections.
- **Bootstrapped variety envelopes.** The 38-variety climate envelopes
  are seeded from training-knowledge literature and need expert review;
  `confidence` ratings reflect the bootstrap provenance.
- **Draft threats CSVs.** Everything under `threats/` is a
  domain-knowledge stub; subagent web tools were denied during initial
  curation, so sources are **unverified**. Do not publish without
  live-source verification.
- **RCP8.5 2071-2100 suitability collapse.** Under end-century RCP8.5,
  suitability scores for many districts collapse toward zero. This
  should be read as "currently-grown varieties become unsuited" rather
  than "no wine production possible" - drought- and heat-tolerant
  southern varieties outside the current 38-variety list are not
  evaluated here.

## Headline numbers

- Total files: {len(files_meta)}
- Total size: {total_mb} MB
- Normals rows (district x index x period x scenario): {normals_rows}
- Suitability rows (district x variety x period x scenario): {suitability_rows}
- CCKP rows (district x variable x period x scenario x stat): {cckp_rows}
"""
    if winkler:
        readme += (
            f"- **Biggest Winkler-class shift (RCP8.5, 2071-2100):** "
            f"{winkler['district']} moves from class {winkler['class_base']} "
            f"to {winkler['class_fut']} ({winkler['shift_steps']} steps, "
            f"+{winkler['delta_gdd']:.0f} GDD).\n"
        )

    readme_path = CURATED / "README.md"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"[s07] wrote {readme_path}")

    # ------------------------------------------------------------------ #
    # SHA256SUMS.txt
    # ------------------------------------------------------------------ #
    sha_lines = [f"{m['sha256']}  {m['path']}" for m in files_meta]
    (CURATED / "SHA256SUMS.txt").write_text(
        "\n".join(sha_lines) + "\n", encoding="utf-8"
    )
    print(f"[s07] wrote SHA256SUMS.txt ({len(sha_lines)} entries)")

    # ------------------------------------------------------------------ #
    # bundle_size.txt
    # ------------------------------------------------------------------ #
    lines = []
    for folder in sorted(per_folder):
        mb = per_folder[folder] / (1024 * 1024)
        lines.append(f"{folder:<20s} {mb:>10.3f} MB")
    lines.append("-" * 34)
    lines.append(f"{'TOTAL':<20s} {total_mb:>10.3f} MB")
    (CURATED / "bundle_size.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"[s07] wrote bundle_size.txt")

    # ------------------------------------------------------------------ #
    # Final summary
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("  CURATED BUNDLE SUMMARY")
    print("=" * 60)
    print(f"  files              : {len(files_meta)}")
    print(f"  total size         : {total_mb} MB")
    print(f"  normals rows       : {normals_rows}")
    print(f"  suitability rows   : {suitability_rows}")
    print(f"  cckp rows          : {cckp_rows}")
    print(f"  validation errors  : {len(validation_errors)}")
    if winkler:
        print()
        print(
            f"  HEADLINE: {winkler['district']} shifts Winkler "
            f"{winkler['class_base']} -> {winkler['class_fut']} "
            f"({winkler['shift_steps']} steps, +{winkler['delta_gdd']:.0f} GDD) "
            f"under RCP8.5 2071-2100"
        )
    print()
    print("  Per-folder size:")
    for line in lines:
        print(f"    {line}")
    if validation_errors:
        print()
        print("  VALIDATION ERRORS:")
        for e in validation_errors:
            print(f"    - {e}")
    print("=" * 60)


if __name__ == "__main__":
    main()
