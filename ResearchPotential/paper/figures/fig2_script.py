#!/usr/bin/env python3
"""Figure 2: 4-panel Winkler GDD spotlight."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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

BLUE = '#2563eb'
RED  = '#dc2626'
GREY = '#374151'

BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated')
df45 = pd.read_parquet(os.path.join(BASE, 'indices', 'indices_rcp45_annual.parquet'))
df85 = pd.read_parquet(os.path.join(BASE, 'indices', 'indices_rcp85_annual.parquet'))

spotlights = ['Tokaji', 'Villányi', 'Csongrádi', 'Soproni']
labels = ['(a) Tokaji', '(b) Villányi', '(c) Csongrádi', '(d) Soproni']
transitions = ['Ia \u2192 IV', 'Ib \u2192 IV', 'Ib \u2192 IV', 'Ia \u2192 III']

winkler_boundaries = [1111, 1389, 1667, 1944, 2222, 2500]
winkler_labels_map = {1111: 'Ia/Ib', 1389: 'Ib/II', 1667: 'II/III', 1944: 'III/IV', 2222: 'IV/V', 2500: 'V+'}

fig, axes = plt.subplots(2, 2, figsize=(180/25.4, 140/25.4), sharex=True)

for idx, (district, label, trans) in enumerate(zip(spotlights, labels, transitions)):
    ax = axes[idx // 2, idx % 2]

    d45 = df45[df45['borvidek'] == district].sort_values('year')
    d85 = df85[df85['borvidek'] == district].sort_values('year')

    # Observed: up to 2020 (shared between rcp45 and rcp85)
    obs = d45[d45['year'] <= 2020]
    proj45 = d45[d45['year'] >= 2021]
    proj85 = d85[d85['year'] >= 2021]

    # 11-year rolling mean
    def rolling(series, years, window=11):
        s = pd.Series(series.values, index=years.values)
        return s.rolling(window, center=True, min_periods=6).mean()

    obs_roll = rolling(obs['winkler_gdd'], obs['year'])
    p45_roll = rolling(proj45['winkler_gdd'], proj45['year'])
    p85_roll = rolling(proj85['winkler_gdd'], proj85['year'])

    # Also connect: last observed year to first projection year
    # Plot raw as faint, rolling as solid
    ax.plot(obs['year'], obs['winkler_gdd'], color=GREY, alpha=0.15, linewidth=0.5)
    ax.plot(obs_roll.index, obs_roll.values, color=GREY, linewidth=1.5, label='Observed')

    ax.plot(proj45['year'].values, proj45['winkler_gdd'].values, color=BLUE, alpha=0.15, linewidth=0.5)
    ax.plot(p45_roll.index, p45_roll.values, color=BLUE, linewidth=1.5, label='RCP4.5')

    ax.plot(proj85['year'].values, proj85['winkler_gdd'].values, color=RED, alpha=0.15, linewidth=0.5)
    ax.plot(p85_roll.index, p85_roll.values, color=RED, linewidth=1.5, label='RCP8.5')

    # Winkler class boundaries
    for wb in winkler_boundaries:
        ax.axhline(wb, color='#9ca3af', linestyle=':', linewidth=0.7, alpha=0.7)

    # Right-side labels for class boundaries that are in view
    ymin_data = min(obs['winkler_gdd'].min(), proj45['winkler_gdd'].min(), proj85['winkler_gdd'].min()) - 50
    ymax_data = max(obs['winkler_gdd'].max(), proj45['winkler_gdd'].max(), proj85['winkler_gdd'].max()) + 50
    for wb in winkler_boundaries:
        if ymin_data < wb < ymax_data:
            ax.text(2102, wb, winkler_labels_map[wb], fontsize=6, va='center', color='#6b7280')

    ax.set_ylim(ymin_data, ymax_data)
    ax.set_xlim(1971, 2100)

    # Panel label
    ax.text(0.02, 0.97, f'{label}: {trans}', transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))

    if idx >= 2:
        ax.set_xlabel('Year')
    if idx % 2 == 0:
        ax.set_ylabel('Winkler GDD (°C·d)')
    if idx == 0:
        ax.legend(fontsize=7, loc='lower right', framealpha=0.9)

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig2_spotlight_winkler.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig2_spotlight_winkler.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Figure 2 saved.')
