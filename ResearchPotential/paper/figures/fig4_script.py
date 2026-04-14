#!/usr/bin/env python3
"""Figure 4: Adaptation recommendations for Tokaji + Csongrádi."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
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

# --- Load Tokaji ---
with open(os.path.join(BASE, 'variety_replacements', 'tokaji.json'), encoding='utf-8') as f:
    tok = json.load(f)

tok_horizon = tok['horizons']['2081-2100_rcp85']
tok_principals = tok['current_principal_varieties']
tok_at_risk = tok_horizon['at_risk_principal_varieties']
tok_replacements = tok_horizon['replacement_candidates']

# Build Tokaji data
tok_data = []
for v in tok_at_risk:
    tok_data.append({
        'variety': v['variety_en'],
        'baseline': v.get('suitability', next((p['suitability'] for p in tok_principals if p['variety_en'] == v['variety_en']), np.nan)),
        'future': v['future_suitability'],
        'group': 'Current (at-risk)'
    })
for v in tok_replacements[:4]:
    tok_data.append({
        'variety': v['variety_en'],
        'baseline': 0.0,  # not currently planted
        'future': v['future_suitability'],
        'group': 'Recommended'
    })

# --- Load Csongrádi ---
with open(os.path.join(BASE, 'variety_replacements', 'csongradi.json'), encoding='utf-8') as f:
    cso = json.load(f)

# Csongrádi: no 2081-2100_rcp85 horizon, use 2081-2100_rcp45 for at-risk OR 2061-2080_rcp85
# The horizons available: up to 2081-2100_rcp45 (last one)
# Use 2061-2080_rcp85 for the future values
cso_horizon = cso['horizons']['2061-2080_rcp85']
cso_principals = cso['current_principal_varieties']
cso_at_risk = cso_horizon['at_risk_principal_varieties']
cso_replacements = cso_horizon['replacement_candidates']

# For Csongrádi, also get Mediterranean varieties from suitability_long for 2081-2100 rcp85
suit = pd.read_parquet(os.path.join(BASE, 'variety_match', 'suitability_long.parquet'))
cso_suit = suit[(suit['borvidek'] == 'Csongrádi') &
                (suit['period'] == '2081-2100') &
                (suit['scenario'] == 'rcp85')]
med_varieties = ['Tempranillo', 'Touriga Nacional', 'Grenache', 'Mourvèdre / Monastrell',
                 'Carignan / Mazuelo', 'Aglianico', 'Assyrtiko']

# Get baseline suitability for Csongrádi (1991-2020 observed)
cso_base = suit[(suit['borvidek'] == 'Csongrádi') &
                (suit['period'] == '1991-2020') &
                (suit['scenario'] == 'observed')]

cso_data = []
for v in cso_at_risk:
    name = v['variety_en']
    base_val = next((p['suitability'] for p in cso_principals if p['variety_en'] == name), np.nan)
    cso_data.append({
        'variety': name,
        'baseline': base_val,
        'future': v['future_suitability'],
        'group': 'Current (at-risk)'
    })

# Add Mediterranean varieties from suitability matrix
for mv in med_varieties:
    row_fut = cso_suit[cso_suit['variety_en'] == mv]
    row_base = cso_base[cso_base['variety_en'] == mv]
    if not row_fut.empty:
        cso_data.append({
            'variety': mv,
            'baseline': float(row_base['suitability'].values[0]) if not row_base.empty else 0.0,
            'future': float(row_fut['suitability'].values[0]),
            'group': 'Mediterranean candidates'
        })

# --- Plot ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(180/25.4, 120/25.4), sharey=False)

def plot_bars(ax, data, title, panel_label):
    df = pd.DataFrame(data)

    # Separate groups
    current = df[df['group'].str.contains('Current')].copy()
    replacements = df[~df['group'].str.contains('Current')].copy()

    # Combine with a separator
    all_vars = list(replacements['variety']) + [''] + list(current['variety'])
    all_baseline = list(replacements['baseline']) + [0] + list(current['baseline'])
    all_future = list(replacements['future']) + [0] + list(current['future'])
    is_sep = [False]*len(replacements) + [True] + [False]*len(current)

    y_pos = np.arange(len(all_vars))
    bar_h = 0.35

    for i, (yp, bl, fu, sep) in enumerate(zip(y_pos, all_baseline, all_future, is_sep)):
        if sep:
            ax.axhline(yp, color='#9ca3af', linewidth=0.8, linestyle='-')
            continue
        ax.barh(yp + bar_h/2, bl, bar_h, color=GREY, alpha=0.7, zorder=3)
        ax.barh(yp - bar_h/2, fu, bar_h, color=RED, alpha=0.85, zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_vars, fontsize=7)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel('Suitability')

    # Panel label
    ax.text(0.02, 0.98, panel_label, transform=ax.transAxes, fontsize=12,
            fontweight='bold', va='top')
    ax.set_title(title, fontsize=9, pad=8)

    # Legend
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor=GREY, alpha=0.7, label='Baseline (1991–2020)'),
        Patch(facecolor=RED, alpha=0.85, label='2081–2100 RCP8.5'),
    ], fontsize=6.5, loc='lower right', framealpha=0.9)

    # Group labels on right side
    n_repl = len(replacements)
    n_curr = len(current)
    if n_repl > 0:
        ax.text(1.02, (n_repl-1)/2 / (len(all_vars)-1), 'Replacements',
                transform=ax.get_yaxis_transform(), fontsize=6, va='center', rotation=-90, color=BLUE)
    if n_curr > 0:
        mid_curr = (n_repl + 1 + (n_curr-1)/2) / (len(all_vars)-1)
        ax.text(1.02, mid_curr, 'Current',
                transform=ax.get_yaxis_transform(), fontsize=6, va='center', rotation=-90, color=RED)

plot_bars(ax1, tok_data, 'Tokaji', '(a)')
plot_bars(ax2, cso_data, 'Csongrádi', '(b)')

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig4_adaptation.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig4_adaptation.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Figure 4 saved.')
