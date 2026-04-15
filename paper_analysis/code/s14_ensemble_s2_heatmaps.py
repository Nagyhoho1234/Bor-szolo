"""Step 14, ensemble-based S2 heatmaps.

For each of the 10 (period, scenario) combinations, render a two-panel
figure: left panel = ensemble **mean** suitability (57 varieties x 22
districts, across 14 members), right panel = ensemble **spread**
p90 - p10. Cell values are annotated.

Outputs land in ``ResearchPotential/paper/figures/`` under the name pattern
``fig3_appendix_ensemble_S2{letter}.{png,pdf}`` where ``letter`` is a-j in
the same order as the existing single-member S2a-S2j.
"""

from __future__ import annotations

import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ANALYSIS = Path(r"C:/Bor-szőlő/analysis")
import os as _os
_VARIANT = _os.environ.get("HUGLIN_VARIANT", "").upper()
ENS_DIR = (ANALYSIS / "curated" / "ensemble_variants" / _VARIANT) if _VARIANT else (ANALYSIS / "curated" / "ensemble")
PAPER_FIG = Path(r"C:/Bor-szőlő/ResearchPotential/paper/figures")
PAPER_FIG.mkdir(parents=True, exist_ok=True)

PERIOD_SCENARIOS = [
    ("S2a", "1971-2000", "observed"),
    ("S2b", "1991-2020", "observed"),
    ("S2c", "2021-2040", "rcp45"),
    ("S2d", "2021-2040", "rcp85"),
    ("S2e", "2041-2060", "rcp45"),
    ("S2f", "2041-2060", "rcp85"),
    ("S2g", "2061-2080", "rcp45"),
    ("S2h", "2061-2080", "rcp85"),
    ("S2i", "2081-2100", "rcp45"),
    ("S2j", "2081-2100", "rcp85"),
]


def _load_grown_varieties() -> set[str]:
    """Union of principal varieties across all 22 districts, from districts.yml.
    These appear in bold on the heatmap y-axis to mark currently-grown cultivars.
    """
    import yaml
    y = yaml.safe_load(
        (Path(r"C:/Bor-szőlő/analysis/config/districts.yml")).read_text(encoding="utf-8")
    )
    grown: set[str] = set()
    for entry in y.values():
        for v in (entry.get("principal_varieties") or []):
            grown.add(v.strip())
    return grown


def _load_principals_by_district() -> dict[str, set[str]]:
    """Map borvidek name -> set of principal varieties from districts.yml.
    Keys are the Hungarian borvidek names used in the parquet (e.g. 'Soproni').
    """
    import yaml
    y = yaml.safe_load(
        (Path(r"C:/Bor-szőlő/analysis/config/districts.yml")).read_text(encoding="utf-8")
    )
    return {k: {v.strip() for v in (entry.get("principal_varieties") or [])}
            for k, entry in y.items()}


def _render_one(letter: str, period: str, scen: str):
    """Render each period/scenario as two separate A4-portrait figures:
    ``fig3_appendix_ensemble_<letter>_mean.{png,pdf}`` and
    ``fig3_appendix_ensemble_<letter>_spread.{png,pdf}``.
    """
    p = ENS_DIR / f"ensemble_suitability_{period}_{scen}.parquet"
    if not p.exists():
        print(f"[s14] SKIP {letter}: {p.name} missing")
        return
    grown = _load_grown_varieties()
    principals_by_district = _load_principals_by_district()
    df = pd.read_parquet(p)
    mean_mat = df.pivot(index="variety", columns="borvidek", values="mean")
    spread_mat = (df.assign(spread=df["p90"] - df["p10"])
                    .pivot(index="variety", columns="borvidek", values="spread"))
    mean_mat = mean_mat.sort_index(axis=1)
    spread_mat = spread_mat.reindex(index=mean_mat.index, columns=mean_mat.columns)
    var_order = mean_mat.mean(axis=1).sort_values(ascending=False).index
    mean_mat = mean_mat.loc[var_order]
    spread_mat = spread_mat.loc[var_order]

    def _draw(mat, cmap, vmin, vmax, cbar_label, title, out_stem):
        # A4 portrait aspect: 8.27 x 11.69 inches
        fig, ax = plt.subplots(figsize=(8.27, 11.2))
        im = ax.imshow(mat.values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
        ax.set_title(title, fontsize=11, pad=8)
        ax.set_xticks(range(len(mat.columns)))
        ax.set_xticklabels(mat.columns, rotation=60, ha="right", fontsize=7)
        ax.set_yticks(range(len(mat.index)))
        ytick_labels = ax.set_yticklabels(mat.index, fontsize=6)
        # Bold currently-grown Hungarian principal varieties
        for t, name in zip(ytick_labels, mat.index):
            if name in grown:
                t.set_fontweight("bold")
        # Black cell borders around (variety, district) pairs where the variety
        # is a principal of that district (OEM-registered cultivar).
        import matplotlib.patches as mpatches
        for j, bv in enumerate(mat.columns):
            princ = principals_by_district.get(bv, set())
            if not princ:
                continue
            for i, variety in enumerate(mat.index):
                if variety in princ:
                    ax.add_patch(mpatches.Rectangle(
                        (j - 0.5, i - 0.5), 1, 1,
                        fill=False, edgecolor="black",
                        linewidth=1.1, zorder=4,
                    ))
        # cell annotations
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat.values[i, j]
                if pd.notna(v):
                    if cmap == "RdYlGn":
                        # mean: dark-red low end + dark-green high end = white text
                        txt_color = "white" if v < 0.22 or v > 0.88 else "black"
                    elif cmap == "RdYlGn_r":
                        # spread (reversed): only high-spread dark-red cells get white;
                        # low spread = green/yellow = black text (yellow is too light for white)
                        txt_color = "white" if v / max(vmax, 1e-9) > 0.85 else "black"
                    else:
                        txt_color = "white" if v < vmax * 0.6 else "black"
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                            fontsize=4.5, color=txt_color)
        cbar = fig.colorbar(im, ax=ax, shrink=0.7, label=cbar_label, pad=0.02)
        cbar.ax.tick_params(labelsize=8)
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(PAPER_FIG / f"{out_stem}.{ext}", dpi=150)
        plt.close(fig)

    _draw(mean_mat, "RdYlGn", 0, 1, "Mean suitability",
          f"Ensemble mean suitability, {period} {scen.upper()}",
          f"fig3_appendix_ensemble_{letter}_mean")

    spread_vmax = float(np.nanmax(spread_mat.values)) if spread_mat.size else 1.0
    spread_vmax = max(spread_vmax, 0.1)
    _draw(spread_mat, "RdYlGn_r", 0, spread_vmax, "p90 - p10 spread (green = robust, red = uncertain)",
          f"Ensemble spread (p90 - p10), {period} {scen.upper()}",
          f"fig3_appendix_ensemble_{letter}_spread")

    print(f"[s14] wrote fig3_appendix_ensemble_{letter}_{{mean,spread}}.{{png,pdf}}")


def main():
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(_render_one, letter, per, scen)
                for letter, per, scen in PERIOD_SCENARIOS]
        for f in futs:
            f.result()
    print(f"[s14] DONE in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
