"""Step 12, appendix figures for the 14-member ensemble analysis.

Renders three supplementary figures and one table for the paper appendix:

- **Figure S3**  ensemble envelope (p10-p90) of national-mean suitability
                  vs. the CNRM-ALADIN53 trajectory, 1971-2100, RCP4.5 and RCP8.5;
- **Figure S4**  p10/p50/p90 district maps at 2081-2100 RCP8.5;
- **Figure S5**  crossover-year distribution across members per district;
- **Table S1**   ensemble mean + p10/p90 of 2081-2100 RCP8.5 suitability for
                  the four spotlight districts plus per-member crossover years.

Reads from ``analysis/curated/ensemble/ensemble_*.parquet`` produced by s11.
Figure panels are rendered in parallel via ``ProcessPoolExecutor``.
"""

from __future__ import annotations

import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
PAPER_FIG = Path(r"C:/Bor-szőlő/ResearchPotential/paper/figures")
import os as _os
_VARIANT = _os.environ.get("HUGLIN_VARIANT", "").upper()
ENSEMBLE_DIR = (ANALYSIS / "curated" / "ensemble_variants" / _VARIANT) if _VARIANT else (ANALYSIS / "curated" / "ensemble")
PAPER_FIG.mkdir(parents=True, exist_ok=True)

SPOTLIGHT = ("Soproni", "Tokaji", "Villányi", "Csongrádi")  # borvidek names
SPOTLIGHT_EN = {"Soproni": "Sopron", "Tokaji": "Tokaj",
                "Villányi": "Villány", "Csongrádi": "Csongrád"}


# ---------------------------------------------------------------------------
# Figure S3, ensemble envelope vs. single member
# ---------------------------------------------------------------------------

