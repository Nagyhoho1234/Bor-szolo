#!/usr/bin/env python3
"""Figure 3: Variety-by-district suitability heatmap at 2081-2100 RCP8.5."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated')
df = pd.read_parquet(os.path.join(BASE, 'variety_match', 'suitability_long.parquet'))

# Filter to 2081-2100 RCP8.5
fut = df[(df['period'] == '2081-2100') & (df['scenario'] == 'rcp85')].copy()

# 15 key varieties
key_varieties = [
    'Furmint', 'Harslevelu', 'Blaufränkisch', 'Cabernet Franc',
    'Cabernet Sauvignon', 'Merlot', 'Welschriesling / Olaszrizling',
    'Pinot Noir', 'Riesling', 'Kadarka', 'Tempranillo',
    'Touriga Nacional', 'Assyrtiko', 'Souvignier Gris', 'Solaris'
]

fut_key = fut[fut['variety_en'].isin(key_varieties)]

# Pivot: rows=variety, cols=district
pivot = fut_key.pivot_table(index='variety_en', columns='borvidek', values='suitability', aggfunc='mean')

# Sort districts by baseline Winkler GDD (use 1991-2020 normals from indices)
df_idx = pd.read_parquet(os.path.join(BASE, 'indices', 'indices_rcp45_annual.parquet'))
baseline = df_idx[(df_idx['year'] >= 1991) & (df_idx['year'] <= 2020)]
dist_winkler = baseline.groupby('borvidek')['winkler_gdd'].mean().sort_values()
# Sort columns by baseline Winkler (coolest to warmest)
ordered_districts = [d for d in dist_winkler.index if d in pivot.columns]
pivot = pivot[ordered_districts]

# Sort varieties by mean suitability (highest at top)
variety_means = pivot.mean(axis=1).sort_values(ascending=True)
pivot = pivot.loc[variety_means.index]

# Display names for varieties (nicer labels)
display_names = {
    'Harslevelu': 'Hárslevelű',
    'Blaufränkisch': 'Blaufränkisch',
    'Welschriesling / Olaszrizling': 'Olaszrizling',
}

# Spotlight districts
spotlights = ['Tokaji', 'Villányi', 'Csongrádi', 'Soproni']

# --- Plot ---
fig, ax = plt.subplots(figsize=(180/25.4, 120/25.4))

# Diverging colormap: red (0) -> white (0.5) -> green (1.0)
cmap = plt.cm.RdYlGn
norm = mcolors.TwoSlopeNorm(vmin=0, vcenter=0.5, vmax=1.0)

im = ax.imshow(pivot.values, cmap=cmap, norm=norm, aspect='auto')

# Axis labels
yticks_labels = [display_names.get(v, v) for v in pivot.index]
ax.set_yticks(range(len(yticks_labels)))
ax.set_yticklabels(yticks_labels, fontsize=7.5)

xticks_labels = list(pivot.columns)
ax.set_xticks(range(len(xticks_labels)))
ax.set_xticklabels(xticks_labels, fontsize=7, rotation=55, ha='right')

# Highlight spotlight district columns
for sp in spotlights:
    if sp in pivot.columns:
        col_idx = list(pivot.columns).index(sp)
        # Bold the x-tick label
        tick_labels = ax.get_xticklabels()
        tick_labels[col_idx].set_fontweight('bold')
        tick_labels[col_idx].set_color('#dc2626')
        # Draw rectangle around the column
        rect = plt.Rectangle((col_idx - 0.5, -0.5), 1, len(pivot.index),
                              linewidth=1.5, edgecolor='#374151', facecolor='none', zorder=10)
        ax.add_patch(rect)

# Cell value annotations (suitability rounded to 2 decimals)
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        val = pivot.values[i, j]
        if not np.isnan(val):
            text_color = 'white' if val < 0.25 or val > 0.85 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=5, color=text_color)

# Colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Suitability', fontsize=9)
cbar.ax.tick_params(labelsize=7)

ax.set_title('Variety suitability at 2081–2100, RCP8.5', fontsize=10, pad=8)

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig3_heatmap_suitability.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig3_heatmap_suitability.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Figure 3 saved.')
