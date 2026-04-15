#!/usr/bin/env python3
"""Figure 1: Regional inverted-U suitability trajectory under RCP8.5, coloured by borrégió."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Style ---
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

# --- Borrégió mapping (data names → display names) and colours ---
BORREGIO_DISPLAY = {
    'Felső-Pannon':        'North Transdanubia',
    'Balaton':              'Balaton',
    'Pannon':               'Pannon',
    'Duna':                 'Duna',
    'Felső-Magyarországi':  'Northern Hungary',
    'Tokaj':                'Tokaj',
}

BORREGIO_COLORS = {
    'North Transdanubia':   '#7B4EA0',
    'Balaton':              '#2E8B57',
    'Pannon':               '#A51E37',
    'Duna':                 '#E8A030',
    'Northern Hungary':     '#DC5A32',
    'Tokaj':                '#784628',
}

# Markers removed per user request — clean lines only, no symbols.

# --- Data ---
DATA = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated',
                     'variety_match', 'suitability_long.parquet')
df = pd.read_parquet(DATA)

periods = ['1971-2000', '1991-2020', '2021-2040', '2041-2060', '2061-2080', '2081-2100']
x = np.arange(len(periods))

# Keep only RCP8.5 + observed
df_rcp85 = df[(df['scenario'] == 'rcp85') | (df['scenario'] == 'observed')].copy()
# Map display names
df_rcp85['borregio_display'] = df_rcp85['borregio'].map(BORREGIO_DISPLAY)

# --- National average + 80% confidence interval (p10/p90 across 22 district means) ---
# Per-district mean suitability (across all 57 varieties)
dist_period = df_rcp85.groupby(['period', 'borvidek'])['suitability'].mean().reset_index()

# For each period, pick observed OR rcp85 (avoid double-counting observed periods)
# The data already handles this: observed periods have scenario='observed', future have 'rcp85'
national = dist_period.groupby('period')['suitability'].agg(
    mean='mean',
    p10=lambda s: s.quantile(0.10),
    p90=lambda s: s.quantile(0.90)
).reindex(periods)

# --- Borrégió group means ---
# Mean suitability per borrégió per period (average across districts in group × varieties)
borregio_period = df_rcp85.groupby(['period', 'borregio_display'])['suitability'].mean().reset_index()
borregio_pivot = borregio_period.pivot(index='period', columns='borregio_display', values='suitability').reindex(periods)

# --- Plot ---
fig, ax = plt.subplots(figsize=(180/25.4, 100/25.4))

# Grey ribbon (national p10-p90)
ax.fill_between(x, national['p10'].values, national['p90'].values,
                color='#999999', alpha=0.15, label='80% confidence interval', zorder=1)

# Regional lines (order for nice legend)
draw_order = ['North Transdanubia', 'Balaton', 'Pannon', 'Duna', 'Northern Hungary', 'Tokaj']
for br in draw_order:
    if br in borregio_pivot.columns:
        y = borregio_pivot[br].values
        ax.plot(x, y, color=BORREGIO_COLORS[br], linewidth=1.5,
                label=br, zorder=4)

# National mean (black dashed, no markers)
ax.plot(x, national['mean'].values, color='black', linewidth=2.0,
        linestyle='--', label='National mean', zorder=5)

ax.set_xticks(x)
ax.set_xticklabels(periods, rotation=30, ha='right')
ax.set_ylabel('Mean variety suitability')
ax.set_ylim(0, 1.0)
ax.set_xlim(-0.3, len(periods) - 0.7)

# Legend in the bottom-left corner with transparency so trends remain visible
ax.legend(fontsize=7, loc='lower left', framealpha=0.5, ncol=1,
          borderpad=0.5, labelspacing=0.3, edgecolor='#d1d5db')

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig1_inverted_u.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig1_inverted_u.png'), dpi=300, bbox_inches='tight')
plt.close()

# Report
n_districts = df_rcp85['borvidek'].nunique()
n_regions = borregio_pivot.shape[1]
print(f'Figure 1 saved. {n_districts} districts, {n_regions} borrégió groups.')
for f in ['fig1_inverted_u.pdf', 'fig1_inverted_u.png']:
    sz = os.path.getsize(os.path.join(outdir, f))
    print(f'  {f}: {sz:,} bytes')