def fig_s3_envelope():
    frames = []
    for rcp in ("rcp45", "rcp85"):
        for period in ("1971-2000", "1991-2020",
                       "2021-2040", "2041-2060", "2061-2080", "2081-2100"):
            scen = "observed" if period in ("1971-2000", "1991-2020") else rcp
            p = ENSEMBLE_DIR / f"ensemble_suitability_{period}_{scen}.parquet"
            if not p.exists():
                continue
            df = pd.read_parquet(p)
            # national mean across (borvidek, variety)
            nat = df.groupby("n_members")[["mean", "p10", "p90"]].apply(
                lambda g: pd.Series({
                    "mean": g["mean"].mean(),
                    "p10": g["p10"].mean(),
                    "p90": g["p90"].mean(),
                })
            ).reset_index(drop=True)
            mid = {"1971-2000": 1986, "1991-2020": 2006,
                   "2021-2040": 2031, "2041-2060": 2051,
                   "2061-2080": 2071, "2081-2100": 2091}[period]
            nat["year"] = mid
            nat["rcp"] = rcp
            frames.append(nat)
    if not frames:
        print("[s12] S3: no ensemble_suitability parquet found, skipping")
        return
    big = pd.concat(frames, ignore_index=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    for rcp, colour in (("rcp45", "#3B82F6"), ("rcp85", "#DC2626")):
        sub = big[big["rcp"] == rcp].sort_values("year")
        ax.fill_between(sub["year"], sub["p10"], sub["p90"],
                        alpha=0.25, color=colour, label=f"{rcp.upper()} 14-member p10-p90")
        ax.plot(sub["year"], sub["mean"], color=colour, lw=2,
                label=f"{rcp.upper()} ensemble mean")
    ax.set_xlabel("Year (period midpoint)")
    ax.set_ylabel("National mean suitability")
    ax.set_ylim(0, 1)
    ax.set_title("")  # appendix figures keep titles empty in body; caption added by markdown
    ax.legend(loc="lower left", fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_envelope.png", dpi=160)
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_envelope.pdf")
    plt.close(fig)
    print("[s12] wrote fig3_appendix_ensemble_envelope.{png,pdf}")


# ---------------------------------------------------------------------------
# Figure S4, p10/p50/p90 district maps at 2081-2100 RCP8.5
# ---------------------------------------------------------------------------

def fig_s4_district_maps():
    p = ENSEMBLE_DIR / "ensemble_suitability_2081-2100_rcp85.parquet"
    if not p.exists():
        print("[s12] S4: ensemble_suitability_2081-2100_rcp85.parquet missing, skipping")
        return
    df = pd.read_parquet(p)
    by_dist = df.groupby("borvidek")[["p10", "p50", "p90"]].mean().reset_index()

    gdf = gpd.read_file(ANALYSIS / "geo" / "wine_districts.gpkg").to_crs("EPSG:3857")
    merged = gdf.merge(by_dist, on="borvidek", how="left")
    # Actual Hungary national boundary: dissolve the admin8 settlements layer
    # (which covers the whole country, unlike the wine-district polygons).
    try:
        admin8 = gpd.read_file(Path(r"C:/Bor-szőlő/admin8.shp")).to_crs("EPSG:3857")
        hu_poly = admin8.dissolve()
        hu_outline = hu_poly.boundary
    except Exception:
        hu_outline = gdf.dissolve().boundary

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5),
                              gridspec_kw={"wspace": 0.05})
    # compute common extent — use Hungary total bounds so the country sits
    # inside each panel
    try:
        xmin, ymin, xmax, ymax = hu_poly.total_bounds
    except NameError:
        xmin, ymin, xmax, ymax = merged.total_bounds
    dx, dy = xmax - xmin, ymax - ymin
    pad = 0.04
    extent_x = (xmin - dx * pad, xmax + dx * pad)
    extent_y = (ymin - dy * pad, ymax + dy * pad)

    import matplotlib.patches as mpatches
    last_im = None
    for ax, col, title in zip(axes, ("p10", "p50", "p90"),
                               ("10th percentile (pessimistic)",
                                "Median",
                                "90th percentile (optimistic)")):
        try:
            hu_poly.plot(ax=ax, color="#f5f5f5", edgecolor="black",
                         linewidth=1.2, zorder=1)
        except NameError:
            pass
        merged.plot(column=col, ax=ax, cmap="RdYlGn", vmin=0, vmax=1,
                    edgecolor="grey", linewidth=0.4, legend=False, zorder=2)
        try:
            hu_outline.plot(ax=ax, color="black", linewidth=1.3, zorder=3)
        except NameError:
            pass
        ax.set_xlim(extent_x); ax.set_ylim(extent_y)
        ax.set_title(title, fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        last_im = ax.collections[-1]

    # Unified colorbar at the bottom
    cax = fig.add_axes([0.15, 0.10, 0.70, 0.025])
    fig.colorbar(last_im, cax=cax, orientation="horizontal",
                 label="Ensemble suitability (0-1)")

    # North arrow in the first panel
    ax0 = axes[0]
    x_arrow = extent_x[0] + (extent_x[1] - extent_x[0]) * 0.05
    y_arrow = extent_y[0] + (extent_y[1] - extent_y[0]) * 0.82
    arrow_len = (extent_y[1] - extent_y[0]) * 0.08
    ax0.annotate("N", xy=(x_arrow, y_arrow + arrow_len),
                 xytext=(x_arrow, y_arrow),
                 arrowprops=dict(arrowstyle="->", color="black", lw=1.4),
                 ha="center", fontsize=11, fontweight="bold")

    # Scale bar (100 km) in the last panel, using Web Mercator metres corrected
    # for Hungary latitude ~47 deg N (scale factor cos(47) = 0.682)
    import math
    sb_len_m = 100_000.0 / math.cos(math.radians(47.5))  # display length on Mercator
    ax2 = axes[-1]
    x0 = extent_x[0] + (extent_x[1] - extent_x[0]) * 0.55
    y0 = extent_y[0] + (extent_y[1] - extent_y[0]) * 0.08
    ax2.plot([x0, x0 + sb_len_m], [y0, y0], color="black", lw=2.2, zorder=4)
    ax2.text(x0 + sb_len_m / 2, y0 + (extent_y[1] - extent_y[0]) * 0.025,
             "100 km", ha="center", fontsize=9)

    fig.suptitle("Ensemble suitability across 14 EURO-CORDEX members, "
                 "2081-2100 RCP8.5", fontsize=12, y=0.97)
    # leave room for bottom colorbar
    fig.subplots_adjust(top=0.90, bottom=0.18, left=0.01, right=0.99)
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_maps.png", dpi=180,
                bbox_inches="tight")
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_maps.pdf",
                bbox_inches="tight")
    plt.close(fig)
    print("[s12] wrote fig3_appendix_ensemble_maps.{png,pdf}")


# ---------------------------------------------------------------------------
# Figure S5, crossover-year distribution per district
# ---------------------------------------------------------------------------

