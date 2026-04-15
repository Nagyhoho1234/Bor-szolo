#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 4 – Variety Adaptation Strategy across four Hungarian wine districts
with MIXED time horizons per district.

Panels:
  Top-left:     Tokaji    2061-2080 RCP8.5 (early stress)
  Top-right:    Soproni   2061-2080 RCP8.5 (climate refuge)
  Bottom-left:  Villányi  2081-2100 RCP8.5 (deep crisis)
  Bottom-right: Csongrádi 2081-2100 RCP8.5 (existential threat)
"""

import json
import os
import sys
import io

# Force UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = r"C:\Bor-szőlő"
JSON_DIR = os.path.join(BASE, "analysis", "curated", "variety_replacements")
PARQUET = os.path.join(BASE, "analysis", "curated", "variety_match", "suitability_long.parquet")
OUT_DIR = os.path.join(BASE, "ResearchPotential", "paper", "figures")

# ── Load parquet ───────────────────────────────────────────────────────────
pq = pd.read_parquet(PARQUET)

def pq_suit(borvidek, variety, period, scenario):
    """Lookup suitability from parquet."""
    mask = (
        (pq["borvidek"] == borvidek)
        & (pq["variety"] == variety)
        & (pq["period"] == period)
        & (pq["scenario"] == scenario)
    )
    rows = pq.loc[mask, "suitability"]
    if len(rows) == 0:
        return None
    return float(rows.iloc[0])

# ── Panel configuration ───────────────────────────────────────────────────
PANELS = [
    {"slug": "tokaji",    "borvidek": "Tokaji",    "label": "Tokaj",     "period": "2081-2100"},
    {"slug": "soproni",   "borvidek": "Soproni",   "label": "Sopron",    "period": "2081-2100"},
    {"slug": "villanyi",  "borvidek": "Villányi",   "label": "Villány",   "period": "2061-2080"},
    {"slug": "csongradi", "borvidek": "Csongrádi",  "label": "Csongrád",  "period": "2061-2080"},
]

# ── Colours ────────────────────────────────────────────────────────────────
C_BASE = "#9CA3AF"
C_45   = "#2563EB"
C_85   = "#DC2626"

# ── Build data per panel ──────────────────────────────────────────────────
fallback_notes = []

def load_panel(cfg):
    """Return (principals_rows, replacements_rows) each as list of dicts
    with keys: variety, baseline, rcp45, rcp85."""
    slug = cfg["slug"]
    borvidek = cfg["borvidek"]
    period = cfg["period"]
    rcp85_key = f"{period}_rcp85"
    rcp45_key = f"{period}_rcp45"

    with open(os.path.join(JSON_DIR, f"{slug}.json"), encoding="utf-8") as f:
        data = json.load(f)

    principals_info = data["current_principal_varieties"]
    horizon_85 = data["horizons"].get(rcp85_key, {})
    horizon_45 = data["horizons"].get(rcp45_key, {})

    at_risk_85 = {v["variety"]: v for v in horizon_85.get("at_risk_principal_varieties", [])}
    at_risk_45 = {v["variety"]: v for v in horizon_45.get("at_risk_principal_varieties", [])}

    # Principals
    principals = []
    for p in principals_info:
        name = p["variety"]
        baseline = p.get("suitability") or p.get("baseline_suitability")
        if baseline is None:
            baseline = pq_suit(borvidek, name, "1991-2020", "observed")
            if baseline is not None:
                fallback_notes.append(f"{borvidek}/{name}: baseline from parquet")

        # RCP8.5
        if name in at_risk_85:
            rcp85 = at_risk_85[name]["future_suitability"]
        else:
            rcp85 = pq_suit(borvidek, name, period, "rcp85")
            if rcp85 is None:
                rcp85 = baseline
                fallback_notes.append(f"{borvidek}/{name}: rcp85 fallback to baseline")
            else:
                fallback_notes.append(f"{borvidek}/{name}: rcp85 from parquet ({rcp85:.3f})")

        # RCP4.5
        if name in at_risk_45:
            rcp45 = at_risk_45[name]["future_suitability"]
        else:
            rcp45 = pq_suit(borvidek, name, period, "rcp45")
            if rcp45 is None:
                rcp45 = baseline
                fallback_notes.append(f"{borvidek}/{name}: rcp45 fallback to baseline")
            else:
                fallback_notes.append(f"{borvidek}/{name}: rcp45 from parquet ({rcp45:.3f})")

        principals.append({"variety": name, "baseline": baseline, "rcp45": rcp45, "rcp85": rcp85})

    # Sort principals by rcp85 suitability descending (worst at bottom)
    principals.sort(key=lambda x: x["rcp85"], reverse=True)

    # Replacements – top 4 from rcp85 horizon, excluding principals
    principal_names = {p["variety"] for p in principals_info}
    repl_cands_85 = horizon_85.get("replacement_candidates", [])
    repl_cands_85 = [r for r in repl_cands_85 if r["variety"] not in principal_names][:4]

    repl_cands_45 = {r["variety"]: r for r in horizon_45.get("replacement_candidates", [])
                     if r["variety"] not in principal_names}

    replacements = []
    for r in repl_cands_85:
        name = r["variety"]
        rcp85 = r["future_suitability"]
        # Baseline from parquet
        baseline = pq_suit(borvidek, name, "1991-2020", "observed")
        if baseline is None:
            baseline = 0.0
            fallback_notes.append(f"{borvidek}/{name}: baseline not found, using 0.0")
        # RCP4.5
        if name in repl_cands_45:
            rcp45 = repl_cands_45[name]["future_suitability"]
        else:
            rcp45 = pq_suit(borvidek, name, period, "rcp45")
            if rcp45 is None:
                rcp45 = 0.0
                fallback_notes.append(f"{borvidek}/{name}: rcp45 not found, using 0.0")
            else:
                fallback_notes.append(f"{borvidek}/{name}: rcp45 from parquet ({rcp45:.3f})")
        replacements.append({"variety": name, "baseline": baseline, "rcp45": rcp45, "rcp85": rcp85})

    # Sort replacements by rcp85 descending
    replacements.sort(key=lambda x: x["rcp85"], reverse=True)

    return principals, replacements


# ── Font setup ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.titlesize": 9.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7.5,
})

# ── Build figure ───────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(180 / 25.4, 210 / 25.4))
axes_flat = [axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]]

bar_height = 0.22
group_gap = 0.7

for ax, cfg in zip(axes_flat, PANELS):
    principals, replacements = load_panel(cfg)
    n_princ = len(principals)
    n_repl = len(replacements)

    # Y positions: principals on top, replacements on bottom
    # Top group: y positions from top
    y_princ = []
    for i in range(n_princ):
        y_princ.append(n_repl + group_gap + (n_princ - 1 - i))

    y_repl = []
    for i in range(n_repl):
        y_repl.append(n_repl - 1 - i)

    y_positions = y_princ + y_repl
    all_rows = principals + replacements
    labels = [row["variety"] for row in all_rows]

    for row, y in zip(all_rows, y_positions):
        offsets = [bar_height, 0, -bar_height]
        colors = [C_BASE, C_45, C_85]
        values = [row["baseline"], row["rcp45"], row["rcp85"]]
        for off, col, val in zip(offsets, colors, values):
            if val is not None:
                ax.barh(y + off, val, height=bar_height, color=col,
                        edgecolor="white", linewidth=0.3)

    # Separator line between groups
    if n_repl > 0 and n_princ > 0:
        sep_y = n_repl + group_gap / 2 - 0.5
        ax.axhline(y=sep_y, color="#6B7280", linewidth=0.5, linestyle="--")

    # Y axis
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("Suitability")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(0.2))
    ax.xaxis.set_minor_locator(mticker.MultipleLocator(0.1))

    # Title
    period_display = cfg["period"].replace("-", "\u2013")
    ax.set_title(f"$\\bf{{{cfg['label']}}}$ ({period_display})", fontsize=9.5, pad=6)

    # Grid
    ax.grid(axis="x", alpha=0.25, linewidth=0.4)
    ax.set_axisbelow(True)

    # Spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Y limits
    ymin = min(y_positions) - 0.6
    ymax = max(y_positions) + 0.6
    ax.set_ylim(ymin, ymax)

    # Group annotations on right margin
    mid_princ_y = np.mean(y_princ) if y_princ else 0
    mid_repl_y = np.mean(y_repl) if y_repl else 0

    ax.text(1.03, mid_princ_y, "Current\nvarieties", transform=ax.get_yaxis_transform(),
            fontsize=5.5, color="#6B7280", va="center", ha="left", style="italic")
    if n_repl > 0:
        ax.text(1.03, mid_repl_y, "Replacement\ncandidates", transform=ax.get_yaxis_transform(),
                fontsize=5.5, color="#6B7280", va="center", ha="left", style="italic")

# ── Legend at bottom ───────────────────────────────────────────────────────
legend_elements = [
    Patch(facecolor=C_BASE, edgecolor="white", label="Baseline (1991\u20132020)"),
    Patch(facecolor=C_45, edgecolor="white", label="RCP4.5"),
    Patch(facecolor=C_85, edgecolor="white", label="RCP8.5"),
]
fig.legend(handles=legend_elements, loc="lower center", ncol=3,
           frameon=False, fontsize=7.5, bbox_to_anchor=(0.5, 0.002))

plt.tight_layout(rect=[0, 0.032, 0.96, 1.0])

# ── Save ───────────────────────────────────────────────────────────────────
pdf_path = os.path.join(OUT_DIR, "fig4_adaptation.pdf")
png_path = os.path.join(OUT_DIR, "fig4_adaptation.png")
fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved: {pdf_path}")
print(f"Saved: {png_path}")
print(f"PDF size: {os.path.getsize(pdf_path):,} bytes")
print(f"PNG size: {os.path.getsize(png_path):,} bytes")

# ── Report ─────────────────────────────────────────────────────────────────
print("\n=== PANEL SUMMARY ===")
for cfg in PANELS:
    principals, replacements = load_panel(cfg)
    print(f"\n{cfg['label']} ({cfg['period']} RCP8.5):")
    print(f"  Principals: {len(principals)} varieties")
    for p in principals:
        print(f"    {p['variety']:25s}  base={p['baseline']:.3f}  rcp45={p['rcp45']:.3f}  rcp85={p['rcp85']:.3f}")
    print(f"  Replacements: {len(replacements)} varieties")
    for r in replacements:
        print(f"    {r['variety']:25s}  base={r['baseline']:.3f}  rcp45={r['rcp45']:.3f}  rcp85={r['rcp85']:.3f}")

print("\n=== DATA FALLBACKS ===")
for note in fallback_notes:
    print(f"  {note}")
