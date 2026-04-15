#!/usr/bin/env python3
"""Figure 5: CCKP cross-check scatter with borrégió spotlight colours."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
})

# Spotlight districts — 4 maximally distinct colors per user request
SPOTLIGHTS = {
    'Tokaji':    ('#DC2626', 'Tokaj'),              # red
    'Villányi':  ('#2563EB', 'Pannon'),             # blue
    'Csongrádi': ('#F59E0B', 'Duna'),               # yellow/amber
    'Soproni':   ('#16A34A', 'North Transdanubia'),  # green
}
# English display names for legend labels
DISTRICT_DISPLAY = {
    'Tokaji': 'Tokaj', 'Villányi': 'Villány',
    'Csongrádi': 'Csongrád', 'Soproni': 'Sopron',
}

BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated')

# --- FORESEE-HUN normals (2081-2100 RCP8.5) ---
normals = pd.read_parquet(os.path.join(BASE, 'normals', 'normals_2081-2100_rcp85_per_district.parquet'))

# Estimate mean annual temperature from Winkler GDD:
# Winkler GDD = sum(max(Tmean - 10, 0)) over Apr-Oct (~214 days)
# T_growing ≈ GDD/214 + 10; T_annual ≈ T_growing - 3.5 (seasonal offset)
foresee_winkler = normals[normals['index'] == 'winkler_gdd'][['borvidek', 'mean']].copy()
foresee_winkler['foresee_tas_est'] = foresee_winkler['mean'] / 214 + 10 - 3.5
foresee_winkler = foresee_winkler[['borvidek', 'foresee_tas_est']]

# --- CCKP data (SSP5-8.5, 2080-2099) ---
cckp_tas = pd.read_parquet(os.path.join(BASE, 'cckp', 'cckp_cmip6_tas_ssp585_per_district.parquet'))
cckp_tas_fut = cckp_tas[
    (cckp_tas['period'] == '2080-2099') & (cckp_tas['stat'] == 'mean')
][['borvidek', 'value']].rename(columns={'value': 'cckp_tas'})

# Merge
merged = pd.merge(foresee_winkler, cckp_tas_fut, on='borvidek', how='inner')
n_districts = len(merged)

# --- Plot ---
fig, ax = plt.subplots(figsize=(180/25.4, 140/25.4))

x_vals = merged['foresee_tas_est'].values
y_vals = merged['cckp_tas'].values

# 1:1 reference line
all_vals = np.concatenate([x_vals, y_vals])
lo, hi = all_vals.min() - 0.5, all_vals.max() + 0.5
ax.plot([lo, hi], [lo, hi], '--', color='#9ca3af', linewidth=1.0, zorder=1, label='1:1 line')

# Non-spotlight districts in grey
other_mask = ~merged['borvidek'].isin(SPOTLIGHTS.keys())
ax.scatter(merged.loc[other_mask, 'foresee_tas_est'],
           merged.loc[other_mask, 'cckp_tas'],
           s=40, c='#CCCCCC', edgecolors='#999999', linewidth=0.5,
           alpha=0.9, zorder=3, label='Other districts')

# Spotlight districts with borrégió colours
for district, (color, region_name) in SPOTLIGHTS.items():
    row = merged[merged['borvidek'] == district]
    if row.empty:
        print(f'  WARNING: {district} not found in merged data')
        continue
    ax.scatter(row['foresee_tas_est'], row['cckp_tas'],
               s=70, c=color, edgecolors='black', linewidth=0.7,
               zorder=5, label=f'{DISTRICT_DISPLAY.get(district, district)} ({region_name})')

# Annotate spotlights — stacked vertically to avoid overlap
# Collect positions, then offset
annotations = []
for district, (color, region_name) in SPOTLIGHTS.items():
    row = merged[merged['borvidek'] == district]
    if row.empty:
        continue
    annotations.append((district, row['foresee_tas_est'].values[0],
                         row['cckp_tas'].values[0], color))

# Sort by y-position to stack annotations
annotations.sort(key=lambda a: a[2])

# Spotlight labels removed per user request — the legend box is sufficient.
# The coloured points in the scatter already identify the 4 spotlights via
# the legend; redundant text labels cluttered the figure.

# Pearson r and RMSE
r, p = stats.pearsonr(x_vals, y_vals)
rmse = np.sqrt(np.mean((x_vals - y_vals)**2))
ax.text(0.05, 0.95, f'r = {r:.2f}\nRMSE = {rmse:.1f} °C',
        transform=ax.transAxes, fontsize=9, va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='#d1d5db'))

ax.set_xlabel('FORESEE-HUN est. T$_{annual}$ (°C)')
ax.set_ylabel('CCKP CMIP6 T$_{annual}$ (°C)')
ax.set_xlim(lo, hi)
ax.set_ylim(lo, hi)
ax.set_aspect('equal', adjustable='box')

ax.legend(fontsize=7.5, loc='lower right', framealpha=0.9,
          borderpad=0.6, labelspacing=0.4)

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig5_cckp_crosscheck.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig5_cckp_crosscheck.png'), dpi=300, bbox_inches='tight')
plt.close()

print(f'Figure 5 saved. {n_districts} districts plotted.')
for f in ['fig5_cckp_crosscheck.pdf', 'fig5_cckp_crosscheck.png']:
    sz = os.path.getsize(os.path.join(outdir, f))
    print(f'  {f}: {sz:,} bytes')