def fig_s5_crossover():
    """Per-member horizontal bar chart of national-mean suitability crossover
    year under RCP8.5. Each of the 14 EURO-CORDEX members is a separate row,
    sorted by year. Reads much more cleanly than the histogram and makes it
    obvious which members are the earliest / latest / reference (CNRM-ALADIN53).
    """
    p = ENSEMBLE_DIR / "ensemble_crossover_year.parquet"
    if not p.exists():
        print("[s12] S5: ensemble_crossover_year.parquet missing, skipping")
        return
    df = pd.read_parquet(p).sort_values("crossover_year_rcp85").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    y = np.arange(len(df))
    # highlight CNRM-ALADIN53 (the main-text reference member)
    colours = ["#DC2626" if m == "CNRM_ALADIN53" else "#9333EA"
               for m in df["member"]]
    ax.barh(y, df["crossover_year_rcp85"] - 2006, left=2006,
            color=colours, edgecolor="white", alpha=0.9)
    for i, (m, yr) in enumerate(zip(df["member"], df["crossover_year_rcp85"])):
        ax.text(yr + 0.6, i, f"{int(yr)}", va="center", fontsize=9)

    mean_y = df["crossover_year_rcp85"].mean()
    p10 = df["crossover_year_rcp85"].quantile(0.10)
    p90 = df["crossover_year_rcp85"].quantile(0.90)
    ax.axvline(mean_y, color="black", lw=1.6, ls="--",
               label=f"ensemble mean = {mean_y:.0f}")
    ax.axvspan(p10, p90, color="grey", alpha=0.12,
               label=f"p10 - p90 = {p10:.0f} - {p90:.0f}")

    ax.set_yticks(y)
    ax.set_yticklabels(df["member"], fontsize=8)
    ax.invert_yaxis()  # earliest at top
    ax.set_xlabel("Year of national-mean suitability crossover (RCP8.5)")
    ax.set_xlim(2000, 2105)
    ax.grid(axis="x", color="grey", alpha=0.3, lw=0.5)
    ax.set_axisbelow(True)
    # annotate the reference member
    ref_idx = int(df.index[df["member"] == "CNRM_ALADIN53"][0]) if \
        (df["member"] == "CNRM_ALADIN53").any() else None
    if ref_idx is not None:
        ax.annotate("reference member\n(main-text narrative)",
                    xy=(df["crossover_year_rcp85"].iloc[ref_idx], ref_idx),
                    xytext=(2045, ref_idx + 1.5),
                    fontsize=8, color="#DC2626",
                    arrowprops=dict(arrowstyle="->", color="#DC2626", lw=0.9))
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_crossover.png", dpi=160)
    fig.savefig(PAPER_FIG / "fig3_appendix_ensemble_crossover.pdf")
    plt.close(fig)
    print("[s12] wrote fig3_appendix_ensemble_crossover.{png,pdf}")


# ---------------------------------------------------------------------------
# Table S1, per-member crossover + 2081-2100 spotlight p10/p90
# ---------------------------------------------------------------------------

def table_s1():
    cross_p = ENSEMBLE_DIR / "ensemble_crossover_year.parquet"
    suit_p  = ENSEMBLE_DIR / "ensemble_suitability_2081-2100_rcp85.parquet"
    if not (cross_p.exists() and suit_p.exists()):
        print("[s12] TableS1: prerequisite parquet missing, skipping")
        return
    cross = pd.read_parquet(cross_p)
    suit = pd.read_parquet(suit_p)
    spot = suit[suit["borvidek"].isin(SPOTLIGHT)] \
        .groupby("borvidek")[["mean", "p10", "p50", "p90"]].mean().reset_index()
    spot["district_en"] = spot["borvidek"].map(SPOTLIGHT_EN)
    spot = spot[["district_en", "mean", "p10", "p50", "p90"]]
    spot.columns = ["District", "Ensemble mean", "p10", "p50", "p90"]

    def _to_md(df: pd.DataFrame, float_cols: dict[str, str]) -> str:
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

    out_md = ENSEMBLE_DIR / "table_s1_ensemble.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("### Table S1a. Spotlight suitability, 14-member ensemble, 2081-2100 RCP8.5\n\n")
        f.write(_to_md(spot, {"Ensemble mean": ".3f", "p10": ".3f",
                              "p50": ".3f", "p90": ".3f"}))
        f.write("\n\n### Table S1b. Per-member crossover year (RCP8.5)\n\n")
        f.write(_to_md(cross, {"crossover_year_rcp85": ".0f"}))
        f.write("\n")
    print(f"[s12] wrote {out_md}")


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = [
            ex.submit(fig_s3_envelope),
            ex.submit(fig_s4_district_maps),
            ex.submit(fig_s5_crossover),
            ex.submit(table_s1),
        ]
        for f in futs:
            f.result()  # re-raise any exception
    print(f"[s12] DONE in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
